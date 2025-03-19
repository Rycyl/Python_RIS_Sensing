import socket

def get_local_ip():
    hostname = socket.gethostname()  # Get the hostname of the machine
    local_ip = socket.gethostbyname(hostname)  # Get the local IP address
    return local_ip

def server_open_socket(IP='192.168.0.0', PORT=11119):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    return server_socket

def server_get_command(server_socket):
    # Enable the server to accept connections (max clients in queue)
    server_socket.listen(5)
    print(f"Server listening on {server_socket.getsockname()}")
    
    # Establish a connection with the client
    client_socket, addr = server_socket.accept()
    print(f"Got a connection from {addr}")

    # Receive data from the client
    data = client_socket.recv(1024).decode()
    print(f"Received from client: {data}")
    return data, client_socket

def send_ack(client_socket, data):
    # Send a response back to the client
    response = f"ack: {data}"
    client_socket.send(response.encode())

def client_open_socket(IP="192.168.8.XXX", PORT=11119):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))  # Connect to the server
    return client_socket

def client_send_message(client_socket, message=' '):
    client_socket.send(message.encode())
    print("Send message:: " + message)
    
    # Receive response from the server
    response = client_socket.recv(1024).decode()
    print(f"Received from server: {response}")

def close_socket(socket):
    socket.close()

# Example usage
def main():
    # Start the server
    server_socket = server_open_socket()
    # In a real application, you would run this in a separate thread or process
    server_get_command(server_socket)

    # Start the client
    client_socket = client_open_socket()  # Connect to the server
    client_send_message(client_socket, message="Hello, Server!")

    # Close sockets
    close_socket(client_socket)
    close_socket(server_socket)

if __name__ == "__main__":
    main()
