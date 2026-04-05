from logic.company_controller import CompanyController
from database.database_manager import db_manager

def seed_jobs():
    print("--- Seeding Jobs ---")
    
    cursor = db_manager.get_mysql_cursor()
    if not cursor:
        print("No DB Connection")
        return
        
    cursor.execute("SELECT u.id, l.username FROM USER u JOIN LOGIN l ON u.id = l.user_id WHERE u.role_id = (SELECT id FROM ROLES WHERE role_name='Company')")
    companies_db = cursor.fetchall()
    
    companies = {c['username']: c['id'] for c in companies_db}
    print("Found companies:", companies)

    if "google" in companies:
        CompanyController.create_job(companies["google"], "Software Engineer", "120,000 USD", 15)
        CompanyController.create_job(companies["google"], "Data Scientist", "140,000 USD", 5)

    if "amazon" in companies:
        CompanyController.create_job(companies["amazon"], "Cloud Architect", "135,000 USD", 10)
        CompanyController.create_job(companies["amazon"], "Backend Developer", "115,000 USD", 20)

    if "morgan" in companies:
        CompanyController.create_job(companies["morgan"], "Quantitative Analyst", "150,000 USD", 3)
        CompanyController.create_job(companies["morgan"], "Security Operations", "95,000 USD", 8)
        
    print("--- FINALIZED SEEDING ---")

if __name__ == '__main__':
    seed_jobs()
