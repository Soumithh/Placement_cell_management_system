from database.database_manager import db_manager, log_activity
from logic.auth_controller import AuthController

class AdminController:
    @staticmethod
    def get_all_users(role_name=None):
        cursor = db_manager.get_mysql_cursor()
        if not cursor: return []
        query = """
        SELECT l.login_username as username, u.user_name as name, r.rol_desc as role_name 
        FROM LOGIN l 
        JOIN USER u ON l.user_id = u.user_id 
        JOIN ROLES r ON u.rol_id = r.rol_id
        """
        if role_name:
            query += " WHERE r.rol_desc = %s"
            cursor.execute(query, (role_name,))
        else:
            cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_all_students():
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("""
            SELECT s.stu_id as id, s.stu_name as name, s.stu_dept as dept, s.stu_cgpa as cgpa 
            FROM STUDENT s 
        """)
        return cursor.fetchall()
        
    @staticmethod
    def get_all_jobs():
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("SELECT j.job_id as id, j.job_name as title, c.com_name as company_name FROM JOB j JOIN COMPANY c ON j.com_id = c.com_id")
        return cursor.fetchall()

    @staticmethod
    def get_all_companies():
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("SELECT com_id as id, com_name as name FROM COMPANY")
        return cursor.fetchall()

    @staticmethod
    def create_job(user_id, company_id, title, salary, vacancy):
        cursor = db_manager.get_mysql_cursor()
        try:
            # We assume title, salary, vacancy are passed in. Salary maps to salary_min/max roughly, we just use min for simplicity since ER D has both.
            # But the ER diagram also maps job_type. Let's just insert what we have.
            cursor.execute("INSERT INTO JOB (com_id, job_name, salary_min, job_vacancy) VALUES (%s, %s, %s, %s)", 
                           (company_id, title, salary, vacancy))
            db_manager.commit_mysql()
            log_activity("JOB_CREATED", user_id, f"Admin created job id {cursor.lastrowid} - {title}")
            return {"success": True, "message": "Job created successfully"}
        except Exception as e:
            db_manager.mysql_conn.rollback()
            return {"success": False, "message": str(e)}
