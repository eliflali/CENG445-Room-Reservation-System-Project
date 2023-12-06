import hashlib
import sqlite3


def login(user,passwd):
    with sqlite3.connect('room_reservation.sql3') as db:
        c = db.cursor()
        row = c.execute('SELECT * FROM users WHERE username=?',(user,))
        row = c.fetchone()  # Fetch the first row of the result
        
        if row is not None and hashlib.sha256(passwd.encode()).hexdigest() == row[1]:
            return True
        
        return False
    

def adduser(user,passwd):
    encpass = hashlib.sha256(passwd.encode()).hexdigest()
    with sqlite3.connect('room_reservation.sql3') as db:
        c = db.cursor()
        c.execute('insert into users values (?,?)',(user,encpass))


def login_required(f):
    """Decorator to check if the user is logged in before performing an action"""
    def wrapper(username, password, *args, **kwargs):
        if not login(username, password):
            raise Exception("User must be logged in to perform this action.")
        return f(username, password, *args, **kwargs)
    return wrapper


@login_required
def print_user(username, password):
    print("test")


print_user("admin", "admin") # will print "test"
print_user("admin", "wrong_password") # will raise an exception