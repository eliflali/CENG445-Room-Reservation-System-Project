import uuid
import hashlib

class User:
    """"User class for Authentication and Session Management"""
    
    def __init__(self, username, email, fullname, passwd):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.fullname = fullname
        self.password_hash = self._hash_password(passwd)
        self.token = None
        
    def _hash_password(self, passwd):
        return hashlib.sha256(passwd.encode()).hexdigest()
    
    def auth(self, plainpass):
        return self.password_hash == self._hash_password(plainpass)
    
    def login(self):
        self.token = str(uuid.uuid4())
        return self.token
    
    def checksession(self,token):
        return self.token == token
    
    def logout(self):
        self.token = None
        return True
    
    def get(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'fullname': self.fullname}
    
    def _repr_(self) -> str:
        return f"<User {self.username}>"
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'passwd':
                value = self._hash_password(value)
            setattr(self, key, value)
            
    def delete(self):
        del self

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
        else:
            raise ValueError("User ID not found")

    def get_current_user(self):
        return self.current_user


class Room:
    def __init__(self, user, name, x, y, capacity, working_hours, permissions):
        """
        Constructor for creating a new Room object.
        :param name: String, the name of the room.
        :param x: Float, the x-coordinate of the room's location.
        :param y: Float, the y-coordinate of the room's location.
        :param capacity: Integer, the capacity of the room.
        :param working_hours: String, the working hours of the room.
        :param permissions: List, the list of permissions required to access the room.
        """
        self.id = uuid.uuid4()
        self.user = user
        self.name = name
        self.coordinates = (x, y)
        self.capacity = capacity
        self.working_hours = working_hours
        self.permissions = permissions
        # Additional attributes like location can be added here

    def get_room(self):
        """
        Class method to read a Room's details.
        :return: attributes of room object in dictionary form.
        """
        return vars(self)

    def update_room(self, **kwargs):
        """
        Method to update the attributes of a Room.
        :param kwargs: Dictionary, key-value pairs of attributes to update.
        :raises AttributeError: If an attribute to update is not found in the Room.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Attribute {key} not found in Room")
        return True

    def delete_room(self, name):
        """
        Class method to delete a Room.
        :param name: String, the name of the room to delete.
        """
        del self
        return True
    
    def get_capacity(self):
        return self.capacity
    
    def get_working_hours(self):
        return self.working_hours
    
    def get_permissions(self):
        return self.permissions

    def get_id(self):
        return self.id




class Event:
    def __init__(self, owner, title, description, category, capacity, duration, weekly, permissions):
        """
        Constructor for creating a new Event object.
        :param title: String, the title of the event.
        :param description: String, the description of the event.
        :param category: String, the category of the event.
        :param capacity: Integer, the required capacity for the event.
        :param duration: Integer, the duration of the event in minutes.
        :param weekly: Boolean, True if the event occurs weekly, False otherwise.
        :param permissions: List, the list of permissions required to attend the event.
        """
        self.id = uuid.uuid4()
        self.owner = owner
        self.title = title
        self.description = description
        self.category = category
        self.capacity = capacity
        self.duration = duration
        self.weekly = weekly
        self.permissions = permissions
        self.start_time = None
        self.location = None

    def get_event(self):
        """
        Class method to read an Event's details.
        :return: dictionary containing attributes of event object.
        """
        return vars(self)
    
    def update_event(self, **kwargs):
        """
        Method to update the attributes of an Event.
        :param kwargs: Dictionary, key-value pairs of attributes to update.
        :raises AttributeError: If an attribute to update is not found in the Event.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Attribute {key} not found in Event")

    def delete_event(self, title):
        """
        Class method to delete an Event.
        :param title: String, the title of the event to delete.
        :raises ValueError: If the event to delete is not found.
        """
        del self
    
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

"""# Example Usage
# Creating an event
#event1 = Event.create_event("Team Meeting", "Weekly team meeting", "Meeting", 10, 60, None, ["user"])

# Reading an event's details
#event_details = event1.get_event()
print(event_details)

# Updating an event's details
event1.update_event(description="Bi-weekly team meeting")
print(event1.read_event())

# Deleting an event
event1.delete_event("Team Meeting")
print(event1.read_event())  # This will return None


# Example Usage
# Creating a room
room1 = Room.create_room("Conference Room", 0, 0, 10, "9AM-5PM", ["admin", "user"])

# Reading a room's details
room_details = room1.read_room()
print(room_details)

# Updating a room's details
room1.update_room(capacity=12)
print(room1)

# Deleting a room
room1.delete_room("Conference Room")
print(room1.read_room())  # This will return None
"""

class Organization:
    #map changed to mapOrganization since map is reserved word
    def __init__(self, user_manager, name, mapOrganization, backgroundImage = None):
        self.id = uuid.uuid4()
        self.owner = user_manager.get_current_user()
        self.name = name
        self.map = mapOrganization
        self.backgroundImage = backgroundImage
        self.rooms = {}
        self.events = {}

    @classmethod
    def create_organization(cls, owner, name, mapOrganization, backgroundImage = None):
        return cls(owner, name, mapOrganization, backgroundImage)

    def read_organization(self):
        return vars(self)
    
    def update_organization(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Attribute {key} not found in Event")

    def delete_organization(self):
        for room in self.rooms:
            room.delete_room()
            
        for event in self.events:
            event.delete_event()
            
        del self

    def create_organization_room(self, name, x, y, capacity, working_hours, permissions):
        current_user = self.owner
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

    def create_organization_event(self, title, description, category, capacity, duration, weekly, permissions):
        current_user = self.owner
        if current_user is None:
            raise Exception("No current user set in UserManager.")
        new_event = Event(owner, title, description, category, capacity, duration, weekly, permissions)
        id = new_event.get_id()
        self.events[id] = new_event
        #self.events[event.title] = event
        return id

    def reserve(self, event_title, room_name, start_time):
        pass

    def find_room(self, event, rect, start, end):
        pass
    
    def find_schedule(self, eventlist, rect, start, end):
        pass

    def reassign(event, room):
        pass
    
    def query(rect, title, category, room):
        pass

    

user_manager = UserManager()
user1 = User("Ahmed Muhsin", "Ahmed Muhsin", "Ahmed Muhsin Kirpi", "aslkd")
user_manager.add_user(user1)
user_manager.switch_user(user1.id) 
print(user_manager.get_current_user().get())
# Example usage
org = Organization(user_manager, "Kirpi", "map")
#room = Room("Conference Room", 0, 0, 10, "9AM-5PM", ["admin", "user"])
#event = Event("Team Meeting", "Weekly team meeting", "Meeting", 10, 60, None, ["user"])
#event1.update_event(description="Bi-weekly team meeting")
org.create_organization_room("Conference Room", 0, 0, 10, "9AM-5PM", ["admin", "user"])
org.create_organization_event(event)

# Logic to reserve rooms, query events, etc., can be added following the project specifications
