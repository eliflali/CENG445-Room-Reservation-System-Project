class Room:
    def __init__(self, name, x, y, capacity, working_hours, permissions):
        """
        Constructor for creating a new Room object.
        :param name: String, the name of the room.
        :param x: Float, the x-coordinate of the room's location.
        :param y: Float, the y-coordinate of the room's location.
        :param capacity: Integer, the capacity of the room.
        :param working_hours: String, the working hours of the room.
        :param permissions: List, the list of permissions required to access the room.
        """
        self.name = name
        self.coordinates = (x, y)
        self.capacity = capacity
        self.working_hours = working_hours
        self.permissions = permissions
        # Additional attributes like location can be added here

    @classmethod
    def create_room(cls, name, x, y, capacity, working_hours, permissions):
        """
        Class method to create a new Room.
        :param name: String, the name of the room.
        :param x: Float, the x-coordinate of the room's location.
        :param y: Float, the y-coordinate of the room's location.
        :param capacity: Integer, the capacity of the room.
        :param working_hours: String, the working hours of the room.
        :param permissions: List, the list of permissions required to access the room.
        :return: Room object, the created room.
        """
        return cls(name, x, y, capacity, working_hours, permissions)

    def get_permissions(self):
        return self.permissions

    def read_room(self):
        """
        Class method to read a Room's details.
        :return: attributes of room object in dictionary form.
        """
        return {"name": self.name, 
                "coordinates": self.coordinates, 
                "capacity": self.capacity,
                "working_hours": self.working_hours,
                "permissions": self.permissions}

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

    def delete_room(self, name):
            """
            Class method to delete a Room.
            :param name: String, the name of the room to delete.
            """
            del self


class Event:
    def __init__(self, title, description, category, capacity, duration, weekly, permissions):
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
        self.title = title
        self.description = description
        self.category = category
        self.capacity = capacity
        self.duration = duration
        self.weekly = weekly
        self.permissions = permissions
        self.start_time = None
        self.location = None

    @classmethod
    def create_event(cls, title, description, category, capacity, duration, weekly, permissions):
        """
        Class method to create a new Event.
        :param title: String, the title of the event.
        :param description: String, the description of the event.
        :param category: String, the category of the event.
        :param capacity: Integer, the required capacity for the event.
        :param duration: Integer, the duration of the event in minutes.
        :param weekly: Boolean, True if the event occurs weekly, False otherwise.
        :param permissions: List, the list of permissions required to attend the event.
        :return: Event object, the created event.
        """
        return cls(title, description, category, capacity, duration, weekly, permissions)

    def read_event(self):
        """
        Class method to read an Event's details.
        :return: dictionary containing attributes of event object.
        """
        return {"title": self.title, 
                "description": self.description,
                "category": self.category,
                "capacity": self.capacity,
                "duration": self.duration,
                "weekly": self.weekly,
                "permissions": self.permissions}
    
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


# Example Usage
# Creating an event
event1 = Event.create_event("Team Meeting", "Weekly team meeting", "Meeting", 10, 60, None, ["user"])

# Reading an event's details
event_details = event1.read_event()
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


class Organization:
    #map changed to mapOrganization since map is reserved word
    def __init__(self, owner, name, mapOrganization, backgroundImage = None):
        self.owner = owner
        self.name = name
        self.map = mapOrganization
        self.backgroundImage = backgroundImage
        self.rooms = {}
        self.events = {}
        self.views = {}

    @classmethod
    def create_organization(cls, owner, name, mapOrganization, backgroundImage = None):
        return cls(owner, name, mapOrganization, backgroundImage)

    def read_organization(self):
        return {"owner": self.owner,
                "name": self.name,
                "map": self.map,
                "backgroundImage": self.backgroundImage,
                "rooms": self.rooms, 
                "events": self.events, 
                "views": self.views}
    
    def update_organization(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Attribute {key} not found in Event")

    def delete_organization(self):
        del self

    #Create for room will be deleted -- probably
    def create_organization_room(self, name, x, y, capacity, working_hours, permissions):
        return Room.create_room(name, x, y, capacity, working_hours, permissions)

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def add_room(self, room):
        self.rooms[room.name] = room

    #Read for room
    def read_organization_room(self, id):
        return self.get_room(id).read_room()
    
    #Update for room
    def update_organization_room(self, room_id, **kwargs):
        if room_id in self.rooms:
            self.get_room(room_id).update_room(kwargs)
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
            del self.rooms[room_id]
            self.get_room(room_id).delete_room()
        else:
            raise ValueError(f"No room found with ID {room_id}")

    def add_event(self, event):
        self.events[event.title] = event

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

    

    

# Example usage
org = Organization("Ahmed Muhsin", "Kirpi", "map")
room = Room("Conference Room", 0, 0, 10, "9AM-5PM", ["admin", "user"])
event = Event("Team Meeting", "Weekly team meeting", "Meeting", 10, 60, None, ["user"])
#event1.update_event(description="Bi-weekly team meeting")
org.add_room(room)
org.add_event(event)
org.update_organization_room(0, description="Bi-weekly team meeting")

# Logic to reserve rooms, query events, etc., can be added following the project specifications
