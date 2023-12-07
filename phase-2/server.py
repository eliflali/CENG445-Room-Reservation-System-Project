import sys
import threading
import socket
import json
import struct
from users import login

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
        try:
            # First, parse the received command as JSON
            wrapped_command = json.loads(command)

            # Check if the 'command' key exists
            if 'command' in wrapped_command:
                # Extract the command
                actual_command_str = wrapped_command['command']

                # Parse the actual command as JSON
                actual_command = json.loads(actual_command_str)

                # Now, process the actual command
                return self.process_actual_command(actual_command)
            else:
                return json.dumps({"response": "Invalid command structure"})

        except json.JSONDecodeError:
            return json.dumps({"response": "Invalid JSON format"})

    def process_actual_command(self, command):
        # Here you process the actual command logic
        if 'action' in command and command['action'] == 'login':
            username = command['username']
            password = command['password']
            if login(username, password):
                return json.dumps({"response": "Login successful"})
            else:
                return json.dumps({"response": "Login failed"})
        else:
            return json.dumps({"response": "Invalid command"})


#controlling if the arguments are true or not
#if true, take the port number
if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != '--port':
        print("Usage: python3 yourapp.py --port <port_number>")
        sys.exit(1)

    port = int(sys.argv[2])
    server = Server(port)
    server.start()