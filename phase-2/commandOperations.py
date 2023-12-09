import sys
from threading import Thread, Lock, Condition
import socket
import json
import struct
from users import UserManager
from models import Event, Room, Organization

class DatabaseLock:
    db_lock = Lock()


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
        organization = Organization()
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

                elif command['action'] == 'list rooms':
                    organization_id = command['organization id']
                    org = organization.get_organization(organization_id)
                    permission = permission_check([0], org)
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})
                    return json.dumps({"response": org.rooms})

                elif command['action'] == 'add room':
                    organization_id = command['organization id']
                    org = organization.get_organization(organization_id)
                    permission = permission_check([1], org)
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})
                    name = command['name']
                    x = command['x']
                    y = command['y']
                    capacity = command['capacity']
                    working_hours = command['working hours']
                    permissions = command['permissions']
                    org.create_organization_room(name, x, y, capacity, working_hours, permissions)
                    return json.dumps({"response": "Room" + name + "successfully created."})




                    

        else:
            return json.dumps({"response": "Invalid command"})