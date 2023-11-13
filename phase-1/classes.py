class Room:
    rooms = {}  # Class variable to store all rooms

    #constructor:
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
        Room.rooms[name] = self  # Adding the room to the class variable

    #Create:
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
        :raises ValueError: If a room with the same name already exists.
        """

        if name in cls.rooms:
            raise ValueError("Room already exists")
        return cls(name, x, y, capacity, working_hours, permissions)

    #Read:
    @classmethod
    def read_room(cls, name):
        """
        Class method to read a Room's details.
        :param name: String, the name of the room.
        :return: Room object, the room with the specified name.
        """
        return cls.rooms.get(name)

    #Update:
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

    #Delete:
    @classmethod
    def delete_room(cls, name):
        """
        Class method to delete a Room.
        :param name: String, the name of the room to delete.
        :raises ValueError: If the room to delete is not found.
        """
        if name in cls.rooms:
            del cls.rooms[name]
        else:
            raise ValueError("Room not found")

    """
    input: room = Room("Conference Room", 0, 0, 10, "9AM-5PM", ["admin", "user"])
    output: {
    'name': 'Conference Room',
    'coordinates': (0, 0),
    'capacity': 10,
    'working_hours': '9AM-5PM',
    'permissions': ['admin', 'user']
    }

    """
    def get_details(self):
        """
        Method to get the details of a Room.
        :return: Dictionary, containing all the attributes of the room.
        """
        return vars(self)


class Event:
    events = {}  # Class variable to store all events

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
        Event.events[title] = self  # Adding the event to the class variable

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
        :raises ValueError: If an event with the same title already exists.
        """
        if title in cls.events:
            raise ValueError("Event already exists")
        return cls(title, description, category, capacity, duration, weekly, permissions)

    @classmethod
    def read_event(cls, title):
        """
        Class method to read an Event's details.
        :param title: String, the title of the event.
        :return: Event object, the event with the specified title.
        """
        return cls.events.get(title)

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

    @classmethod
    def delete_event(cls, title):
        """
        Class method to delete an Event.
        :param title: String, the title of the event to delete.
        :raises ValueError: If the event to delete is not found.
        """
        if title in cls.events:
            del cls.events[title]
        else:
            raise ValueError("Event not found")

    def get_details(self):
        """
        Method to get the details of an Event.
        :return: Dictionary, containing all the attributes of the event.
        """
        return vars(self)

# Example Usage
# Creating an event
event1 = Event.create_event("Team Meeting", "Weekly team meeting", "Meeting", 10, 60, None, ["user"])

# Reading an event's details
event_details = Event.read_event("Team Meeting")
print(event_details.get_details())

# Updating an event's details
event1.update_event(description="Bi-weekly team meeting")
print(event1.get_details())

# Deleting an event
Event.delete_event("Team Meeting")
print(Event.read_event("Team Meeting"))  # This will return None


# Example Usage
# Creating a room
room1 = Room.create_room("Conference Room", 0, 0, 10, "9AM-5PM", ["admin", "user"])

# Reading a room's details
room_details = Room.read_room("Conference Room")
print(room_details.get_details())

# Updating a room's details
room1.update_room(capacity=12)
print(room1.get_details())

# Deleting a room
Room.delete_room("Conference Room")
print(Room.read_room("Conference Room"))  # This will return None
