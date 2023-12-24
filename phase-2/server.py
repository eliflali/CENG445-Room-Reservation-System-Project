from threading import Thread, Lock, Condition
import socket
import struct
from commandOperations import CommandOperations


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
    def __init__(self, connection, address, command):
        Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.command = command

    def run(self):
        try:
            while True:
                command = self.command.getCommand()
                if command:
                    self.connection.sendall(command.encode())
                with self.command.lock:
                    self.command.arrivingCommand.wait()  # Wait for a new command
        except socket.error as e:
            print(f"Socket error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.connection.close()




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
                
                print(f"Received command: {command}")
                command = CommandOperations.process_command(command)
                self.command.newCommand(command)

        finally:
            self.connection.close()
            print(f"Connection closed with {self.address}")