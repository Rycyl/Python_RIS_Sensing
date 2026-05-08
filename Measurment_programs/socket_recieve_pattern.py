
import socket
import threading
from RIS import RIS
from config_obj import Config

class RISSocketServer:
    def __init__(self, RIS, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.running = False
        self.RIS_device = RIS

    def start(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        print(f"RIS Socket Server listening on {self.host}:{self.port}")

        while self.running:
            conn, addr = self.server_socket.accept()
            print(f"Client connected from {addr}")

            client_thread = threading.Thread(
                target=self.handle_client,
                args=(conn, addr),
                daemon=True
            )
            client_thread.start()

    def handle_client(self, conn, addr):
        with conn:
            buffer = ""
            while self.running:
                try:
                    data = conn.recv(1024)
                    if not data:
                        print(f"Client {addr} disconnected")
                        break

                    buffer += data.decode("utf-8")

                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip()

                        if not line:
                            continue

                        print(f"Received command: {line}")

                        # --- Tu można dodać realną obsługę RIS ---
                        if line.startswith("!"):
                            pattern = line[1:]
                            self.process_pattern(pattern)
                            conn.sendall(b"#OK\n")
                        else:
                            conn.sendall(b"#ERR\n")

                except socket.error as e:
                    print(f"Socket error with {addr}: {e}")
                    break

    def process_pattern(self, pattern):
        print(f"Setting RIS pattern: {pattern}")
        i = 0
        while i<3:
            done = self.RIS_device.set_pattern(pattern)
            if done:
                return True
            else:
                i+=1

    def stop(self):
        self.running = False
        try:
            self.server_socket.close()
        except Exception:
            pass


# --------------------------------------------------
# START SERWERA
# --------------------------------------------------

if __name__ == "__main__":
    conf = Config()
    ris = RIS(port="/dev/ttyUSB0", use_socket=False)
    server = RISSocketServer(RIS=ris, host="0.0.0.0", port=5000)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop()