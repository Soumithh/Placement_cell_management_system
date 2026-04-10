from database.database_manager import db_manager, log_activity

class StudentController:
    @staticmethod
    def get_all_jobs():
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("""
            SELECT j.job_id as id, j.job_name as title, j.salary_min as salary, j.job_vacancy as vacancy, c.com_name as company_name 
            FROM JOB j 
            JOIN COMPANY c ON j.com_id = c.com_id
        """)
        return cursor.fetchall()

    @staticmethod
    def apply_to_job(user_id, job_id, description=""):
        cursor = db_manager.get_mysql_cursor()
        
        # Verify student exists perfectly
        cursor.execute("SELECT stu_id as id FROM STUDENT WHERE user_id = %s", (user_id,))
        student = cursor.fetchone()
        if not student:
            return {"success": False, "message": "Student profile not linked to user."}

        try:
            cursor.execute("INSERT INTO PLACEMENTS (stu_id, job_id, status, plcm_desc) VALUES (%s, %s, %s, %s)",
                           (student['id'], job_id, 'Applied', description))
            db_manager.commit_mysql()
            log_activity("JOB_APPLY", user_id, f"Applied for job id {job_id}")
            return {"success": True, "message": "Applied successfully!"}
        except Exception as e:
            if "unique_application" in str(e).lower() or "duplicate" in str(e).lower():
                return {"success": False, "message": "You have already applied for this job."}
            db_manager.mysql_conn.rollback()
            return {"success": False, "message": str(e)}

    @staticmethod
    def get_my_applications(user_id):
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("SELECT stu_id as id FROM STUDENT WHERE user_id = %s", (user_id,))
        student = cursor.fetchone()
        if not student: return []

        cursor.execute("""
            SELECT p.status, j.job_id as job_id, j.job_name as title, c.com_name as company_name 
            FROM PLACEMENTS p
            JOIN JOB j ON p.job_id = j.job_id
            JOIN COMPANY c ON j.com_id = c.com_id
            WHERE p.stu_id = %s
        """, (student['id'],))
        return cursor.fetchall()

    @staticmethod
    def get_student_profile(user_id):
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("""
            SELECT u.user_name as name, l.login_username as username, s.stu_dept as dept, s.stu_cgpa as cgpa, p.phone_number as phone
            FROM USER u
            JOIN LOGIN l ON l.user_id = u.user_id
            JOIN STUDENT s ON s.user_id = u.user_id
            LEFT JOIN USER_PHONE p ON p.user_id = u.user_id
            WHERE u.user_id = %s
        """, (user_id,))
        return cursor.fetchone()
