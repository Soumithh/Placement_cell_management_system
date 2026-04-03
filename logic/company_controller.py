from database.database_manager import db_manager, log_activity

class CompanyController:
    @staticmethod
    def get_my_company(user_id):
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("SELECT * FROM COMPANY WHERE user_id = %s", (user_id,))
        return cursor.fetchone()

    @staticmethod
    def create_job(user_id, title, salary, vacancy):
        cursor = db_manager.get_mysql_cursor()
        company = CompanyController.get_my_company(user_id)
        if not company:
            return {"success": False, "message": "Company profile not found for this user."}

        if int(vacancy) <= 0:
            return {"success": False, "message": "Vacancy must be greater than 0."}

        try:
            cursor.execute("INSERT INTO JOB (company_id, title, salary, vacancy) VALUES (%s, %s, %s, %s)",
                           (company['id'], title, salary, vacancy))
            db_manager.commit_mysql()
            log_activity("JOB_POST", user_id, f"Posted job {title}")
            return {"success": True, "message": "Job posted successfully"}
        except Exception as e:
            db_manager.mysql_conn.rollback()
            return {"success": False, "message": str(e)}

    @staticmethod
    def get_my_jobs(user_id):
        cursor = db_manager.get_mysql_cursor()
        company = CompanyController.get_my_company(user_id)
        if not company: return []
        cursor.execute("SELECT * FROM JOB WHERE company_id = %s", (company['id'],))
        return cursor.fetchall()

    @staticmethod
    def get_applicants(user_id):
        cursor = db_manager.get_mysql_cursor()
        company = CompanyController.get_my_company(user_id)
        if not company: return []
        
        cursor.execute("""
            SELECT p.status, j.title, u.name as student_name, s.cgpa
            FROM PLACEMENTS p
            JOIN JOB j ON p.job_id = j.id
            JOIN STUDENT s ON p.student_id = s.id
            JOIN USER u ON s.user_id = u.id
            WHERE j.company_id = %s
        """, (company['id'],))
        return cursor.fetchall()
