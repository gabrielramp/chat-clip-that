import socket
import threading
from test import start_editing
import cv2
import pyaudio
import struct
import time
import sys
import numpy as np
import heapq
from collections import deque
import whisper
import librosa
import os
import re
import wave
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip
import json
import logging
import tempfile

# Configuration
SERVER_IP = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 9999

# Audio Playback Configuration
AUDIO_RATE = 44100
AUDIO_CHANNELS = 1
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHUNK = 1024

# Initial delay to allow buffering (seconds)
INITIAL_DELAY = 1.0

# Global variables for synchronization
audio_buffer = []
video_buffer = []
audio_lock = threading.Lock()
video_lock = threading.Lock()

# Additional buffers for speech recognition and video saving
speech_recognition_buffer = deque()
video_deque = deque()  # To store last 30 seconds of video frames
VIDEO_FPS = 20.0  # Assuming 20 FPS; adjust if different
VIDEO_BUFFER_SECONDS = 30
video_deque_maxlen = int(VIDEO_FPS * VIDEO_BUFFER_SECONDS)
video_deque = deque(maxlen=video_deque_maxlen)

# Additional buffer for audio data
audio_deque_maxlen = int((AUDIO_RATE / AUDIO_CHUNK) * VIDEO_BUFFER_SECONDS)
audio_deque = deque(maxlen=audio_deque_maxlen)

# Playback start time
playback_start_time = None

# Flag to control the shutdown of threads
shutdown_flag = threading.Event()

# Directory to save video clips
SAVE_DIR = './just-saved'
os.makedirs(SAVE_DIR, exist_ok=True)

# Global variable for sample width
sample_width = None

# Configure logging
logging.basicConfig(level=logging.INFO)

def receive_stream(conn, playback_start_time_event):
    global playback_start_time, audio_buffer, video_buffer
    buffer = b''
    start_time_received = False
    while not shutdown_flag.is_set():
        try:
            data = conn.recv(4096)
            if not data:
                # No more data from client.
                shutdown_flag.set()
                break
            buffer += data
            # Received data from client.

            while True:
                if len(buffer) < 13:
                    # Not enough data for header
                    break
                # Read header
                packet_type = buffer[0:1]
                size = struct.unpack('!I', buffer[1:5])[0]
                timestamp = struct.unpack('!d', buffer[5:13])[0]
                if len(buffer) < 13 + size:
                    # Not enough data for the whole packet
                    break
                payload = buffer[13:13 + size]
                buffer = buffer[13 + size:]

                if not start_time_received:
                    # Initialize playback_start_time
                    playback_start_time = time.time() + INITIAL_DELAY
                    playback_start_time_event.set()
                    start_time_received = True
                    # Playback start time set.

                scheduled_time = playback_start_time + timestamp

                if packet_type == b'V':
                    with video_lock:
                        heapq.heappush(video_buffer, (scheduled_time, payload))
                        # Video packet buffered.
                elif packet_type == b'A':
                    with audio_lock:
                        heapq.heappush(audio_buffer, (scheduled_time, payload))
                        speech_recognition_buffer.append((timestamp, payload))
                        # Audio packet buffered and appended to speech recognition buffer.
                else:
                    # Unknown packet type.
                    pass

        except ConnectionResetError:
            # Connection reset by peer.
            shutdown_flag.set()
            break
        except Exception as e:
            # Error receiving data.
            logging.exception("Exception in receive_stream")
            shutdown_flag.set()
            break

    conn.close()
    # Connection closed.

def play_audio():
    global sample_width
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=AUDIO_FORMAT,
                        channels=AUDIO_CHANNELS,
                        rate=AUDIO_RATE,
                        output=True,
                        frames_per_buffer=AUDIO_CHUNK)
        # Audio stream opened successfully.
        sample_width = p.get_sample_size(AUDIO_FORMAT)
    except Exception as e:
        # Failed to open audio stream.
        logging.exception("Exception in play_audio during stream opening")
        shutdown_flag.set()
        return

    while not shutdown_flag.is_set():
        current_time = time.time()
        with audio_lock:
            if audio_buffer and audio_buffer[0][0] <= current_time:
                scheduled_time, data = heapq.heappop(audio_buffer)
                try:
                    stream.write(data)
                    # Audio data played.
                    # Append to audio_deque with timestamp
                    audio_deque.append((scheduled_time, data))
                except Exception as e:
                    # Error writing audio data.
                    logging.exception("Exception in play_audio during stream write")
                    shutdown_flag.set()
                    break
            else:
                pass
        time.sleep(0.001)  # Sleep briefly to prevent busy waiting.

    stream.stop_stream()
    stream.close()
    p.terminate()
    # Audio stream closed.

