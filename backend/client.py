import socket
import threading
import cv2
import pyaudio
import struct
import time
import sys

# Configuration
SERVER_IP = 'localhost'  # Replace with your server's IP
SERVER_PORT = 9999

# Video Configuration
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
VIDEO_FPS = 20.0

# Audio Configuration
AUDIO_RATE = 44100
AUDIO_CHANNELS = 1
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHUNK = 1024

def video_stream(conn, start_time):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, VIDEO_FPS)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture video frame")
                break

            # Encode frame as JPEG
            encoded, buffer = cv2.imencode('.jpg', frame)
            if not encoded:
                print("Failed to encode frame")
                continue

            data = buffer.tobytes()
            # Compute relative timestamp
            timestamp = time.time() - start_time
            # Prepare packet with header
            # Packet structure: [TYPE][SIZE][TIMESTAMP][DATA]
            # TYPE: b'V' for video
            # SIZE: 4 bytes unsigned int
            # TIMESTAMP: 8 bytes double
            packet = b'V' + struct.pack('!I', len(data)) + struct.pack('!d', timestamp) + data
            try:
                conn.sendall(packet)
            except (BrokenPipeError, OSError) as e:
                print(f"Connection error in video_stream: {e}")
                break

            # Control frame rate
            time.sleep(1 / VIDEO_FPS)
    except Exception as e:
        print(f"Exception in video_stream: {e}")
    finally:
        cap.release()

def audio_stream(conn, start_time):
    p = pyaudio.PyAudio()
    stream = p.open(format=AUDIO_FORMAT,
                    channels=AUDIO_CHANNELS,
                    rate=AUDIO_RATE,
                    input=True,
                    frames_per_buffer=AUDIO_CHUNK)

    try:
        while True:
            try:
                data = stream.read(AUDIO_CHUNK, exception_on_overflow=False)
            except IOError as e:
                print(f"Error reading audio stream: {e}")
                break

            # Compute relative timestamp
            timestamp = time.time() - start_time
            # Prepare packet with header
            # Packet structure: [TYPE][SIZE][TIMESTAMP][DATA]
            # TYPE: b'A' for audio
            # SIZE: 4 bytes unsigned int
            # TIMESTAMP: 8 bytes double
            packet = b'A' + struct.pack('!I', len(data)) + struct.pack('!d', timestamp) + data
            try:
                conn.sendall(packet)
            except (BrokenPipeError, OSError) as e:
                print(f"Connection error in audio_stream: {e}")
                break

    except Exception as e:
        print(f"Exception in audio_stream: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def main():
    while True:
        # Create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((SERVER_IP, SERVER_PORT))
            print("Connected to server. Starting streams...")
        except Exception as e:
            print(f"Unable to connect to server: {e}")
            client_socket.close()
            print("Retrying in 10 seconds...")
            time.sleep(10)
            continue  # Retry connection

        # Record the start time
        start_time = time.time()

        # Start video and audio threads, pass start_time
        video_thread = threading.Thread(target=video_stream, args=(client_socket, start_time))
        audio_thread = threading.Thread(target=audio_stream, args=(client_socket, start_time))
        video_thread.start()
        audio_thread.start()

        try:
            # Keep main thread alive while threads are running
            while video_thread.is_alive() and audio_thread.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user. Closing connection.")
            try:
                client_socket.close()
            except Exception as e:
                print(f"Error closing socket: {e}")
            sys.exit()
        except Exception as e:
            print(f"Exception in main thread: {e}")
            try:
                client_socket.close()
            except Exception as e2:
                print(f"Error closing socket: {e2}")
            print("Retrying in 10 seconds...")
            time.sleep(10)
            continue

        # If threads have exited, close socket and retry connection
        print("Connection lost. Retrying in 10 seconds...")
        try:
            client_socket.close()
        except Exception as e:
            print(f"Error closing socket: {e}")
        time.sleep(10)

if __name__ == "__main__":
    main()
