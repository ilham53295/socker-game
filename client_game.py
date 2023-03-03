import socket
import re

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        number = input("Enter a number (or 'quit' to exit): ")
        if number == 'quit' or number == 'exit':
            break
        try:
            num = int(number)
            if num < 1 or num > 100:
                print("Number must be between 1 and 100.")
                continue
        except ValueError:
            print("Invalid input! Only numbers are allowed.")
            continue
        s.sendall(number.encode())
        data = s.recv(1024)
        response = data.decode()
        print(f"Received {response}")
        if response.startswith("You win!"):
            break
        elif response == "You lose!":
            break