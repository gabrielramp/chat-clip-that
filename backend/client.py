import socket
import threading
import cv2
import pyaudio
import struct
import time
import sys

# Configuration
SERVER_IP = '6.tcp.ngrok.io'  # Replace with your server's IP
SERVER_PORT = 11666

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
        except BrokenPipeError:
            print("Connection closed by server")
            break

        # Control frame rate
        time.sleep(1 / VIDEO_FPS)

    cap.release()

def audio_stream(conn, start_time):
    p = pyaudio.PyAudio()
    stream = p.open(format=AUDIO_FORMAT,
                    channels=AUDIO_CHANNELS,
                    rate=AUDIO_RATE,
                    input=True,
                    frames_per_buffer=AUDIO_CHUNK)

    while True:
        try:
            data = stream.read(AUDIO_CHUNK)
        except IOError:
            print("Error reading audio stream")
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
        except BrokenPipeError:
            print("Connection closed by server")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

def main():
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
    except Exception as e:
        print(f"Unable to connect to server: {e}")
        sys.exit()

    print("Connected to server. Starting streams...")

    # Record the start time
    start_time = time.time()

    # Start video and audio threads, pass start_time
    video_thread = threading.Thread(target=video_stream, args=(client_socket, start_time))
    audio_thread = threading.Thread(target=audio_stream, args=(client_socket, start_time))
    video_thread.start()
    audio_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user. Closing connection.")
        client_socket.close()
        sys.exit()

if __name__ == "__main__":
    main()
