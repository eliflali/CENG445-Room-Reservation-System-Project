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
                "DELETE": 3, #user can delete the reservations for the room. 
                            #It requires WRITE permission on the Event. 
                            #Owner of the Room can delete any events 
                            #WRITE permission on event.
                "WRITE": 4 #user can delete the reservations for the room. 
                            #It requires WRITE permission on the Event. 
                            #Owner of the Room can delete any events 
                            #WRITE permission on event.
}

eventPermissions = {
                "READ": 0, #User can see the title and details of the events. 
                            #If not granted room will be displayed as BUSY without any other detail.
                "WRITE": 1 #User can update and delete (if Room has DELETE too) the Event.
}

class Permissions:
    @staticmethod
    def permission_check(permission_index1, object1, permission_index2 = None, object2 = None):
        type1 = object1.get_type()
        object1_permissions = object1.get_permissions()
        available = 1

        permissionList1 = []
        match type1:
            case "organization":
                permissionList1 = organizationPermissions
                
            case "room":
                permissionList1 = roomPermissions

            case "event":
                permissionList1 = eventPermissions
            case _:
                print("Invalid object - no permission data.")
                return False
        
        if object2:
            type2 = object2.get_type()
            object2_permissions = object2.get_permissions()
            match type2:
                case "organization":
                    permissionList2 = organizationPermissions
                    
                case "room":
                    permissionList2 = roomPermissions

                case "event":
                    permissionList2 = eventPermissions
                case _:
                    print("Invalid object - no permission data.")
                    return False

            for ind in permission_index2:
                if permissionList2[ind] in object2_permissions:
                    available = 1
                else:
                    available = 0
        else:
            type2 = None
            object2_permissions = None
        

        
        for ind in permission_index1:
            if permissionList1[ind] in object1_permissions:
                available = 1
            else:
                available = 0

        

        if available == 0:
            return False
        else:
            return True

        
