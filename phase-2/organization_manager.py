"""
This module defines an OrganizationManager class for managing organization data in a SQLite database.

The OrganizationManager class provides methods for creating an organization table in the database,
creating a new organization, and deleting an organization.

The organization table includes the following fields: id, name, description, and owner.
The id field is an integer that serves as the primary key.
The name field is a text string that must be unique.
The description field is a text string that stores the description of the organization.
The owner field is a text string that stores the username of the owner of the organization.

The create_organization method takes a name, description, and owner as arguments.
It inserts a new row into the organization table with the provided values.
"""
import sqlite3

class OrganizationManager:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self.conn = sqlite3.connect(self._db_path)
        self._create_organizations_table()
    
    def _create_organizations_table(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                owner TEXT NOT NULL,
                FOREIGN KEY(owner) REFERENCES users(username)
            );
        """)
        
        self.conn.commit()
    
    def create_organization(self, name: str, description: str, owner: str) -> None:
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO organizations (name, description, owner)
                VALUES (?, ?, ?);
            """, (name, description, owner))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True
            
    def delete_organization(self, name: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""DELETE FROM organizations WHERE name = ?;""", (name,))
        self.conn.commit()
    
    def get_all_organizations(self) -> list:
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM organizations;""")
        result = cursor.fetchall()
        
        return [{
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "owner": row[3]
        } for row in result] if result else None
    
    def get_organization(self, name: str) -> dict:
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM organizations WHERE name = ?;""", (name,))
        result = cursor.fetchone()
        
        return {
            "id": result[0],
            "name": result[1],
            "description": result[2],
            "owner": result[3]
        } if result else None

    def get_organization_owner(self, name: str):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT owner FROM organizations WHERE name = ?;""", (name,))
        result = cursor.fetchone()
        
        return result[0] if result else None
    


"""if __name__ == "__main__":
    organization_manager = OrganizationManager("project.db")
    
    organization_manager.create_organization("org1", "org1 description", "user1")
    
    org1 = organization_manager.get_organization_owner("org1")
    print(org1)"""