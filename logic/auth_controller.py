import bcrypt
from database.database_manager import db_manager, log_activity

class AuthController:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def login(username, password, expected_role=None):
        cursor = db_manager.get_mysql_cursor()
        if not cursor:
            return {"success": False, "message": "Database disconnected"}

        query = """
            SELECT l.user_id, l.username, l.password_hash, u.name, u.role_id, r.role_name 
            FROM LOGIN l 
            JOIN USER u ON l.user_id = u.id 
            JOIN ROLES r ON u.role_id = r.id 
            WHERE l.username = %s
        """
        cursor.execute(query, (username,))
        user_record = cursor.fetchone()

        if user_record:
            if expected_role and user_record['role_name'] != expected_role:
                return {"success": False, "message": f"Account is not a {expected_role}"}

            if AuthController.verify_password(password, user_record['password_hash']):
                # Log to Mongo
                log_activity("LOGIN", user_record['user_id'], f"{username} logged in as {user_record['role_name']}")

                return {
                    "success": True, 
                    "user": {
                        "id": user_record['user_id'],
                        "username": user_record['username'],
                        "role_name": user_record['role_name'],
                        "role_id": user_record['role_id'],
                        "name": user_record['name']
                    }
                }
            else:
                return {"success": False, "message": "Invalid password"}
        return {"success": False, "message": "User not found"}

    @staticmethod
    def register_base_user(username, password, role_id, name):
        """Creates the core USER and LOGIN records."""
        cursor = db_manager.get_mysql_cursor()
        if not cursor:
            return {"success": False, "message": "Database disconnected"}

        try:
            # Insert into USER
            cursor.execute("INSERT INTO USER (name, role_id) VALUES (%s, %s)", (name, role_id))
            user_id = cursor.lastrowid
            
            # Insert into LOGIN
            hashed_pw = AuthController.hash_password(password)
            cursor.execute("INSERT INTO LOGIN (user_id, username, password_hash) VALUES (%s, %s, %s)", 
                           (user_id, username, hashed_pw))
            
            return {"success": True, "user_id": user_id, "message": "Base user created"}
        except Exception as e:
            # Reverting is handled externally if part of a broader transaction,
            # but we can try to rollback here for safety against immediate LOGIN unique violation
            db_manager.mysql_conn.rollback()
            return {"success": False, "message": str(e)}

    @staticmethod
    def ensure_admin_exists():
        cursor = db_manager.get_mysql_cursor()
        if not cursor: return
        
        cursor.execute("SELECT id FROM LOGIN WHERE username = 'admin'")
        if not cursor.fetchone():
            print("Creating default admin account...")
            try:
                cursor.execute("INSERT INTO USER (name, role_id) VALUES ('System Administrator', 1)")
                user_id = cursor.lastrowid
                hashed = AuthController.hash_password('admin123')
                cursor.execute("INSERT INTO LOGIN (user_id, username, password_hash) VALUES (%s, %s, %s)", (user_id, 'admin', hashed))
                db_manager.commit_mysql()
            except Exception as e:
                db_manager.mysql_conn.rollback()
