import socket
import threading
import struct
import argparse

class ClientHandler(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
    
    def run(self):
        with self.client_socket:
            while True:
                command = self.read_command()
                if not command: 
                    break
                response = self.process_command(command)
                self.client_socket.sendall(response.encode())
    
    def read_command(self):
        try: 
            size_data = self.client_socket.recv(4)
            if not size_data:
                return None
            size = struct.unpack('!I', size_data)[0]
            command_data = self.client_socket.recv(size)
            return command_data.decode()
        except Exception as e:
            print(f"Error reading command: {e}")
            return None
    
    def process_command(self, command):
        # Implement command processing logic
        print(f"Processing command: {command}")
        return "Command processed"


class Server:
    def __init__(self, port):
        self.host = ''
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on port {self.port}")
        
    def start(self):
        try:
            while True:
                client_socket, client_addr = self.socket.accept()
                print(f"Connection from {client_addr}")
                client_handler = ClientHandler(client_socket)
                client_handler.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.socket.close()


# Parsing command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="TCP server application")
    parser.add_argument("--port", type=int, required=True, help="TCP port to listen on")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    tcp_server = Server(args.port)
    tcp_server.start()