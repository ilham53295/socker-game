import socket
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        number = input("Enter a number (or 'quit' to exit): ")
        if number == 'quit':
            break
        s.sendall(number.encode())
        data = s.recv(1024)
        print(f"Received {data.decode()}")
        if data.decode() == "You win!":
            break
        if data.decode() == "You lose!":
            break
