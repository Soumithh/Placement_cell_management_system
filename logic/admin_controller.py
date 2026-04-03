from database.database_manager import db_manager, log_activity
from logic.auth_controller import AuthController

class AdminController:
    @staticmethod
    def get_all_users(role_name=None):
        cursor = db_manager.get_mysql_cursor()
        if not cursor: return []
        query = """
        SELECT l.username, u.name, r.role_name 
        FROM LOGIN l 
        JOIN USER u ON l.user_id = u.id 
        JOIN ROLES r ON u.role_id = r.id
        """
        if role_name:
            query += " WHERE r.role_name = %s"
            cursor.execute(query, (role_name,))
        else:
            cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_all_students():
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("""
            SELECT s.id, u.name, s.dept, s.cgpa 
            FROM STUDENT s 
            JOIN USER u ON s.user_id = u.id
        """)
        return cursor.fetchall()
        
    @staticmethod
    def get_all_jobs():
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("SELECT j.id, j.title, c.name as company_name FROM JOB j JOIN COMPANY c ON j.company_id = c.id")
        return cursor.fetchall()

    @staticmethod
    def create_student(username, password, name, phone, dept, cgpa):
        # 1. Base User creation
        base = AuthController.register_base_user(username, password, 2, name)
        if not base['success']: return base

        try:
            cursor = db_manager.get_mysql_cursor()
            user_id = base['user_id']
            
            # 2. Insert PHONE
            cursor.execute("INSERT INTO USER_PHONE (user_id, phone) VALUES (%s, %s)", (user_id, phone))
            
            # 3. Insert STUDENT
            cursor.execute("INSERT INTO STUDENT (user_id, dept, cgpa) VALUES (%s, %s, %s)", 
                           (user_id, dept, cgpa))
            
            db_manager.commit_mysql()
            log_activity("ADMIN_ACTION", 1, f"Created student {name}")
            return {"success": True, "message": "Student created successfully"}
        except Exception as e:
            db_manager.mysql_conn.rollback()
            return {"success": False, "message": str(e)}

    @staticmethod
    def create_company(username, password, name, phone, location, contact):
        base = AuthController.register_base_user(username, password, 3, name)
        if not base['success']: return base

        try:
            cursor = db_manager.get_mysql_cursor()
            user_id = base['user_id']
            
            # Optional: Link phone in USER_PHONE as well? The design explicitly asks for contact in COMPANY.
            # But "USER_PHONE must reference USER". I will insert it just to follow the strict ER rule.
            cursor.execute("INSERT INTO USER_PHONE (user_id, phone) VALUES (%s, %s)", (user_id, phone))
            
            # Insert COMPANY
            cursor.execute("INSERT INTO COMPANY (user_id, name, location, contact) VALUES (%s, %s, %s, %s)", 
                           (user_id, name, location, contact))
            
            db_manager.commit_mysql()
            log_activity("ADMIN_ACTION", 1, f"Created company {name}")
            return {"success": True, "message": "Company created successfully"}
        except Exception as e:
            db_manager.mysql_conn.rollback()
            return {"success": False, "message": str(e)}

    @staticmethod
    def assign_placement(student_id, job_id, status):
        cursor = db_manager.get_mysql_cursor()
        try:
            cursor.execute("INSERT INTO PLACEMENTS (student_id, job_id, status) VALUES (%s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE status=%s", (student_id, job_id, status, status))
            db_manager.commit_mysql()
            return {"success": True, "message": "Placement updated successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}
