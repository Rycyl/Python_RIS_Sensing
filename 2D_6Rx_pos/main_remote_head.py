import sockets
from remote_head import Remote_Head
from config_obj import Config

if __name__ == "__main__":

    ip_server = '192.168.8.0'  # Server address
    port = 13245
    config = Config()
    RH = Remote_Head(config)
    
    socket = sockets.server_open_socket(ip_server, port)
    
    while True:
        command = sockets.server_get_command(socket)
        RH.steering_command(command=command)

    close_socket(socket)
