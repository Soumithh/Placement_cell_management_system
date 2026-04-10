from database.database_manager import db_manager, log_activity

class CompanyController:
    @staticmethod
    def get_my_company(user_id):
        cursor = db_manager.get_mysql_cursor()
        cursor.execute("SELECT com_id as id, user_id, com_name as name, com_desc, com_type, com_add, salary_min, salary_max FROM COMPANY WHERE user_id = %s", (user_id,))
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
            cursor.execute("INSERT INTO JOB (com_id, job_name, salary_min, job_vacancy) VALUES (%s, %s, %s, %s)",
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
        cursor.execute("SELECT job_id as id, job_name as title, salary_min as salary, job_vacancy as vacancy FROM JOB WHERE com_id = %s", (company['id'],))
        return cursor.fetchall()

    @staticmethod
    def delete_job(user_id, job_id):
        cursor = db_manager.get_mysql_cursor()
        company = CompanyController.get_my_company(user_id)
        if not company: return {"success": False, "message": "Company not found."}
        try:
            cursor.execute("DELETE FROM JOB WHERE job_id = %s AND com_id = %s", (job_id, company['id']))
            db_manager.commit_mysql()
            log_activity("JOB_DELETE", user_id, f"Deleted job id {job_id}")
            return {"success": True, "message": "Job deleted successfully."}
        except Exception as e:
            db_manager.mysql_conn.rollback()
            return {"success": False, "message": str(e)}

    @staticmethod
    def get_applicants(user_id):
        cursor = db_manager.get_mysql_cursor()
        company = CompanyController.get_my_company(user_id)
        if not company: return []
        
        cursor.execute("""
            SELECT p.plcm_id as placement_id, p.status, j.job_name as title, s.stu_name as student_name, s.stu_cgpa as cgpa,
                   s.stu_email as email, s.stu_phone as phone, s.stu_dept as dept, p.plcm_desc as description
            FROM PLACEMENTS p
            JOIN JOB j ON p.job_id = j.job_id
            JOIN STUDENT s ON p.stu_id = s.stu_id
            WHERE j.com_id = %s
        """, (company['id'],))
        return cursor.fetchall()

    @staticmethod
    def update_placement_status(user_id, placement_id, status):
        cursor = db_manager.get_mysql_cursor()
        company = CompanyController.get_my_company(user_id)
        if not company: return {"success": False, "message": "Company not found."}
        
        # Verify the placement belongs to a job posted by this company
        cursor.execute("""
            SELECT p.plcm_id FROM PLACEMENTS p 
            JOIN JOB j ON p.job_id = j.job_id 
            WHERE p.plcm_id = %s AND j.com_id = %s
        """, (placement_id, company['id']))
        if not cursor.fetchone():
            return {"success": False, "message": "Unauthorized placement update."}
            
        try:
            cursor.execute("UPDATE PLACEMENTS SET status = %s WHERE plcm_id = %s", (status, placement_id))
            db_manager.commit_mysql()
            log_activity("PLACEMENT_UPDATE", user_id, f"Updated placement {placement_id} to {status}")
            return {"success": True, "message": f"Applicant {status} successfully."}
        except Exception as e:
            db_manager.mysql_conn.rollback()
            return {"success": False, "message": str(e)}
