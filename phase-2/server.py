import sys
import threading
import socket
import json
import struct


class Server(threading.Thread):
    def __init__(self, port):
        self.host = '' #this may change.
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        threading.Thread.__init__(self)

    def start(self):
        self.socket.listen(1)
        print(f"Server listening on port {self.port}")
        while True:
            agent_conn, agent_addr = self.socket.accept()

            #now agent is being returned:
            agent_thread = Agent(agent_conn, agent_addr)
            agent_thread.start()


#This is the Agent = Client implementation but not "client" in pdf
class Agent(threading.Thread):
    def __init__(self,connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        print(f"Connection established with {self.address}")
        try:
            while True:
                # Read the size of the command -- an binary encoded int
                raw_size = self.connection.recv(4)
                if not raw_size:
                    break
                size = struct.unpack('!I', raw_size)[0]

                # Read the command
                raw_command = self.connection.recv(size)
                command = raw_command.decode()

                # Process command
                response = self.process_command(command)
                self.connection.sendall(response.encode())
        finally:
            self.connection.close()
            print(f"Connection closed with {self.address}")
    
    #in here make corresponding library calls:
    def process_command(self, command):
        # Implement command processing logic 
        # this is a mock one:

        if command.startswith('{') and command.endswith('}'):
            # Process JSON command
            command_data = json.loads(command)
            return json.dumps({"response": "Processed JSON command"})
        else:
            # Process simple text command
            command_data = command.split()
            return "Processed text command"


#controlling if the arguments are true or not
#if true, take the port number
if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != '--port':
        print("Usage: python3 yourapp.py --port <port_number>")
        sys.exit(1)

    port = int(sys.argv[2])
    server = Server(port)
    server.start()