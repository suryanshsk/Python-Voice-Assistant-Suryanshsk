import socket
import pyaudio
import threading
import sys
import logging
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

clients = set()
is_running = True
lock = threading.Lock()
cipher = Fernet(Fernet.generate_key())

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

def handle_client(sock):
    while is_running:
        try:
            data, addr = sock.recvfrom(CHUNK)
            if addr in clients:
                decrypted_data = cipher.decrypt(data)
                with lock:
                    for client in clients:
                        if client != addr:
                            sock.sendto(decrypted_data, client)
        except Exception as e:
            logging.error(f"Error in handling client: {e}")

def record_audio(sock):
    stream = pyaudio.PyAudio().open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while is_running:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            encrypted_data = cipher.encrypt(data)
            sock.sendto(encrypted_data, (UDP_IP, UDP_PORT))
        except Exception as e:
            logging.error(f"Error in recording audio: {e}")

def play_audio(sock):
    stream = pyaudio.PyAudio().open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    while is_running:
        try:
            data, _ = sock.recvfrom(CHUNK)
            stream.write(data)
        except Exception as e:
            logging.error(f"Error in playback: {e}")

def main():
    global is_running

    local_ip = get_local_ip()
    logging.info(f"Local IP Address: {local_ip}")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    threading.Thread(target=handle_client, args=(sock,), daemon=True).start()

    logging.info("Voice communication app started. Type 'join <username>' to connect and 'leave' to disconnect.")

    while is_running:
        command = input().strip().lower()
        if command.startswith("join"):
            username = command.split(" ")[1] if len(command.split(" ")) > 1 else None
            if username:
                with lock:
                    clients.add(sock.getsockname())
                    logging.info(f"{username} joined the communication.")
                    threading.Thread(target=record_audio, args=(sock,), daemon=True).start()
                    threading.Thread(target=play_audio, args=(sock,), daemon=True).start()
            else:
                logging.warning("Please provide a username.")
        elif command == "leave":
            with lock:
                clients.remove(sock.getsockname())
                logging.info("Left the communication.")
                if not clients:
                    logging.info("No clients connected. Stopping...")
                    is_running = False
        elif command == "exit":
            confirmation = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if confirmation == 'y':
                is_running = False
                logging.info("Exiting the application...")
        else:
            logging.warning("Invalid command. Type 'join <username>', 'leave', or 'exit'.")

    sock.close()
    pyaudio.PyAudio().terminate()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        is_running = False
        logging.info("Application interrupted. Exiting...")