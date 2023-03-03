import socket
import selectors
import types
import random

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

sel = selectors.DefaultSelector()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print(f"Listening on {(HOST, PORT)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

numberlist = []

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", random_number=random.randint(1, 100), num_sent=0)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    numberlist.append(conn)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)  # Should be ready to read
        except:
            recv_data = None

        if recv_data:
            data.num_sent += 1
            if data.num_sent > 15:
                sock.send(b"You lose!")
                numberlist.remove(sock)
                sel.unregister(sock)
                sock.close()
                return
            # Check if the received number matches the random number
            if int(recv_data.strip()) < data.random_number:
                sock.send(b"too little!")
            elif int(recv_data.strip()) > data.random_number:
                sock.send(b"too much!")
            else:
                # Send the number of times the client sent the number
                response = f"You win! You guessed it in {data.num_sent} tries.".encode()
                sock.send(response)
                numberlist.remove(sock)
                sel.unregister(sock)
                sock.close()
        else:
            numberlist.remove(sock)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            for _sock in numberlist:
                if _sock != sock:
                    _sock.send(str(data.random_number).encode())
            data.outb = b''

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
