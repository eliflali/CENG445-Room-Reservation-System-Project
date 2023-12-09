organizationPermissions = {
                    "LIST": 0, #user can list the Room objects in the organization
                    "ADD": 1, #user can add new rooms to the organization.
                    "ACCESS": 2, #user can access the rooms and events in the organization.
                    "DELETE": 3 # user can delete a Room in the organization 
                    #if s/he also has WRITE permission on it. 
                    #Owner of the Organization can delete the Room 
                    #without WRITE permission. 
                    #All Events in the Room are automatically deleted 
                    #regardless of Event permissions.
                    }

roomPermissions = {
                "LIST": 0, #user can list and view the Event reservations for the room.
                "RESERVE": 1, #user can reserve the room.
                "PERRESERVE": 2, #user can reserve the room for periodic events.Implies RESERVE.
                "DELETE": 3 #user can delete the reservations for the room. 
                            #It requires WRITE permission on the Event. 
                            #Owner of the Room can delete any events 
                            #WRITE permission on event.
}

eventPermissions = {
                "READ": 0, #User can see the title and details of the events. 
                            #If not granted room will be displayed as BUSY without any other detail.
                "WRITE": 1 #User can update and delete (if Room has DELETE too) the Event.
}