import socket

def server_open_socket(IP = '192.168.8.0', PORT = 13245):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    return server_socket

def server_get_command(server_socket):

    # Enable the server to accept connections (max clients in queue)
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    
    # Establish a connection with the client
    client_socket, addr = server_socket.accept()
    print(f"Got a connection from {addr}")

    # Receive data from the client
    data = client_socket.recv(1024).decode()
    print(f"Received from client: {data}")

    # Send a response back to the client
    response = (f"ack: {data}")
    client_socket.send(response.encode())
    return(data)

def client_open_socket(IP = "192.168.8.XXX", PORT = 13245):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

def client_send_message(client_socket, message=' '):
    client_socket.send(message.encode())
    print("Send message:: " + message)

    response = client_socket.recv(1024).decode()
    print(f"Received from server: {response}")


def close_socket(socket):
    socket.close()
