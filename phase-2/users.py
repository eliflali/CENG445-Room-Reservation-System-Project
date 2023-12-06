import hashlib
import secrets


class User():
    all_users = []
    
    def __init__(self, username, email, fullname, passwd):
        self.id = len(User.all_users)
        self.username = username
        self.email = email
        self.fullname = fullname
        self.password_hash = self._hash_password(passwd)
        self.session_token = None
        
        User.all_users.append(self)
        print(f"User {self.username} created")
        

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
    
def login_required(f):
    def wrapper(user, *args, **kwargs):
        if user.session_token is None:
            raise Exception("User must be logged in to perform this action.")
        return f(user, *args, **kwargs)
    return wrapper