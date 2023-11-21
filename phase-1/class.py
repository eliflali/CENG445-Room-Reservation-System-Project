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
    def __init__(self):
        self.rooms = {}
        self.events = {}
        self.views = {}

    @classmethod
    def create_organization(cls):
        return cls()

    def read_organization(self):
        return {"rooms": self.rooms, 
                "events": self.events, 
                "views": self.views}

    def add_room(self, room):
        self.rooms[room.name] = room

    def get_room(self, roomName):
        return rooms[roomName]

    def add_event(self, event):
        self.events[event.title] = event

    def reserve_room(self, event_title, room_name, start_time):
        # Add logic to reserve a room for an event
        pass

    # Additional methods for CRUD operations on rooms and events can be added here

# Example usage
org = Organization()
room = Room("Conference Room", 0, 0, 10, "9AM-5PM", ["admin", "user"])
event = Event("Team Meeting", "Weekly team meeting", "Meeting", 10, 60, None, ["user"])

org.add_room(room)
org.add_event(event)

# Logic to reserve rooms, query events, etc., can be added following the project specifications
