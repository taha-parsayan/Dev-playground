import sqlite3

class DatabaseManager:
    def __init__(self, db_name="mydb.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
    
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                age INTEGER NOT NULL)''')
        self.connection.commit()
    
    def add_item(self, name, family_name, age):
        self.cursor.execute("INSERT INTO users (name, family_name, age) VALUES (?, ?, ?)",
                            (name, family_name, age))
        self.connection.commit()
    
    def delete_item(self, name, family_name, age):
        self.cursor.execute("DELETE FROM users WHERE name = ? AND family_name = ? AND age = ?", 
                            (name, family_name, age))
        self.connection.commit()
    
    def item_exists(self, name, family_name, age):
        self.cursor.execute("SELECT * FROM users WHERE name = ? AND family_name = ? AND age = ?", 
                            (name, family_name, age))
        return self.cursor.fetchone() is not None
    
    def update_item(self, user_id, name=None, family_name=None, age=None):
        if name:
            self.cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
        if family_name:
            self.cursor.execute("UPDATE users SET family_name = ? WHERE id = ?", (family_name, user_id))
        if age:
            self.cursor.execute("UPDATE users SET age = ? WHERE id = ?", (age, user_id))
        self.connection.commit()
    
    def close_connection(self):
        self.connection.close()

# Example Usage
if __name__ == "__main__":
    db = DatabaseManager()
    db.create_table()
    
    # Adding items
    db.add_item("John", "Doe", 28)
    db.add_item("Jane", "Smith", 32)
    
    # Check if an item exists
    exists = db.item_exists("John", "Doe")
    print("John Doe exists:", exists)
    
    # Update an item
    db.update_item(1, age=29)
    
    # Delete an item
    db.delete_item("John", "Doe", 28)
    
    # Close the connection when done
    db.close_connection()
