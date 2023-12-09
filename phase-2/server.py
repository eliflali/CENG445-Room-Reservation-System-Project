import sys
from threading import Thread, Lock, Condition
import socket
import json
import struct
from users import UserManager


class DatabaseLock:
    db_lock = Lock()

class Command:
    def __init__(self):
        self.lock = Lock()
        self.buffer = []
        self.arrivingCommand = Condition(self.lock)
    def newCommand(self, command):
        with self.lock:
            self.buffer.append(command)
            self.arrivingCommand.notify_all()

    
    def getCommand(self):
        with self.lock:
            if len(self.buffer) > 0:
                currentCommand = self.buffer.pop(0) #pop 0th elmt
                return currentCommand #return 0th elmt
            else:
                return ""
    


class Server():
    def __init__(self, port):
        self.host = '' #this may change.
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def start(self):
        self.socket.listen(1)
        print(f"Server listening on port {self.port}")
        
        while True:
            commandProcessor = Command()
            agent_conn, agent_addr = self.socket.accept()
            reader = ReadAgent(agent_conn, agent_addr, commandProcessor)
            writer = WriteAgent(agent_conn, agent_addr, commandProcessor)

            #now agents started:
            reader.start()
            writer.start()

class WriteAgent(Thread):
    def __init__(self,connection, address, command):
        self.connection = connection
        self.address = address
        self.command = command
        self.lock = Lock()
        Thread.__init__(self)

    def run(self):
        command = self.command.getCommand()
        
        self.connection.sendall(command.encode())
        notexit = True
        while notexit:
            with self.command.lock:
                if not self.connection:  # Check if connection is closed
                    break
                self.command.arrivingCommand.wait()
            command = self.command.getCommand()
            if command == "":
                continue
            try:
                self.connection.sendall(command.encode())
            except:
                notexit = False



class ReadAgent(Thread):
    def __init__(self,connection, address, command):
        self.connection = connection
        self.address = address
        self.command = command
        Thread.__init__(self)

    def run(self):
        print(f"Connection established with {self.address}")
        try:
            while True:
                # Read the size of the command -- an binary encoded int
                if not self.connection:  # Check if connection is closed
                    exit(1)
                    break
                raw_size = self.connection.recv(4)
                if not raw_size:
                    break
                size = struct.unpack('!I', raw_size)[0]

                # Read the command
                raw_command = self.connection.recv(size)
                command = raw_command.decode()

                if command == '{"command":"close connection"}':
                    break
                
                command = CommandOperations.process_command(command)
                self.command.newCommand(command)

        finally:
            self.connection.close()
            print(f"Connection closed with {self.address}")


class CommandOperations:
     #in here make corresponding library calls:
    @staticmethod
    def process_command(command):
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
                return CommandOperations.process_actual_command(actual_command)
            else:
                return json.dumps({"response": "Invalid command structure"})

        except json.JSONDecodeError:
            return json.dumps({"response": "Invalid JSON format"})

    @staticmethod
    def process_actual_command(command):
        # Here you process the actual command logic
        usermanager = UserManager("./users.db")
        if 'action' in command:
            if command['action'] == 'login':
                username = command['username']
                password = command['password']
                token = usermanager.authenticate_user(username, password)
                if token:
                    return json.dumps({"response": "Login successful and this is your token: ", "token": token })
                else:
                    return json.dumps({"response": "Login failed"})

            with DatabaseLock.db_lock:
                if command['action'] == 'save': #this will be implemented
                    return json.dumps({"response": "Activity saved."})
                         
                elif command['action'] == 'register':
                    username = command['username']
                    password = command['password']
                    email = command['email']
                    fullname = command['fullname']
                    usermanager.register_user(username, password, email, fullname)
                    return json.dumps({"response": "Successfully registered."})
                    

        else:
            return json.dumps({"response": "Invalid command"})
