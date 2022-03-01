# requires python 3.6 and above
# simply echo back what it received on the port
# client can test via telnet or echo_client.py

import socket

# HOST = "127.0.0.1"  # Standard loopback interface address 
HOST = "" # empty string allow all IP addresses
PORT = 30000  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)