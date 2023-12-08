import hashlib
import sqlite3
import uuid


class UserManager:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self.conn = sqlite3.connect(self._db_path)
        self._create_users_table()
    
    def _create_users_table(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                fullname TEXT,
                token TEXT
            );
        """)
        
        self.conn.commit()
    
    def register_user(self, username: str, password: str, email: str, fullname: str) -> None:
        cursor = self.conn.cursor()
        password_hash = self._hash_password(password)
        try:
            cursor.execute("""
                INSERT INTO users (username, password_hash, email, fullname)
                VALUES (?, ?, ?, ?);
            """, (username, password_hash, email, fullname))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("""SELECT password_hash FROM users WHERE username = ?;""", (username,))
        
        result = cursor.fetchone()
        
        if result and self._check_password(password, result[0]):
            return self._generate_token(username)
        return None

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _check_password(self, password: str, password_hash: str) -> bool:
        return self._hash_password(password) == password_hash
    
    def _generate_token(self, username: str) -> str:
        token = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE users SET token = ? WHERE username = ?;""", (token, username))
        self.conn.commit()
        return token
    
    def verify_token(self, username: str, token: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("""SELECT token FROM users WHERE username = ?;""", (username,))
        result = cursor.fetchone()
        
        return token == result[0] if result else False
    
    def logout_user(self, username: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE users SET token = NULL WHERE username = ?;""", (username,))
        self.conn.commit()
        
    def get_user(self, username: str) -> dict:
        cursor = self.conn.cursor()
        cursor.execute("""SELECT username, email, fullname FROM users WHERE username = ?;""", (username,))
        result = cursor.fetchone()
        
        return {
            "username": result[0],
            "email": result[1],
            "fullname": result[2]
        } if result else None
    
    def update_user(self, username: str, email: str, fullname: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE users SET email = ?, fullname = ? WHERE username = ?;""", (email, fullname, username))
        self.conn.commit()
    
    def delete_user(self, username: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""DELETE FROM users WHERE username = ?;""", (username,))
        self.conn.commit()
    
    def __del__(self) -> None:
        self.conn.close()




user_manager = UserManager("users.db")

user_manager.register_user("test", "test", "test@test.com", "Test User")

# Authenticate a user
token = user_manager.authenticate_user('test', 'test')

if token:
    print("Login successful, token:", token)
else:
    print("Login failed")
    

# Verify token
is_valid = user_manager.verify_token('test', token)
print("Token valid:", is_valid)

# Logout user
user_manager.logout_user('test')
