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
    def assign_placement(student_id, job_id, status):
        cursor = db_manager.get_mysql_cursor()
        try:
            cursor.execute("INSERT INTO PLACEMENTS (student_id, job_id, status) VALUES (%s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE status=%s", (student_id, job_id, status, status))
            db_manager.commit_mysql()
            return {"success": True, "message": "Placement updated successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}
