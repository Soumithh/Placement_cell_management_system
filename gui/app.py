import customtkinter as ctk
from gui.login_frame import LoginFrame
from gui.register_frame import RegisterFrame
from gui.admin_dashboard import AdminDashboard
from gui.student_dashboard import StudentDashboard
from gui.company_dashboard import CompanyDashboard
from logic.auth_controller import AuthController

class PlacementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Placement Cell Management System")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Ensure admin account exists on startup
        AuthController.ensure_admin_exists()

        self.current_user = None

        # Container for screens
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        self.show_login()

    def show_login(self):
        self.clear_container()
        login_frame = LoginFrame(self.container, self)
        login_frame.grid(row=0, column=0, sticky="nsew")

    def show_register(self):
        self.clear_container()
        register_frame = RegisterFrame(self.container, self)
        register_frame.grid(row=0, column=0, sticky="nsew")

    def show_dashboard(self, user_info):
        self.current_user = user_info
        self.clear_container()

        role = user_info.get("role_name")
        if role == "Admin":
            dashboard = AdminDashboard(self.container, self)
        elif role == "Student":
            dashboard = StudentDashboard(self.container, self)
        elif role == "Company":
            dashboard = CompanyDashboard(self.container, self)
        else:
            self.show_login()
            return
            
        dashboard.grid(row=0, column=0, sticky="nsew")

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def logout(self):
        self.current_user = None
        self.show_login()
