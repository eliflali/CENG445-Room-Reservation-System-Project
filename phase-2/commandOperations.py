import sys
from threading import Thread, Lock, Condition
import socket
import json
import struct
from users import UserManager
from models import Event, Room, Organization
from permissions import Permissions
import uuid

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
        usermanager = UserManager("./project.db")
        #organization = Organization()
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

                elif command['action'] == 'create_organization':
                    name = command['name']
                    organization_map = command['map']
                    permissions = command['permissions']
                    backgroundImage = None
                    if 'backgroundImage' in command:
                        backgroundImage = command['backgroundImage']

                    organization = Organization(usermanager.get_current_user(), name, organization_map, permissions, backgroundImage)
                    return json.dumps({"response": "Organization " + name + " successfully created. Id: "+ str(organization.get_id())})
                #Read for room
                elif command['action'] == 'list rooms':
                    organization_id = command['organization id']
                    org = Organization.get_organization(organization_id)
                    permission = Permissions.permission_check([0], org)
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})
                    return json.dumps({"response": org.rooms})

                elif command['action'] == 'add_room':
                    organization_id = command['organization_id']
                    org_uuid = uuid.UUID(organization_id)
                    org = Organization.get_organization(org_uuid)
                    permission = Permissions.permission_check([1], org)
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})
                    name = command['name']
                    x = command['x']
                    y = command['y']
                    capacity = command['capacity']
                    working_hours = command['working hours']
                    permissions = command['permissions']
                    room = org.create_organization_room(name, x, y, capacity, working_hours, permissions)
                    return json.dumps({"response": "Room " + name + " successfully created with id: " + str(room.get_id())})
                
                elif command['action'] == 'update_room':
                    organization_id = command['organization_id']
                    org_uuid = uuid.UUID(organization_id)
                    org = Organization.get_organization(org_uuid)
                    permission = Permissions.permission_check([2], org)
                    if not permission:
                        return json.dumps({"response": "You don't have permission."})

                    room_id = command['room_id']  # This needs to be provided for an update
                    room_uuid = uuid.UUID(room_id)
                    room = org.get_room(room_uuid)

                    # Gather only the arguments that were provided in the command
                    kwargs_to_update = {}
                    if 'name' in command:
                        kwargs_to_update['name'] = command['name']
                    if 'x' in command:
                        kwargs_to_update['x'] = command['x']
                    if 'y' in command:
                        kwargs_to_update['y'] = command['y']
                    if 'capacity' in command:
                        kwargs_to_update['capacity'] = command['capacity']
                    if 'working hours' in command:
                        kwargs_to_update['working_hours'] = command['working hours']
                    if 'permissions' in command:
                        kwargs_to_update['permissions'] = command['permissions']

                    # Update the room with the provided attributes
                    try:
                        org.update_organization_room(room_uuid, **kwargs_to_update)
                        return json.dumps({"response": "Room successfully updated."})
                    except ValueError as e:
                        return json.dumps({"response": str(e)})


                elif command['action'] == 'delete_room':
                    organization_id = command['organization_id']
                    room_id = command['room_id']
                    org_uuid = uuid.UUID(organization_id)
                    org = Organization.get_organization(org_uuid)
                    room_uuid = uuid.UUID(room_id)
                    room = org.get_room(room_uuid)

                    if(usermanager.get_current_user() == org.get_owner):
                        permission = Permissions.permission_check([2,3], org)

                    else:
                        permission = Permissions.permission_check([2,3], org, [4], room)
                    
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})

                    org.delete_organization_room(room_uuid)
                    return json.dumps({"response": "Room successfully deleted."})

                elif command['action'] == 'create_event':
                    organization_id = command['organization_id']
                    org_uuid = uuid.UUID(organization_id)
                    org = Organization.get_organization(org_uuid)

                    room_id = command['room_id']
                    room_uuid = uuid.UUID(room_id)
                    room = org.get_room(room_uuid)

                    permission = Permissions.permission_check([4], room, [1], event)
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})

                    title, description, category, capacity, duration, weekly, permissions
                    title = command['title']
                    description = command['description']
                    category = command['category']
                    capacity = command['capacity']
                    duration = command['duration']
                    weekly = command['weekly']
                    permissions = command['permissions']

                    event = org.create_organization_event(title, description, category, capacity, duration, weekly, permissions)

                    return json.dumps({"response": "Event successfully created with id: " + str(event.get_id())})

                elif command['action'] == 'list_events':
                    organization_id = command['organization_id']
                    org_uuid = uuid.UUID(organization_id)
                    org = Organization.get_organization(org_uuid)

                    room_id = command['room_id']
                    room_uuid = uuid.UUID(room_id)
                    room = org.get_room(room_uuid)

                    permission = Permissions.permission_check([0], room)
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})

                    return json.dumps({"response": room.get_reservations()})

                elif command['action'] == 'reserve': 
                    organization_id = command['organization_id']
                    org_uuid = uuid.UUID(organization_id)
                    org = Organization.get_organization(org_uuid)

                    room_id = command['room_id']
                    room_uuid = uuid.UUID(room_id)
                    room = org.get_room(room_uuid)

                    event_id = command['event_id']
                    event_uuid = uuid.UUID(event_id)
                    event = org.get_event(event_uuid)

                    start_time = command['start_time']

                    if type(event.weekly) is datetime:
                        permission = Permissions.permission_check([2], room)
                    else:
                        permission = Permissions.permission_check([1], room) or Permissions.permission_check([2], room)
            
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})

                    org.reserve(event, room, start_time)

                    return json.dumps({"response": room.get_name() + " reserved for event " + event.get_name()})

                elif command['action'] == 'delete_reservations':
                    organization_id = command['organization_id']
                    org_uuid = uuid.UUID(organization_id)
                    org = Organization.get_organization(org_uuid)

                    room_id = command['room id']
                    room_uuid = uuid.UUID(room_id)
                    room = org.get_room(room_uuid)

                    if(usermanager.get_current_user() == org.get_owner):
                        permission = Permissions.permission_check([3], room)

                    else:
                        reservations = room.get_reservations()
                        for reservation in reservations:
                            _,_,event = reservation
                            permission = Permissions.permission_check([3], room, [1], event)
                            if permission == False:
                                return json.dumps({"response": "You don't have permission."})
                    
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})

                    room.delete_reservations()

                    return json.dumps({"response": "Successfully deleted reservations for room: " + room.get_name()})
                
                elif command['action'] == 'read_event':
                    organization_id = command['organization_id']
                    org_uuid = uuid.UUID(organization_id)
                    org = Organization.get_organization(org_uuid)

                    room_id = command['room_id']
                    room_uuid = uuid.UUID(room_id)
                    room = org.get_room(room_uuid)

                    event_id = command['event_id']
                    event_uuid = uuid.UUID(event_id)
                    event = org.get_event(event_uuid)

                    permission = Permissions.permission_check([0], event)
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})

                    return json.dumps({"response": event.get()})

                elif command['action'] == 'update_event':
                    organization_id = command['organization_id']
                    org_uuid = uuid.UUID(organization_id)
                    org = Organization.get_organization(org_uuid)

                    room_id = command['room_id']
                    room_uuid = uuid.UUID(room_id)
                    room = org.get_room(room_uuid)

                    event_id = command['event_id']
                    event_uuid = uuid.UUID(event_id)
                    event = org.get_event(event_uuid)

                    permission = Permissions.permission_check([1], event)
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})

                    kwargs_to_update = {}
                    if 'title' in command:
                        kwargs_to_update['title'] = command['title']
                    if 'description' in command:
                        kwargs_to_update['description'] = command['description']
                    if 'category' in command:
                        kwargs_to_update['category'] = command['category']
                    if 'capacity' in command:
                        kwargs_to_update['capacity'] = command['capacity']
                    if 'duration' in command:
                        kwargs_to_update['duration'] = command['duration']
                    if 'weekly' in command:
                        kwargs_to_update['weekly'] = command['weekly']
                    if 'permissions' in command:
                        kwargs_to_update['permissions'] = command['permissions']

                    # Update the room with the provided attributes
                    try:
                        org.update_organization_event(event_uuid, **kwargs_to_update)
                        return json.dumps({"response": "Event successfully updated."})
                    except ValueError as e:
                        return json.dumps({"response": str(e)})

                elif command['action'] == 'delete_event':
                    organization_id = command['organization_id']
                    org_uuid = uuid.UUID(organization_id)
                    org = Organization.get_organization(org_uuid)

                    room_id = command['room_id']
                    room_uuid = uuid.UUID(room_id)
                    room = org.get_room(room_uuid)

                    event_id = command['event_id']
                    event_uuid = uuid.UUID(event_id)
                    event = org.get_event(event_uuid)

                    permission = Permissions.permission_check([1], event, [3], room)
                    if permission == False:
                        return json.dumps({"response": "You don't have permission."})

                    org.delete_organization_event(event_uuid)
                    return json.dumps({"response": "Event successfully deleted."})

        else:
            return json.dumps({"response": "Invalid command"})


    """
    {"action": "add_room", 
    "organization_id":"71d34c72-cbd9-4e94-8d3c-52045ae584fd",
    "name": "room1", "x": 10, "y": 20, 
    "capacity": 1000,"working hours": "09.00-17.00", 
    "permissions": ["LIST", "RESERVE", "PERRESERVE", "DELETE", "WRITE"]}
    """

    """
    {"action": "update_room", "organization_id":"71d34c72-cbd9-4e94-8d3c-52045ae584fd","room_id":"b7767821-af31-4a18-a374-ec2b7cec8ba4","name": "conference room"}
    """