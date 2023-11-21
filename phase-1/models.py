import datetime
import uuid
import hashlib
import secrets

class SingletonMeta(type):
    """
    A Singleton metaclass that creates only one instance of a class.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class UserManager(metaclass=SingletonMeta):
    def __init__(self):
        self.current_user = None
        self.users = {}  # Dictionary to store user objects

    def add_user(self, user):
        self.users[user.id] = user

    def switch_user(self, user_id):
        if user_id in self.users:
            self.current_user = self.users[user_id]
            print ("User switched to: ", self.current_user.get())
        else:
            raise ValueError("User ID not found")

    def get_current_user(self):
        return self.current_user

class CRUD:
    def __init__(self, **kwargs):
        # Create operation: Initialize the object with given arguments
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.id = uuid.uuid4()

    def get(self):
        # Read operation: Return the object's data in a readable format
        return vars(self)

    def update(self, **kwargs):
        # Update operation: Update object attributes with given keyword arguments
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Attribute {key} does not exist.")

    def delete(self):
        # Delete operation: You might want to handle this by removing the object from
        # a collection or database, or setting a flag that marks it as deleted.
        del self
        return f"Object {self.id} deleted."
    

class User(CRUD):
    def __init__(self, username, email, fullname, passwd):
        super().__init__(username=username, email=email, fullname=fullname)
        self.password_hash = self._hash_password(passwd)
        self.session_token = None

    def _hash_password(self, passwd):
        # Use hashlib or another library to hash the password
        return hashlib.sha256(passwd.encode('utf-8')).hexdigest()

    def auth(self, plainpass):
        # Check if the supplied password matches the user password hash
        return self.password_hash == self._hash_password(plainpass)

    def login(self):
        # Start a session for the user, return a random token to be used during the session
        self.session_token = secrets.token_hex()
        return self.session_token

    def checksession(self, token):
        # Check if the token is valid
        return token == self.session_token

    def logout(self):
        # End the session invalidating the token
        self.session_token = None  
    
    def get_id(self):
        return self.id
        
class Room(CRUD):
    def __init__(self, user, name, x, y, capacity, working_hours, permissions):
        super().__init__(user=user, name=name, x=x, y=y, capacity=capacity, working_hours=working_hours, permissions=permissions)
        self.reservations = []  
    def get_permissions(self):
        return self.permissions
    
    def get_capacity(self):
        return self.capacity
    
    def get_working_hours(self):
        return self.working_hours
    
    def get_permissions(self):
        return self.permissions
    
    def get_id(self):
        return self.id
    
    def is_available(self, start_time, duration):
        end_time = start_time + datetime.timedelta(minutes=duration)

        if not self.is_working_hours(start_time, end_time):
            return False
        
        for reservation in self.reservations:
            reservation_start, reservation_end = reservation
            # Check for overlap between reservations
            if start_time < reservation_end and end_time > reservation_start:
                return False  # Room is already reserved during this time

        # If no conflicts were found, the room is available
        return True

    def is_working_hours(self, start_time, end_time):
        # Check if the event's time interval falls within the room's working hours
        return self.working_hours[0] <= start_time.time() <= self.working_hours[1] and \
               self.working_hours[0] <= end_time.time() <= self.working_hours[1]
    
class Event:
    def __init__(self, title, description, category, capacity, duration, weekly, permissions):
        super().__init__(title=title, description=description, category=category, capacity=capacity, duration=duration, weekly=weekly, permissions=permissions)
    
    def get_permissions(self):
        return self.permissions
    
    def get_capacity(self):
        return self.capacity
    
    def get_duration(self):
        return self.duration
    
    def get_weekly(self):
        return self.weekly
    
    def get_category(self):
        return self.category
    
    def get_id(self):
        return self.id


class Organization(CRUD):
    #map changed to mapOrganization since map is reserved word
    def __init__(self, owner, name, mapOrganization, backgroundImage = None):
        super().__init__(name=name, mapOrganization=mapOrganization, backgroundImage=backgroundImage)
        self.user_manager = owner #UserManager is singleton instance.
        self.owner = owner.get_current_user()
        self.rooms = {}
        self.events = {}

    def delete(self):
        for room in self.rooms:
            room.delete_room()
            
        for event in self.events:
            event.delete_event()
            
        del self

    def create_organization_room(self, name, x, y, capacity, working_hours, permissions):
        current_user = self.user_manager.get_current_user()
        if current_user is None:
            raise Exception("No current user set in UserManager.")
        new_room = Room(current_user, name, x, y, capacity, working_hours, permissions)
        id = new_room.get_id()
        self.rooms[id] = new_room
        return id

    def get_room(self, room_id):
        return self.rooms.get(room_id)
    
    #Read for room
    def read_organization_room(self, id):
        return self.rooms[id].get_room()
    
    #Update for room
    def update_organization_room(self, room_id, **kwargs):
        if room_id in self.rooms:
            return self.rooms[room_id].update_room(**kwargs)
            """for key, value in kwargs.items():
                if hasattr(self.rooms[room_id], key):
                    setattr(self.rooms[room_id], key, value)
                else:
                    raise AttributeError(f"Attribute {key} not found in Room")"""
        else:
            raise ValueError(f"No room found with ID {room_id}")

    #Delete for room
    def delete_organization_room(self, room_id):
        if room_id in self.rooms:
            self.rooms[room_id].delete_room()
            del self.rooms[room_id]
        else:
            raise ValueError(f"No room found with ID {room_id}")

    def add_event(self, event):
        self.events[event.title] = event

    def reserve(self, event_title, room_name, start_time):
        pass

    def find_room(self, event, rect, start, end):
        available_rooms = []

        for room_id, room in self.rooms.items():
            if room.is_available(start, end - start):
                if room.capacity >= event.get_capacity():
                    available_rooms.append(room)

        return available_rooms
    
    def find_schedule(self, eventlist, rect, start, end):
        pass

    def reassign(event, room):
        pass
    
    def query(rect, title, category, room):
        pass
