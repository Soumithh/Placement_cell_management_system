from database.database_manager import db_manager, log_activity

class StudentController:
    @staticmethod
    def get_all_jobs():
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("""
            SELECT j.id, j.title, j.salary, j.vacancy, c.name as company_name 
            FROM JOB j 
            JOIN COMPANY c ON j.company_id = c.id
        """)
        return cursor.fetchall()

    @staticmethod
    def apply_to_job(user_id, job_id):
        cursor = db_manager.get_mysql_cursor()
        
        # Verify student exists perfectly
        cursor.execute("SELECT id FROM STUDENT WHERE user_id = %s", (user_id,))
        student = cursor.fetchone()
        if not student:
            return {"success": False, "message": "Student profile not linked to user."}

        try:
            cursor.execute("INSERT INTO PLACEMENTS (student_id, job_id, status) VALUES (%s, %s, %s)",
                           (student['id'], job_id, 'Applied'))
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
        cursor.execute("SELECT id FROM STUDENT WHERE user_id = %s", (user_id,))
        student = cursor.fetchone()
        if not student: return []

        cursor.execute("""
            SELECT p.status, j.title, c.name as company_name 
            FROM PLACEMENTS p
            JOIN JOB j ON p.job_id = j.id
            JOIN COMPANY c ON j.company_id = c.id
            WHERE p.student_id = %s
        """, (student['id'],))
        return cursor.fetchall()
