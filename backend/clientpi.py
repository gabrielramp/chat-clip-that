import socket
import threading
import time
import struct
import cv2
import pyaudio
import numpy as np
from picamera2 import Picamera2

# Server configuration
SERVER_IP = '6.tcp.ngrok.io'  # Replace with your server's IP address
SERVER_PORT = 11666

# Audio configuration
AUDIO_RATE = 44100
AUDIO_CHANNELS = 1
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHUNK = 1024

# Video configuration
VIDEO_FPS = 20.0

def send_video(sock, start_time, stop_event, sock_lock):
    # Initialize Picamera2
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (640, 480)})
    picam2.configure(video_config)
    picam2.start()
    time.sleep(1)  # Allow the camera to warm up

    while not stop_event.is_set():
        frame = picam2.capture_array()
        if frame is None:
            print("Cannot receive frame")
            continue

        # Convert to BGR (Picamera2 uses RGB by default)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Encode frame as JPEG
        result, encoded_image = cv2.imencode('.jpg', frame)
        if not result:
            print("Could not encode frame")
            continue

        # Get timestamp
        timestamp = time.time() - start_time

        # Create packet
        packet_type = b'V'
        payload = encoded_image.tobytes()
        size = len(payload)
        header = packet_type + struct.pack('!I', size) + struct.pack('!d', timestamp)
        packet = header + payload

        # Send packet
        with sock_lock:
            try:
                sock.sendall(packet)
            except Exception as e:
                print(f"Error sending video packet: {e}")
                stop_event.set()
                break

        # Wait to maintain frame rate
        time.sleep(1.0 / VIDEO_FPS)

    picam2.stop()

def audio_stream(sock, start_time, sock_lock):
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
        packet = b'A' + struct.pack('!I', len(data)) + struct.pack('!d', timestamp) + data
        with sock_lock:
            try:
                sock.sendall(packet)
            except BrokenPipeError:
                print("Connection closed by server")
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

def main():
    # Connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
    except Exception as e:
        print(f"Could not connect to server: {e}")
        return

    start_time = time.time()
    stop_event = threading.Event()
    sock_lock = threading.Lock()

    # Start threads for video and audio
    video_thread = threading.Thread(target=send_video, args=(sock, start_time, stop_event, sock_lock))
    audio_thread = threading.Thread(target=audio_stream, args=(sock, start_time, sock_lock))

    video_thread.start()
    audio_thread.start()

    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user")
        stop_event.set()
    finally:
        video_thread.join()
        audio_thread.join()
        sock.close()
        print("Connection closed")

if __name__ == '__main__':
    main()