def display_video():
    global video_buffer
    cv2.namedWindow('Received Video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Received Video', 640, 480)
    # Video display window created.

    while not shutdown_flag.is_set():
        current_time = time.time()
        with video_lock:
            while video_buffer and video_buffer[0][0] <= current_time:
                scheduled_time, payload = heapq.heappop(video_buffer)
                try:
                    # Decode JPEG
                    np_arr = np.frombuffer(payload, dtype=np.uint8)
                    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    if frame is not None:
                        cv2.imshow('Received Video', frame)
                        # Append to video_deque with timestamp
                        video_deque.append((scheduled_time, frame))
                        # Displayed and buffered video frame.
                    else:
                        # Failed to decode video frame.
                        logging.error("Failed to decode video frame.")
                except Exception as e:
                    # Exception in display_video.
                    logging.exception("Exception in display_video")
        # Handle OpenCV window events
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            # Shutdown requested by user via 'q' key.
            shutdown_flag.set()
            break
        time.sleep(0.01)  # Sleep briefly to prevent high CPU usage.

    cv2.destroyAllWindows()
    # Video display window closed.

def save_words_as_json(words_data, save_path):
    json_path = save_path.replace('.mp4', '.json')
    with open(json_path, 'w') as json_file:
        json.dump(words_data, json_file, indent=4)
    print(f"Word timestamps saved to {json_path}")
    # JSON file saved successfully.

