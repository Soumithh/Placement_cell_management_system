import customtkinter as ctk
from logic.auth_controller import AuthController

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        # Deep blue background from reference
        super().__init__(master, fg_color="#181a2e")
        self.app_controller = app_controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Glass panel container, strictly forced to 620x620 Square
        self.login_box = ctk.CTkFrame(self, width=620, height=620, corner_radius=20, fg_color="#2b304c", border_width=1, border_color="#3e4368")
        self.login_box.grid(row=1, column=1, sticky="n", padx=20, pady=20)
        self.login_box.grid_propagate(False)
        
        self.login_box.grid_columnconfigure(0, weight=1)
        self.login_box.grid_rowconfigure(0, weight=1) # top spacer
        self.login_box.grid_rowconfigure(9, weight=1) # bottom spacer

        # Main glowing icon circle
        self.logo_circle = ctk.CTkFrame(self.login_box, width=65, height=65, corner_radius=32, fg_color="#7158E2")
        self.logo_circle.grid(row=1, column=0, pady=(10, 10))
        ctk.CTkLabel(self.logo_circle, text="➔]", text_color="white", font=ctk.CTkFont(size=22, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(self.login_box, text="Placement Cell Portal", text_color="white", font=ctk.CTkFont(family="Inter", size=26, weight="bold"))
        self.title_label.grid(row=2, column=0, pady=(5, 5))
        
        self.subtitle_label = ctk.CTkLabel(self.login_box, text="Sign in to continue", text_color="#A0A0BA", font=ctk.CTkFont(family="Inter", size=14))
        self.subtitle_label.grid(row=3, column=0, pady=(0, 20))

        # Username Input Layer
        self.user_frame = ctk.CTkFrame(self.login_box, fg_color="transparent")
        self.user_frame.grid(row=4, column=0, pady=(5, 5), padx=50, sticky="ew")
        ctk.CTkLabel(self.user_frame, text="Username", text_color="white", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 6))
        # White background inputs matching reference
        self.username_entry = ctk.CTkEntry(self.user_frame, placeholder_text="user", placeholder_text_color="#888", height=45, corner_radius=10, fg_color="white", border_width=0, text_color="black", font=ctk.CTkFont(size=14))
        self.username_entry.pack(fill="x")

        # Password Input Layer
        self.pass_frame = ctk.CTkFrame(self.login_box, fg_color="transparent")
        self.pass_frame.grid(row=5, column=0, pady=(5, 5), padx=50, sticky="ew")
        ctk.CTkLabel(self.pass_frame, text="Password", text_color="white", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 6))
        self.password_entry = ctk.CTkEntry(self.pass_frame, placeholder_text="••••", show="*", placeholder_text_color="#888", height=45, corner_radius=10, fg_color="white", border_width=0, text_color="black", font=ctk.CTkFont(size=16))
        self.password_entry.pack(fill="x")

        self.error_label = ctk.CTkLabel(self.login_box, text="", text_color="#ff4c4c", font=ctk.CTkFont(size=12))
        self.error_label.grid(row=6, column=0, pady=(10, 5))

        self.login_button = ctk.CTkButton(self.login_box, text="Sign In", height=48, corner_radius=12,
                                          fg_color="#8c52ff", hover_color="#5e1b9f", text_color="white", font=ctk.CTkFont(family="Inter", size=16, weight="bold"),
                                          command=self.handle_login)
        self.login_button.grid(row=7, column=0, pady=(10, 20), padx=50, sticky="ew")

        # Registration Swap
        self.reg_frame = ctk.CTkFrame(self.login_box, fg_color="transparent")
        self.reg_frame.grid(row=8, column=0, pady=(0, 10))

        ctk.CTkLabel(self.reg_frame, text="Don't have an account?", text_color="white", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 5))
        ctk.CTkButton(self.reg_frame, text="Create an account", text_color="#63b3ed", fg_color="transparent", hover_color="#2b304c", 
                      font=ctk.CTkFont(size=14, weight="bold"), width=0, height=0,
                      command=self.app_controller.show_register).pack(side="left")

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.error_label.configure(text="Please enter all required fields.")
            return

        result = AuthController.login(username, password)
        if result["success"]:
            self.app_controller.show_dashboard(result["user"])
        else:
            self.error_label.configure(text=result["message"])
