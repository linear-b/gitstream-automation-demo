import socket
import threading
import sys

# Wait for incoming data from server
# .decode is used to turn the message in bytes to a string
def receive(socket, stop_event):
    while not stop_event.is_set():
        try:
            data = b''
            while True:
                chunk = socket.recv(4096)
                data += chunk
                if len(chunk) < 4096:
                    break
            if data:
                print(str(data.decode('utf-8')))
        except (socket.error, ConnectionResetError) as e:
            print("You have been disconnected from the server. Error: " + str(e))
            connected = False
            break

# Get host and port
host = input("Host: ")
port = int(input("Port: "))
name = input("Enter your name: ")

# Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(str.encode(name))  # Send the name to the server
except (socket.error, ConnectionRefusedError) as e:
    print("Could not make a connection to the server. Error: " + str(e))
    input("Press enter to quit")
    sys.exit(0)

# Create new thread to wait for data
stop_event = threading.Event()
receiveThread = threading.Thread(target=receive, args=(sock, stop_event))
receiveThread.start()

# Send data to server
# str.encode is used to turn the string message into bytes so it can be sent across the network
# Setup clean exit
try:
    while True:
        message = input()
        if not message:  # Allow clean exit on empty input
            break
        sock.sendall(str.encode(message))
except (socket.error, ConnectionResetError) as e:    
    print(f"Connection error: {e}")
finally:
    print("Closing connection...")
    stop_event.set()  # Signal receive thread to stop
    sock.close()
    receiveThread.join()
