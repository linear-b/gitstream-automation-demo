import socket
import threading
import sys

#Wait for incoming data from server
#.decode is used to turn the message in bytes to a string
def receive(socket, stop_event):
    while True:
        if stop_event.is_set():
            break
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
            print("You have been disconnected from the server. Error: " + e.strerror)
            break

#Get host and port
host = input("Host: ")
port = int(input("Port: "))

#Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except (socket.error, ConnectionRefusedError) as e:
    print("Could not make a connection to the server. Error: " + e.strerror)
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
