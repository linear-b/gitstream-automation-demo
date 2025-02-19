import socket
import threading
import sys

#Wait for incoming data from server
#.decode is used to turn the message in bytes to a string
def receive(socket, stop_event):
    while True:
        if stop_event.is_set():
            break
        socket.settimeout(1.0)  # 1 second timeout
        try:
            data = b''
            while True:
                chunk = socket.recv(4096)
                data += chunk
                if len(chunk) < 4096:
                    break
            if data:
                print(str(data.decode('utf-8')))
        except (socket.error, ConnectionResetError, socket.timeout) as e:
            print(f"You have been disconnected from the server. Error: {str(e)}")
            stop_event.set()
            break

#Get host and port
host = input("Host: ")
try:
    port = int(input("Port: "))
    if not (1024 <= port <= 65535):
        raise ValueError("Port must be between 1024 and 65535")
except ValueError as e:
    print(f"Invalid port: {str(e)}")
    sys.exit(1)

#Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except (socket.error, ConnectionRefusedError) as e:
    print(f"Could not make a connection to the server. Error: {str(e)}")
    input("Press enter to quit")
    sys.exit(0)

#Create new thread to wait for data
stop_event = threading.Event()
receiveThread = threading.Thread(target = receive, args = (sock, stop_event))
receiveThread.start()

#Send data to server
#str.encode is used to turn the string message into bytes so it can be sent across the network
# Setup clean exit
try:
    while True:
        message = input()
        sock.sendall(str.encode(message))
finally:
    stop_event.set()
    sock.close()
    receiveThread.join()