def speech_to_text():
    global speech_recognition_buffer, video_deque
    # Initialize Whisper model for speech recognition.
    model = whisper.load_model("small")  # Use a smaller model to reduce CPU load.
    # Whisper model loaded successfully.

    audio_data = []
    audio_start_time = None  # To track the start time of the current buffer.

    detected_words = deque(maxlen=200)  # To detect the phrase "chat clip that"

    PROCESS_INTERVAL = 1.0  # Process every 1.0 seconds.
    BUFFER_DURATION = 1.0    # Process 1.0-second audio chunks.

    while not shutdown_flag.is_set():
        with audio_lock:
            while speech_recognition_buffer:
                timestamp, data = speech_recognition_buffer.popleft()
                if audio_start_time is None:
                    audio_start_time = timestamp
                audio_data.append(data)

        # Calculate the total duration of collected audio
        total_samples = len(audio_data) * AUDIO_CHUNK
        total_duration = total_samples / AUDIO_RATE

        if total_duration >= BUFFER_DURATION:
            # Sufficient audio data collected for transcription.
            # Concatenate all audio data
            audio_bytes = b''.join(audio_data)
            # Convert bytes to numpy array
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            # Resample to 16000 Hz as required by Whisper
            audio_resampled = librosa.resample(audio_np, orig_sr=AUDIO_RATE, target_sr=16000)
            # Audio data resampled to 16000 Hz.

            # Perform transcription with word timestamps
            try:
                result = model.transcribe(audio_resampled, word_timestamps=True)
            except Exception as e:
                # Transcription failed.
                logging.exception("Exception in speech_to_text during transcription")
                shutdown_flag.set()
                break

            # Store words and their timestamps
            words_data = []

            # Process transcription result
            if 'segments' in result:
                for segment in result['segments']:
                    if 'words' in segment:
                        for word_info in segment['words']:
                            word = word_info['word'].lower()
                            end_time = word_info['end'] + (audio_start_time if audio_start_time else 0)
                            print(f"Recognized word: '{word}' at {end_time} seconds.")
                            # Check for the phrase "chat clip that"
                            print("Processing recognized words...")
                            cleaned_word = re.sub(r"[^a-zA-Z]", "", word)  # Remove non-alphabetic characters
                            if cleaned_word:  # Only append if there's a valid word left
                                detected_words.append(cleaned_word.lower())  # Optionally convert to lowercase

                            print(f"detected_words: {detected_words}")
                            if 'chat' in detected_words and 'clip' in detected_words and 'that' in detected_words:
                                print('Trigger Phrase Detected')
                                # Trigger phrase 'chat clip that' detected.
                                trigger_time = end_time
                                # Calculate the start time for the 30-second video clip
                                clip_start_time = trigger_time - VIDEO_BUFFER_SECONDS
                                if clip_start_time < 0:
                                    clip_start_time = 0

                                # Retrieve video frames within the last 30 seconds
                                frames_to_save = []
                                with video_lock:
                                    for frame_time, frame in video_deque:
                                        relative_time = frame_time - playback_start_time
                                        if clip_start_time <= relative_time <= trigger_time:
                                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                            frames_to_save.append((frame_time, frame_rgb))

                                # Retrieve audio data within the last 30 seconds
                                audio_data_to_save = []
                                with audio_lock:
                                    for audio_time, audio_chunk in audio_deque:
                                        relative_time = audio_time - playback_start_time
                                        if clip_start_time <= relative_time <= trigger_time:
                                            audio_data_to_save.append((audio_time, audio_chunk))

                                if frames_to_save and audio_data_to_save:
                                    # Sort frames and audio data by time
                                    frames_to_save.sort(key=lambda x: x[0])
                                    audio_data_to_save.sort(key=lambda x: x[0])

                                    # Find earliest timestamps
                                    earliest_frame_time = frames_to_save[0][0]
                                    earliest_audio_time = audio_data_to_save[0][0]
                                    earliest_time = min(earliest_frame_time, earliest_audio_time)

                                    # Adjust frame times
                                    frame_times = [ft - earliest_time for ft, _ in frames_to_save]
                                    frames_list = [frame for _, frame in frames_to_save]

                                    # Calculate durations between frames
                                    durations_list = [t2 - t1 for t1, t2 in zip(frame_times[:-1], frame_times[1:])]
                                    # For the last frame, estimate duration based on average
                                    if durations_list:
                                        avg_duration = sum(durations_list) / len(durations_list)
                                    else:
                                        avg_duration = 1.0 / VIDEO_FPS
                                    durations_list.append(avg_duration)

                                    # Create the video clip
                                    video_clip = ImageSequenceClip(frames_list, durations=durations_list)

                                    # Adjust audio data
                                    audio_bytes_concatenated = b''.join([chunk for _, chunk in audio_data_to_save])

                                    # If audio starts after video, pad with silence
                                    if earliest_audio_time > earliest_frame_time:
                                        audio_padding_duration = earliest_audio_time - earliest_frame_time
                                        num_padding_samples = int(audio_padding_duration * AUDIO_RATE)
                                        silence = np.zeros(num_padding_samples, dtype=np.int16)
                                        audio_np_full = np.frombuffer(audio_bytes_concatenated, dtype=np.int16)
                                        audio_np_full = np.concatenate((silence, audio_np_full))
                                    else:
                                        # Trim the audio data if it starts before the video
                                        audio_trim_duration = earliest_frame_time - earliest_audio_time
                                        num_trim_samples = int(audio_trim_duration * AUDIO_RATE)
                                        audio_np_full = np.frombuffer(audio_bytes_concatenated, dtype=np.int16)
                                        audio_np_full = audio_np_full[num_trim_samples:]

                                    # Ensure audio and video durations match
                                    audio_duration = len(audio_np_full) / AUDIO_RATE
                                    video_duration = video_clip.duration
                                    if audio_duration > video_duration:
                                        # Trim the audio
                                        num_samples = int(video_duration * AUDIO_RATE)
                                        audio_np_full = audio_np_full[:num_samples]
                                    elif audio_duration < video_duration:
                                        # Pad the audio
                                        num_padding_samples = int((video_duration - audio_duration) * AUDIO_RATE)
                                        padding = np.zeros(num_padding_samples, dtype=np.int16)
                                        audio_np_full = np.concatenate((audio_np_full, padding))

                                    # Save audio data to a temporary WAV file
                                    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
                                        temp_audio_file_name = temp_audio_file.name
                                        with wave.open(temp_audio_file_name, 'wb') as wf:
                                            wf.setnchannels(AUDIO_CHANNELS)
                                            wf.setsampwidth(sample_width)
                                            wf.setframerate(AUDIO_RATE)
                                            wf.writeframes(audio_np_full.astype(np.int16).tobytes())

                                    # Create AudioFileClip from the temporary WAV file
                                    audio_clip = AudioFileClip(temp_audio_file_name)

                                    # Combine audio and video
                                    video_with_audio = video_clip.set_audio(audio_clip)

                                    # Save the final video
                                    #timestamp_str = time.strftime("%Y%m%d-%H%M%S")
                                    final_save_path = os.path.join(SAVE_DIR, f"final_clip.mp4")
                                    video_with_audio.write_videofile(final_save_path, codec='libx264', audio_codec='aac', fps=VIDEO_FPS)

                                    # Remove the temporary audio file
                                    os.remove(temp_audio_file_name)

                                    detected_words.clear()
                                    print(f"Video clip saved to {final_save_path}")

                                    # Re-run speech recognition on the audio data of the clip
                                    # Load audio data
                                    audio_np_resampled = librosa.resample(audio_np_full.astype(np.float32) / 32768.0, orig_sr=AUDIO_RATE, target_sr=16000)
                                    # Perform transcription with word timestamps
                                    try:
                                        result_clip = model.transcribe(audio_np_resampled, word_timestamps=True)
                                    except Exception as e:
                                        # Transcription failed.
                                        logging.exception("Exception in speech_to_text during clip transcription")
                                        shutdown_flag.set()
                                        break

                                    # Store words and their timestamps
                                    words_data = []

                                    # Process transcription result
                                    if 'segments' in result_clip:
                                        for segment in result_clip['segments']:
                                            if 'words' in segment:
                                                for word_info in segment['words']:
                                                    word = word_info['word']
                                                    # Adjust timestamp to be relative to the clip
                                                    end_time = word_info['end']
                                                    words_data.append({"word": word, "timestamp": end_time})

                                    # Save the words data as a JSON file alongside the video clip
                                    save_words_as_json(words_data, final_save_path)
                                    # Word timestamps saved to JSON file.
                                    start_editing()
                                else:
                                    # No video frames or audio data found for the specified time range.
                                    logging.warning("No video frames or audio data found for the specified time range.")
                                    pass
            # Reset audio data
            audio_data = []
            audio_start_time = None

        time.sleep(PROCESS_INTERVAL)  # Adjust the sleep time as needed

