from logic.auth_controller import AuthController
from logic.company_controller import CompanyController
from logic.admin_controller import AdminController

def seed_database():
    print("--- Seeding Companies ---")
    AuthController.register_company("google", "test1234", "Google LLC", "Technology", "Mountain View, CA", "Tech")
    AuthController.register_company("amazon", "test1234", "Amazon Web Services", "Cloud Computing", "Seattle, WA", "Cloud")
    AuthController.register_company("morgan", "test1234", "JP Morgan", "Banking", "New York, NY", "Finance")

    print("--- Seeding Students ---")
    AuthController.register_student("alice", "test1234", "Alice Johnson", "alice@edu.com", "Computer Science", "9.2")
    AuthController.register_student("bob", "test1234", "Bob Smith", "bob@edu.com", "Information Technology", "8.5")
    AuthController.register_student("charlie", "test1234", "Charlie Brown", "charlie@edu.com", "Electronics", "7.9")
    AuthController.register_student("diana", "test1234", "Diana Prince", "diana@edu.com", "Mechanical", "8.8")

    # Fetch Companies to post jobs
    users = AdminController.get_all_users()
    companies = {u['username']: u['id'] for u in users if u['role_name'] == 'company'}

    print("--- Seeding Jobs ---")
    if "google" in companies:
        CompanyController.create_job(companies["google"], "Software Engineer", "120,000 USD", 15)
        CompanyController.create_job(companies["google"], "Data Scientist", "140,000 USD", 5)

    if "amazon" in companies:
        CompanyController.create_job(companies["amazon"], "Cloud Architect", "135,000 USD", 10)
        CompanyController.create_job(companies["amazon"], "Backend Developer", "115,000 USD", 20)

    if "morgan" in companies:
        CompanyController.create_job(companies["morgan"], "Quantitative Analyst", "150,000 USD", 3)
        CompanyController.create_job(companies["morgan"], "Security Operations", "95,000 USD", 8)

    print("--- Seeding COMPLETE! ---")
    print("You can log in manually with usernames: [alice, bob, charlie, diana, google, amazon, morgan]")
    print("Password for all dummy accounts: test1234")

if __name__ == "__main__":
    seed_database()
