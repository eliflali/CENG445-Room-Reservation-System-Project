class Room:
    rooms = {}  # Class variable to store all rooms

    #constructor:
    def __init__(self, name, x, y, capacity, working_hours, permissions): 
        self.name = name
        self.coordinates = (x, y)
        self.capacity = capacity
        self.working_hours = working_hours
        self.permissions = permissions
        Room.rooms[name] = self  # Adding the room to the class variable

    #Create:
    @classmethod
    def create_room(cls, name, x, y, capacity, working_hours, permissions):
        if name in cls.rooms:
            raise ValueError("Room already exists")
        return cls(name, x, y, capacity, working_hours, permissions)

    #Read:
    @classmethod
    def read_room(cls, name):
        return cls.rooms.get(name)

    #Update:
    def update_room(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Attribute {key} not found in Room")

    #Delete:
    @classmethod
    def delete_room(cls, name):
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
        return vars(self)

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
