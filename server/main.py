import socket
import time

HOST = '127.0.0.1'
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on port {PORT}...")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                if message == "stop":
                    print("Received stop message. Stopping machine...")
                    break
                else:
                    print(f"Received unknown message: {message}")

while True:
    main()
    time.sleep(1)
