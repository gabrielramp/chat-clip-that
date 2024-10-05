import socket
import threading
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

# Playback start time
playback_start_time = None

# Flag to control the shutdown of threads
shutdown_flag = threading.Event()

# Directory to save video clips
SAVE_DIR = './just-saved'
os.makedirs(SAVE_DIR, exist_ok=True)

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
                        # Audio packet buffered.
                    # Also append to speech_recognition_buffer
                    with audio_lock:
                        speech_recognition_buffer.append((timestamp, payload))
                        # Audio data appended to speech recognition buffer.
                else:
                    # Unknown packet type.
                    pass

        except ConnectionResetError:
            # Connection reset by peer.
            shutdown_flag.set()
            break
        except Exception as e:
            # Error receiving data.
            shutdown_flag.set()
            break

    conn.close()
    # Connection closed.

def play_audio():
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=AUDIO_FORMAT,
                        channels=AUDIO_CHANNELS,
                        rate=AUDIO_RATE,
                        output=True,
                        frames_per_buffer=AUDIO_CHUNK)
        # Audio stream opened successfully.
    except Exception as e:
        # Failed to open audio stream.
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
                except Exception as e:
                    # Error writing audio data.
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
                        pass
                except Exception as e:
                    # Exception in display_video.
                    pass

        # Handle OpenCV window events
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            # Shutdown requested by user via 'q' key.
            shutdown_flag.set()
            break
        time.sleep(0.001)  # Sleep briefly to prevent high CPU usage.

    cv2.destroyAllWindows()
    # Video display window closed.

def are_words_close(words, target_words, max_distance):
    # Find the indices of the target words in the list
    indices = {word: [] for word in target_words}
    for i, word in enumerate(words):
        if word in target_words:
            indices[word].append(i)
    
    # Check if all target words were found
    if not all(indices[word] for word in target_words):
        return False

    # Find the minimum and maximum index for the found words
    all_indices = []
    for word in target_words:
        all_indices.extend(indices[word])

    min_index = min(all_indices)
    max_index = max(all_indices)

    # Return whether the words are within the max_distance of each other
    print((max_index - min_index) <= max_distance)
    return (max_index - min_index) <= max_distance


import json

# Helper function to save words and timestamps to a JSON file
def save_words_as_json(words_data, save_path):
    json_path = save_path.replace('.avi', '.json')
    with open(json_path, 'w') as json_file:
        json.dump(words_data, json_file, indent=4)
    print(f"Word timestamps saved to {json_path}")
    # JSON file saved successfully.

def speech_to_text():
    global speech_recognition_buffer, video_deque
    # Initialize Whisper model for speech recognition.
    model = whisper.load_model("large")  # Use the most accurate model available.
    # Whisper model loaded successfully.

    audio_data = []
    audio_start_time = None  # To track the start time of the current buffer.

    detected_words = deque(maxlen=200)  # To detect the phrase "chat clip that"

    PROCESS_INTERVAL = 0.5  # Process every 0.5 seconds.
    BUFFER_DURATION = 0.5    # Process 0.5-second audio chunks.

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
                                words_data.append({"word": cleaned_word, "timestamp": end_time})

                            print(f"detected_words: {detected_words}")
                            if detected_words.__contains__('chat') and detected_words.__contains__('clip') and detected_words.__contains__('that'):
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
                                            frames_to_save.append((frame_time, frame))

                                if frames_to_save:
                                    # Sort frames by time
                                    frames_to_save.sort(key=lambda x: x[0])
                                    # Save frames as a video file
                                    timestamp_str = time.strftime("%Y%m%d-%H%M%S")
                                    save_path = os.path.join(SAVE_DIR, f"clip_{timestamp_str}.avi")
                                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                                    out = cv2.VideoWriter(save_path, fourcc, VIDEO_FPS, (640, 480))

                                    for _, frame in frames_to_save:
                                        out.write(frame)
                                    out.release()
                                    detected_words = []
                                    print(f"Video clip saved to {save_path}")

                                    # Save the words data as a JSON file alongside the video clip
                                    save_words_as_json(words_data, save_path)
                                    # Word timestamps saved to JSON file.
                                else:
                                    # No video frames found for the specified time range.
                                    pass

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