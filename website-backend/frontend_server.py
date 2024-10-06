import socket
import threading
import subprocess
import sys
import os
import struct
import logging
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Configuration
SERVER_IP = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 8888     # Port to receive data from the server

# HLS Configuration
HLS_OUTPUT_DIR = './hls_stream'
os.makedirs(HLS_OUTPUT_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)

def start_ffmpeg_process():
    ffmpeg_command = [
        'ffmpeg',
        '-y',  # Overwrite output files
        '-f', 'image2pipe',
        '-vcodec', 'mjpeg',
        '-r', '20',  # Frame rate
        '-i', '-',   # Input comes from stdin
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-g', '50',
        '-f', 'hls',
        '-hls_time', '1',
        '-hls_list_size', '5',
        '-hls_flags', 'delete_segments',
        os.path.join(HLS_OUTPUT_DIR, 'stream.m3u8')
    ]

    logging.info("Starting FFmpeg process...")
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)
    return ffmpeg_process

def handle_client_connection(client_socket, ffmpeg_process):
    buffer = b''
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            buffer += data

            while True:
                if len(buffer) < 5:
                    break
                packet_type = buffer[0:1]
                size = struct.unpack('!I', buffer[1:5])[0]
                if len(buffer) < 5 + size:
                    break
                payload = buffer[5:5 + size]
                buffer = buffer[5 + size:]

                if packet_type == b'V':
                    # Write frame to FFmpeg stdin
                    ffmpeg_process.stdin.write(payload)
                else:
                    # Handle other packet types if necessary
                    pass
        except Exception as e:
            logging.exception("Exception in handle_client_connection")
            break

    client_socket.close()
    logging.info("Client connection closed.")

# Custom HTTP request handler to add CORS headers
class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        # Allow Range header for video streaming
        self.send_header('Access-Control-Allow-Headers', 'Range')
        # Expose the Accept-Ranges header to the client
        self.send_header('Access-Control-Expose-Headers', 'Content-Length, Content-Range, Accept-Ranges')
        SimpleHTTPRequestHandler.end_headers(self)

def start_http_server():
    os.chdir(HLS_OUTPUT_DIR)
    server_address = ('', 8000)  # Serve on all interfaces, port 8000
    httpd = HTTPServer(server_address, CORSRequestHandler)
    logging.info("Starting HTTP server on port 8000...")
    httpd.serve_forever()

def main():
    # Start FFmpeg process
    ffmpeg_process = start_ffmpeg_process()

    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    # Create socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        logging.info(f"Frontend-server listening on {SERVER_IP}:{SERVER_PORT}")
    except Exception as e:
        logging.exception("Failed to bind frontend-server socket")
        sys.exit()

    server_socket.listen(5)

    while True:
        try:
            client_sock, addr = server_socket.accept()
            logging.info(f"Accepted connection from {addr}")
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_sock, ffmpeg_process),
                daemon=True
            )
            client_handler.start()
        except KeyboardInterrupt:
            logging.info("Shutting down frontend-server...")
            ffmpeg_process.stdin.close()
            ffmpeg_process.wait()
            server_socket.close()
            sys.exit()

if __name__ == "__main__":
    main()
