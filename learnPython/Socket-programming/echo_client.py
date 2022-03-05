# requires python 3.6 and above
import socket

HOST = input("remote server hostname: ")
PORT = 30000
text_to_send = ''' \n From: echo client -
If it is a string, you must also give the encoding (and optionally, errors) parameters;
bytearray() then converts the string to bytes using str.encode().'''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(str.encode(text_to_send)) # won't send string
    data = s.recv(1024)

print(f"Received {data!r}")