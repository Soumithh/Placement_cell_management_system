import mysql.connector
from pymongo import MongoClient
import os

# MySQL config
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root123")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "placement_db")

# MongoDB config
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "placement_logs_db")

class DatabaseManager:
    def __init__(self):
        self.mysql_conn = None
        self.mongo_client = None
        self.mongo_db = None
        self.connect_mysql()
        self.connect_mongo()

    def connect_mysql(self):
        try:
            self.mysql_conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )
            print("Connected to MySQL successfully.")
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")

    def connect_mongo(self):
        try:
            self.mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self.mongo_client.server_info() # trigger exception if not reachable
            self.mongo_db = self.mongo_client[MONGO_DATABASE]
            print("Connected to MongoDB successfully.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_mysql_cursor(self):
        if not self.mysql_conn or not self.mysql_conn.is_connected():
            self.connect_mysql()
        if self.mysql_conn and self.mysql_conn.is_connected():
            return self.mysql_conn.cursor(dictionary=True)
        return None
    
    def commit_mysql(self):
        if self.mysql_conn and self.mysql_conn.is_connected():
            self.mysql_conn.commit()

db_manager = DatabaseManager()

def log_activity(action, user_id, details=""):
    """Log an activity to MongoDB"""
    if db_manager.mongo_db is not None:
        try:
            collection = db_manager.mongo_db["activity_logs"]
            import datetime
            log_entry = {
                "action": action,
                "user_id": user_id,
                "details": details,
                "timestamp": datetime.datetime.now()
            }
            collection.insert_one(log_entry)
        except Exception as e:
            print(f"Failed to log activity: {e}")
