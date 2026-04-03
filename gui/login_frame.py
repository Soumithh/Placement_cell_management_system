import customtkinter as ctk
from logic.auth_controller import AuthController

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master)
        self.app_controller = app_controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Login Box
        self.login_box = ctk.CTkFrame(self, width=400, corner_radius=15)
        self.login_box.grid(row=1, column=1, rowspan=4, sticky="nsew", padx=20, pady=20)
        self.login_box.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.login_box, text="Placement Cell", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(30, 10))

        # Role Selector (Segmented Button for distinct logins)
        self.role_var = ctk.StringVar(value="Student")
        self.role_selector = ctk.CTkSegmentedButton(self.login_box, values=["Admin", "Company", "Student"], variable=self.role_var)
        self.role_selector.grid(row=1, column=0, pady=(10, 20))

        self.username_entry = ctk.CTkEntry(self.login_box, placeholder_text="Username", width=250)
        self.username_entry.grid(row=2, column=0, pady=10)

        self.password_entry = ctk.CTkEntry(self.login_box, placeholder_text="Password", show="*", width=250)
        self.password_entry.grid(row=3, column=0, pady=10)

        self.error_label = ctk.CTkLabel(self.login_box, text="", text_color="red")
        self.error_label.grid(row=4, column=0, pady=5)

        self.login_button = ctk.CTkButton(self.login_box, text="Login", width=250, command=self.handle_login)
        self.login_button.grid(row=5, column=0, pady=(10, 30))

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        expected_role = self.role_var.get()

        if not username or not password:
            self.error_label.configure(text="Please enter all fields")
            return

        result = AuthController.login(username, password, expected_role=expected_role)
        if result["success"]:
            self.app_controller.show_dashboard(result["user"])
        else:
            self.error_label.configure(text=result["message"])