def main():
    global playback_start_time
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        # Server socket bound to {SERVER_IP}:{SERVER_PORT}.
    except Exception as e:
        # Failed to bind server socket.
        logging.exception("Failed to bind server socket")
        sys.exit()

    server_socket.listen(5)
    # Server listening on {SERVER_IP}:{SERVER_PORT}

    try:
        conn, addr = server_socket.accept()
        # Connected by {addr}
    except KeyboardInterrupt:
        # Server shutdown requested by user.
        server_socket.close()
        sys.exit()

    # Event to signal that playback_start_time has been set
    playback_start_time_event = threading.Event()

    # Start thread to receive data
    recv_thread = threading.Thread(target=receive_stream, args=(conn, playback_start_time_event), daemon=True)
    recv_thread.start()
    # Data receiving thread started.

    # Start speech recognition thread
    speech_thread = threading.Thread(target=speech_to_text, daemon=True)
    speech_thread.start()
    # Speech recognition thread started.

    # Wait until playback_start_time is set
    playback_start_time_event.wait()
    # Playback start time event set. Starting playback and video display.

    # Start thread to play audio
    audio_thread = threading.Thread(target=play_audio, daemon=True)
    audio_thread.start()
    # Audio playback thread started.

    # Run display_video on the main thread
    try:
        display_video()
    except KeyboardInterrupt:
        # Shutdown requested by user via KeyboardInterrupt.
        shutdown_flag.set()

    # Cleanup
    recv_thread.join()
    speech_thread.join()
    audio_thread.join()
    server_socket.close()
    cv2.destroyAllWindows()
    # Server shutdown complete.

if __name__ == "__main__":
    main()
