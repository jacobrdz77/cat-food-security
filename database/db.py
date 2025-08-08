import sqlite3
import string
import random

DB_PATH= "/home/jacop/dev/cat-food-security/database/logs.db"

# Singleton class
class Database:

    _instance = None # Class variable (static)

    # __new__ allocates memory and creates the object
    # Mostly used for Singleton or Immutable objects
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls) # The main constructor of a Python object
            cls._instance._init() # Intializes the instance -> creates new DB
        return cls._instance

    def _init(self) -> None:
        try:
            print("Initializing DB...")
            self.db = sqlite3.connect(DB_PATH) # isolation_level=None makes it so that it enables auto_commit -> which automatically save the db inserts to the actual database.
            if not self.db:
                raise RuntimeError("Couldn't connect to DB")
            self.cur = self.db.cursor()
            self.define_schema()
            print("Finished creating schema!")
        except Exception as e:
            print(f"Error initializing Database: {e}")
            raise e
    

    def define_schema(self):
        try:
            # Logs table
            self.cur.execute("CREATE TABLE IF NOT EXISTS detect_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, created_at INTEGER DEFAULT (unixepoch()), img_path TEXT NOT NULL, type TEXT NOT NULL )")
        except Exception as e:
            print(f"Error creating schema: {e}")
            raise e

    def get_logs(self) -> list:
        try:
            res = self.cur.execute("SELECT * FROM detect_logs")
            return res.fetchall()
        except Exception as e:
            print(f"Error fetching logs: {e}")
            raise e
    
    def create_log(self, img_path: str, type: str):
        try:
            if not img_path:
                raise ValueError("img_path must not be empty")

            self.cur.execute("INSERT INTO detect_logs (img_path, type) VALUES (?, ?)",[img_path, type])
            self.db.commit() # Confirms the transaction and SAVES it to the database
            print("Created log!")
        except Exception as e:
            print(f"Error creating log: {e}")
            self.db.rollback()
            raise e

    def close(self):
        self.db.close()

def main():
    db = Database()
    rand_characters = string.ascii_letters + string.digits
    random_str = ''.join(random.choices(rand_characters, k=10))
    try:
        db.create_log(random_str, "cat")
        logs = db.get_logs()
        print(f"Got logs: {logs}")
    except Exception as e:
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    main()
