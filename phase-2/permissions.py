organizationPermissions = {
                    0: "LIST", #user can list the Room objects in the organization
                    1: "ADD", #user can add new rooms to the organization.
                    2: "ACCESS", #user can access the rooms and events in the organization.
                    3: "DELETE" # user can delete a Room in the organization 
                    #if s/he also has WRITE permission on it. 
                    #Owner of the Organization can delete the Room 
                    #without WRITE permission. 
                    #All Events in the Room are automatically deleted 
                    #regardless of Event permissions.
                    }

roomPermissions = {
                0: "LIST", #user can list and view the Event reservations for the room.
                1: "RESERVE", #user can reserve the room.
                2: "PERRESERVE", #user can reserve the room for periodic events.Implies RESERVE.
                3: "DELETE", #user can delete the reservations for the room. 
                            #It requires WRITE permission on the Event. 
                            #Owner of the Room can delete any events 
                            #WRITE permission on event.
                4: "WRITE" #user can delete the reservations for the room. 
                            #It requires WRITE permission on the Event. 
                            #Owner of the Room can delete any events 
                            #WRITE permission on event.
}

eventPermissions = {
                0: "READ", #User can see the title and details of the events. 
                            #If not granted room will be displayed as BUSY without any other detail.
                1: "WRITE" #User can update and delete (if Room has DELETE too) the Event.
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
        

        print(permissionList1)
        
        for ind in permission_index1:
            if permissionList1[ind] in object1_permissions:
                available = 1
            else:
                available = 0

        

        if available == 0:
            return False
        else:
            return True

        
