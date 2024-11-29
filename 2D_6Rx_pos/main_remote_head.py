import sockets
from remote_head import Remote_Head
from config_obj import Config

if __name__ == "__main__":

    ip_server = '192.168.8.104'  # Server address
    port = 13245
    config = Config()
    RH = Remote_Head(config)
    
    socket = sockets.server_open_socket(ip_server, port)
    client_socket = sockets.server_listen(socket)

    while True:
        command = sockets.server_data_recv(client_socket)
        RH.steering_command(command=command)
        sockets.send_ack(client_socket=client_socket, data=command)

    close_socket(socket)
