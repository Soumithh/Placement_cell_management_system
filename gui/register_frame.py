import customtkinter as ctk
from logic.auth_controller import AuthController
from tkinter import messagebox

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="#181a2e")
        self.app_controller = app_controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.form_box = ctk.CTkFrame(self, width=680, height=680, corner_radius=20, fg_color="#2b304c", border_width=1, border_color="#3e4368")
        self.form_box.grid(row=1, column=1, sticky="n", padx=20, pady=20)
        self.form_box.grid_propagate(False)
        
        self.form_box.grid_columnconfigure(0, weight=1)
        self.form_box.grid_rowconfigure(0, weight=1) # top spacer
        self.form_box.grid_rowconfigure(7, weight=1) # bottom spacer

        self.logo_circle = ctk.CTkFrame(self.form_box, width=65, height=65, corner_radius=32, fg_color="#7158E2")
        self.logo_circle.grid(row=1, column=0, pady=(15, 5))
        ctk.CTkLabel(self.logo_circle, text="+ 👤", text_color="white", font=ctk.CTkFont(size=24)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.form_box, text="Create Account", text_color="white", font=ctk.CTkFont(family="Inter", size=26, weight="bold")).grid(row=2, column=0, pady=(5, 2))
        ctk.CTkLabel(self.form_box, text="Join the Placement Cell Portal", text_color="#A0A0BA", font=ctk.CTkFont(size=14)).grid(row=3, column=0, pady=(0, 15))

        self.content_frame = ctk.CTkFrame(self.form_box, fg_color="transparent")
        self.content_frame.grid(row=4, column=0, sticky="ew", padx=40, pady=(0, 10))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # The ComboBox Role Selection
        ctk.CTkLabel(self.content_frame, text="I am applying as a:", text_color="white", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))
        self.role_var = ctk.StringVar(value="Student")
        self.role_combo = ctk.CTkComboBox(self.content_frame, values=["Student", "Company"], variable=self.role_var, height=40, corner_radius=10, 
                                          fg_color="#181a2e", border_width=2, border_color="#7158E2", button_color="#181a2e", text_color="white", dropdown_fg_color="#181a2e", dropdown_text_color="white", state="readonly", command=self.on_role_change)
        self.role_combo.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Dynamic Field Container
        self.dynamic_wrapper = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.dynamic_wrapper.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.dynamic_wrapper.grid_columnconfigure(0, weight=1)
        self.dynamic_wrapper.grid_columnconfigure(1, weight=1)

        # Button Container
        self.btn_frame = ctk.CTkFrame(self.form_box, fg_color="transparent")
        self.btn_frame.grid(row=5, column=0, sticky="ew", padx=40, pady=(10, 15))

        self.submit_btn = ctk.CTkButton(self.btn_frame, text="Sign Up", height=45, corner_radius=12, fg_color="#8c52ff", hover_color="#5e1b9f", text_color="white", font=ctk.CTkFont(family="Inter", size=16, weight="bold"), command=self.handle_register)
        self.submit_btn.pack(fill="x")

        # Back link
        self.login_link = ctk.CTkFrame(self.form_box, fg_color="transparent")
        self.login_link.grid(row=6, column=0, pady=(0, 20))
        ctk.CTkLabel(self.login_link, text="Already have an account?", text_color="white", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 5))
        ctk.CTkButton(self.login_link, text="Sign In", text_color="#63b3ed", fg_color="transparent", hover_color="#2b304c", font=ctk.CTkFont(size=14, weight="bold"), width=0, height=0, command=self.app_controller.show_login).pack(side="left")

        # Initial Render
        self.input_vars = {}
        self.on_role_change("Student")

    def create_field(self, parent, label_text, placeholder, row, col, columnspan=1, is_pass=False, padx_l=0, padx_r=0):
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=row, column=col, columnspan=columnspan, sticky="ew", pady=3, padx=(padx_l, padx_r))
        ctk.CTkLabel(wrapper, text=label_text, text_color="white", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 3))
        
        # White inputs to match reference UI exact style
        entry = ctk.CTkEntry(wrapper, placeholder_text=placeholder, show="*" if is_pass else "", placeholder_text_color="#888", height=40, corner_radius=10, fg_color="white", border_width=0, text_color="black", font=ctk.CTkFont(size=14))
        entry.pack(fill="x")
        return entry

    def on_role_change(self, choice):
        for widget in self.dynamic_wrapper.winfo_children():
            widget.destroy()
        
        self.input_vars = {}

        if choice == "Student":
            # Image 2 implementation
            self.input_vars["username"] = self.create_field(self.dynamic_wrapper, "Username", "user", 0, 0, padx_r=8)
            self.input_vars["password"] = self.create_field(self.dynamic_wrapper, "Password", "••••", 0, 1, is_pass=True, padx_l=8)
            self.input_vars["name"] = self.create_field(self.dynamic_wrapper, "Full Name", "John Doe", 1, 0, columnspan=2)
            self.input_vars["email"] = self.create_field(self.dynamic_wrapper, "Email", "john@example.com", 2, 0, columnspan=2)
            self.input_vars["dept"] = self.create_field(self.dynamic_wrapper, "Department", "Computer Science", 3, 0, padx_r=8)
            self.input_vars["cgpa"] = self.create_field(self.dynamic_wrapper, "CGPA", "8.5", 3, 1, padx_l=8)

        else:
            # Image 3 implementation
            self.input_vars["username"] = self.create_field(self.dynamic_wrapper, "Username", "user", 0, 0, padx_r=8)
            self.input_vars["password"] = self.create_field(self.dynamic_wrapper, "Password", "••••", 0, 1, is_pass=True, padx_l=8)
            self.input_vars["name"] = self.create_field(self.dynamic_wrapper, "Company Name", "Acme Corp", 1, 0, columnspan=2)
            self.input_vars["industry"] = self.create_field(self.dynamic_wrapper, "Industry", "Technology", 2, 0, padx_r=8)
            self.input_vars["location"] = self.create_field(self.dynamic_wrapper, "Location", "New York, NY", 2, 1, padx_l=8)

    def handle_register(self):
        role = self.role_var.get()
        vals = {k: v.get().strip() for k, v in self.input_vars.items()}
        
        if not all(vals.values()):
            messagebox.showerror("Error", "Required fields missing!")
            return
            
        if role == "Student":
            res = AuthController.register_student(
                vals["username"], vals["password"], vals["name"],
                vals["email"], vals["dept"], vals["cgpa"]
            )
        else:
            res = AuthController.register_company(
                vals["username"], vals["password"], vals["name"],
                vals["industry"], vals["location"], vals["industry"]
            )

        if res['success']:
            messagebox.showinfo("Success", res['message'])
            self.app_controller.show_login()
        else:
            messagebox.showerror("Error", res['message'])
