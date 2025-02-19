import socket
import sys
import threading

# Variables for holding information about connections
connections = []
total_connections = 0
_connections_lock = threading.Lock()

# Client class, new instance created for each connected client
# Each instance has the socket and address that is associated with items
# Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address) + " " + self.name
    
    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server and send it back to every
    # client aside from the client that has sent it
    # .decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            try:
                data = b''
                while True:
                    chunk = self.socket.recv(4096)
                    data += chunk
                    if len(chunk) < 4096:
                        break
            except (socket.error, ConnectionResetError) as e:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                with _connections_lock:
                    connections.remove(self)
                break
            if data != b"":
                print("ID " + str(self.id) + ": " + str(data.decode('utf-8')))
                with _connections_lock:
                    for client in connections:
                        if client.id != self.id:
                            client.socket.sendall(data)

# Wait for new connections
def newConnections(socket):
    global total_connections
    while True:
        try:
            sock, address = socket.accept()
            name = sock.recv(1024).decode('utf-8')  # Receive the name from the client
            client = Client(sock, address, total_connections, name, True)
            with _connections_lock:
                connections.append(client)
                total_connections += 1
            client.start()
            print("New connection at ID " + str(client))
        except (socket.error, ConnectionError) as e:
            print(f"Error accepting connection: {e}")
            continue

def main():
    # Get host and port
    host = input("Host: ")
    if not host:
        host = "localhost"
    try:
        port = int(input("Port: "))
        if not (1024 <= port <= 65535):
            raise ValueError("Port must be between 1024 and 65535")
    except ValueError as e:
        print(f"Invalid port: {e}")
        sys.exit(1)

    # Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        sock.listen(5)
        sock.settimeout(60)  # 60 second timeout
    except socket.error as e:
        print(f"Failed to bind socket: {e}")
        sys.exit(1)

    # Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target=newConnections, args=(sock,))
    newConnectionsThread.start()
    try:
        stop_event = threading.Event()
        stop_event.wait()  # Wait indefinitely until KeyboardInterrupt
    except KeyboardInterrupt:
        print("\nShutting down server...")
        # Signal all clients to stop
        with _connections_lock:
            for client in connections:
                client.signal = False
                client.socket.close()
                client.join()
        sock.close()

if __name__ == "__main__":
    main()