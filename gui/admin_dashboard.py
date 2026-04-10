import customtkinter as ctk
from logic.admin_controller import AdminController
from logic.auth_controller import AuthController
from tkinter import messagebox

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="#f4f6fa")
        self.app_controller = app_controller
        self.user_info = app_controller.current_user

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=220)
        self.grid_columnconfigure(1, weight=1)

        # -------------------------------------
        # LEFT SIDEBAR
        # -------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#15142d")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Placement Cell", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40), sticky="w")

        self.btn_home = self.create_nav_button("⌂ Home", 1, lambda: self.show_page("home"))
        self.btn_users = self.create_nav_button("👥 View Users", 2, lambda: self.show_page("users"))
        self.btn_add_st = self.create_nav_button("➕ Add Student", 3, lambda: self.show_page("add_student"))
        self.btn_add_co = self.create_nav_button("➕ Add Company", 4, lambda: self.show_page("add_company"))
        self.btn_create_job = self.create_nav_button("💼 Create Job", 5, lambda: self.show_page("create_job"))

        # -------------------------------------
        # RIGHT MAIN AREA
        # -------------------------------------
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self.main_area, height=80, corner_radius=0, fg_color="white")
        self.header.grid(row=0, column=0, sticky="ew")
        
        header_text_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        header_text_frame.pack(side="left", padx=30, pady=20)
        ctk.CTkLabel(header_text_frame, text=f"Welcome back, {self.user_info['name']}", font=ctk.CTkFont(size=22, weight="bold"), text_color="#15142d").pack(anchor="w")
        ctk.CTkLabel(header_text_frame, text="System Administrator Dashboard", font=ctk.CTkFont(size=13), text_color="#7b7a8a").pack(anchor="w")

        r_btns = ctk.CTkFrame(self.header, fg_color="transparent")
        r_btns.pack(side="right", padx=30)
        ctk.CTkButton(r_btns, text="⎋ Log Out", width=100, height=35, corner_radius=18, fg_color="#8c52ff", hover_color="#5e1b9f", command=self.app_controller.logout).pack(side="left")

        # Page Container
        self.pages_container = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.pages_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.pages_container.grid_rowconfigure(0, weight=1)
        self.pages_container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        self.build_home_page()
        self.build_users_page()
        self.build_add_student_page()
        self.build_add_company_page()
        self.build_create_job_page()
        
        self.refresh_company_list()

        self.show_page("home")

    def create_nav_button(self, text, row, cmd):
        btn = ctk.CTkButton(self.sidebar_frame, text=text, width=220, height=45, corner_radius=0, 
                            fg_color="transparent", hover_color="#2b2a4a", text_color="#c8c7d4", 
                            font=ctk.CTkFont(size=14), anchor="w", command=cmd)
        btn.grid(row=row, column=0, sticky="ew")
        return btn

    def show_page(self, page_name):
        for frame in self.pages.values():
            frame.grid_forget()
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")

    # ==========================
    # PAGE: HOME
    # ==========================
    def build_home_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["home"] = page
        page.grid_columnconfigure((0,1,2,3), weight=1)

        users = AdminController.get_all_users()

        # Summary Cards
        self.create_summary_card(page, "Total Users", str(len(users)), "#7158fe", 0, 0)
        self.create_summary_card(page, "Total Students", str(len([u for u in users if u['role_name'] == 'Student'])), "#f64e60", 0, 1)
        self.create_summary_card(page, "Total Companies", str(len([u for u in users if u['role_name'] == 'Company'])), "#ffb822", 0, 2)
        self.create_summary_card(page, "Active Admins", str(len([u for u in users if u['role_name'] == 'Admin'])), "#1bc5bd", 0, 3)

        table_cont = ctk.CTkFrame(page, fg_color="white", corner_radius=8)
        table_cont.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=(30, 0))
        table_cont.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(table_cont, text="System User Ledger", font=ctk.CTkFont(size=18, weight="bold"), text_color="#15142d").pack(anchor="w", padx=20, pady=(20, 10))
        
        hdr = ctk.CTkFrame(table_cont, fg_color="#f8f9fa", height=40, corner_radius=0)
        hdr.pack(fill="x", padx=20)
        hdr.grid_columnconfigure((0,1,2), weight=1)
        ctk.CTkLabel(hdr, text="Username", font=ctk.CTkFont(size=12, weight="bold"), text_color="#15142d").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkLabel(hdr, text="Full Name", font=ctk.CTkFont(size=12, weight="bold"), text_color="#15142d").grid(row=0, column=1, sticky="w", padx=10, pady=10)
        ctk.CTkLabel(hdr, text="Role", font=ctk.CTkFont(size=12, weight="bold"), text_color="#15142d").grid(row=0, column=2, sticky="w", padx=10, pady=10)

        for i, u in enumerate(users[-5:]): # show 5 most recent
            row_frame = ctk.CTkFrame(table_cont, fg_color="white", height=50, corner_radius=0)
            row_frame.pack(fill="x", padx=20)
            row_frame.grid_columnconfigure((0,1,2), weight=1)
            if i > 0: ctk.CTkFrame(table_cont, height=1, fg_color="#e2e5ec").pack(fill="x", padx=20)
            
            ctk.CTkLabel(row_frame, text=u['username'], text_color="#3f4254").grid(row=0, column=0, sticky="w", padx=10, pady=15)
            ctk.CTkLabel(row_frame, text=u['name'], text_color="#7b7a8a").grid(row=0, column=1, sticky="w", padx=10, pady=15)
            ctk.CTkLabel(row_frame, text=u['role_name'], text_color="#8c52ff").grid(row=0, column=2, sticky="w", padx=10, pady=15)

    def create_summary_card(self, parent, title, number, color, row, col):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
        ctk.CTkLabel(card, text=title, text_color="#3f4254", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
        ctk.CTkLabel(card, text=number, text_color=color, font=ctk.CTkFont(size=32, weight="bold")).pack(pady=(5, 20))

    def refresh_company_list(self):
        comps = AdminController.get_all_companies()
        c_vals = [f"{c['id']} - {c['name']}" for c in comps] if comps else ["No Companies"]
        try:
            self.cj_company.configure(values=c_vals)
            if c_vals: self.cj_company.set(c_vals[0])
        except AttributeError:
            pass

    # ==========================
    # PAGE: VIEW USERS
    # ==========================
    def build_users_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["users"] = page
        page.grid_rowconfigure(1, weight=1); page.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(page, text="All System Users", font=ctk.CTkFont(size=20, weight="bold"), text_color="#15142d").grid(row=0, column=0, sticky="w", pady=(0, 15))
        ctk.CTkButton(page, text="↺ Reload", width=100, height=30, corner_radius=8, fg_color="#8c52ff", hover_color="#5e1b9f", command=self.refresh_users).grid(row=0, column=0, sticky="e")

        self.users_frame = ctk.CTkScrollableFrame(page, corner_radius=10, fg_color="white")
        self.users_frame.grid(row=1, column=0, sticky="nsew")
        self.refresh_users()

    def refresh_users(self):
        for w in self.users_frame.winfo_children(): w.destroy()
        users = AdminController.get_all_users()
        for idx, u in enumerate(users):
            card = ctk.CTkFrame(self.users_frame, fg_color="#f8f9fa", corner_radius=8)
            card.pack(fill="x", pady=6, padx=10)
            
            ctk.CTkLabel(card, text=f"[{u['role_name'].upper()}]", text_color="#15142d", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=15, pady=15)
            ctk.CTkLabel(card, text=f"Username: {u['username']}  |  Name: {u['name']}", text_color="#7b7a8a").pack(side="left", padx=10)

    # ==========================
    # PAGE: ADD STUDENT
    # ==========================
    def build_add_student_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["add_student"] = page
        
        ctk.CTkLabel(page, text="Register New Student", font=ctk.CTkFont(size=20, weight="bold"), text_color="#15142d").pack(anchor="w", pady=(0, 15))
        
        scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        form = ctk.CTkFrame(scroll, fg_color="white", corner_radius=15)
        form.pack(fill="x", pady=10)
        
        def create_entry(label_text, placeholder="", is_password=False):
            ctk.CTkLabel(form, text=label_text, text_color="#15142d", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(15, 5), anchor="w", padx=40)
            entry = ctk.CTkEntry(form, width=350, height=45, corner_radius=8, fg_color="#f4f6fa", border_width=1, border_color="#e2e5ec", text_color="black", placeholder_text=placeholder, show="*" if is_password else "")
            entry.pack(pady=5, padx=40, anchor="w")
            return entry

        ent_name = create_entry("Full Name", "e.g., John Doe")
        ent_dept = create_entry("Department", "e.g., Computer Science")
        ent_cgpa = create_entry("CGPA", "e.g., 8.5")
        ent_phone = create_entry("Phone Number", "e.g., +1234567890")
        ent_user = create_entry("Login Username", "student_login_id")
        ent_pass = create_entry("Password", "Secret passcode", True)
        
        def submit():
            name = ent_name.get().strip()
            dept = ent_dept.get().strip()
            cgpa_str = ent_cgpa.get().strip()
            phone = ent_phone.get().strip()
            uname = ent_user.get().strip()
            pwd = ent_pass.get()
            
            if not all([name, dept, cgpa_str, phone, uname, pwd]):
                messagebox.showerror("Error", "All fields are required")
                return
            try:
                cgpa = float(cgpa_str)
            except ValueError:
                messagebox.showerror("Error", "CGPA must be a valid number")
                return
                
            res = AuthController.register_student(uname, pwd, name, phone, dept, cgpa)
            if res['success']:
                messagebox.showinfo("Success", res['message'])
                ent_name.delete(0, 'end'); ent_dept.delete(0, 'end'); ent_cgpa.delete(0, 'end')
                ent_phone.delete(0, 'end'); ent_user.delete(0, 'end'); ent_pass.delete(0, 'end')
                self.refresh_users()
                self.refresh_company_list()
            else:
                messagebox.showerror("Error", res['message'])
                
        ctk.CTkButton(form, text="Create Student", width=200, height=45, corner_radius=8, fg_color="#f64e60", hover_color="#c83f4f", font=ctk.CTkFont(size=14, weight="bold"), command=submit).pack(pady=(30, 30), anchor="w", padx=40)

    # ==========================
    # PAGE: ADD COMPANY
    # ==========================
    def build_add_company_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["add_company"] = page
        
        ctk.CTkLabel(page, text="Register New Company", font=ctk.CTkFont(size=20, weight="bold"), text_color="#15142d").pack(anchor="w", pady=(0, 15))
        
        scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        form = ctk.CTkFrame(scroll, fg_color="white", corner_radius=15)
        form.pack(fill="x", pady=10)
        
        def create_entry(label_text, placeholder="", is_password=False):
            ctk.CTkLabel(form, text=label_text, text_color="#15142d", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(15, 5), anchor="w", padx=40)
            entry = ctk.CTkEntry(form, width=350, height=45, corner_radius=8, fg_color="#f4f6fa", border_width=1, border_color="#e2e5ec", text_color="black", placeholder_text=placeholder, show="*" if is_password else "")
            entry.pack(pady=5, padx=40, anchor="w")
            return entry

        ent_name = create_entry("Company Name", "e.g., Tech Corp")
        ent_location = create_entry("Location", "e.g., New York, NY")
        ent_contact = create_entry("Contact Email/Person", "e.g., hr@techcorp.com")
        ent_phone = create_entry("Official Phone Number", "e.g., +1234567890")
        ent_user = create_entry("Company Login Username", "company_login")
        ent_pass = create_entry("Password", "Secret passcode", True)
        
        def submit():
            name = ent_name.get().strip()
            loc = ent_location.get().strip()
            contact = ent_contact.get().strip()
            phone = ent_phone.get().strip()
            uname = ent_user.get().strip()
            pwd = ent_pass.get()
            
            if not all([name, loc, contact, phone, uname, pwd]):
                messagebox.showerror("Error", "All fields are required")
                return
                
            res = AuthController.register_company(uname, pwd, name, phone, loc, contact)
            if res['success']:
                messagebox.showinfo("Success", res['message'])
                ent_name.delete(0, 'end'); ent_location.delete(0, 'end'); ent_contact.delete(0, 'end')
                ent_phone.delete(0, 'end'); ent_user.delete(0, 'end'); ent_pass.delete(0, 'end')
                self.refresh_users()
                self.refresh_company_list()
            else:
                messagebox.showerror("Error", res['message'])
                
        ctk.CTkButton(form, text="Create Company", width=200, height=45, corner_radius=8, fg_color="#ffb822", hover_color="#c98d00", font=ctk.CTkFont(size=14, weight="bold"), command=submit).pack(pady=(30, 30), anchor="w", padx=40)

    # ==========================
    # PAGE: CREATE JOB
    # ==========================
    def build_create_job_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["create_job"] = page
        
        ctk.CTkLabel(page, text="Create Job Posting", font=ctk.CTkFont(size=20, weight="bold"), text_color="#15142d").pack(anchor="w", pady=(0, 15))
        
        scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        form = ctk.CTkFrame(scroll, fg_color="white", corner_radius=15)
        form.pack(fill="x", pady=10)
        
        ctk.CTkLabel(form, text="Select Hosting Company", text_color="#15142d", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(25, 5), anchor="w", padx=40)
        self.cj_company = ctk.CTkComboBox(form, values=["Loading..."], width=350, height=45, corner_radius=8, fg_color="#f4f6fa", border_width=1, border_color="#e2e5ec", button_color="#15142d", text_color="black")
        self.cj_company.pack(pady=5, padx=40, anchor="w")

        def create_entry(label_text, placeholder=""):
            ctk.CTkLabel(form, text=label_text, text_color="#15142d", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(15, 5), anchor="w", padx=40)
            entry = ctk.CTkEntry(form, width=350, height=45, corner_radius=8, fg_color="#f4f6fa", border_width=1, border_color="#e2e5ec", text_color="black", placeholder_text=placeholder)
            entry.pack(pady=5, padx=40, anchor="w")
            return entry

        ent_title = create_entry("Job Title", "e.g., Software Engineer")
        ent_salary = create_entry("Salary", "e.g., $100k - $120k")
        ent_vacancy = create_entry("Vacancy Count", "e.g., 5")
        
        def submit():
            c_val = self.cj_company.get()
            if "No" in c_val or "Loading" in c_val:
                messagebox.showerror("Error", "Invalid company selection")
                return
            company_id = int(c_val.split(" - ")[0])
            title = ent_title.get().strip()
            salary = ent_salary.get().strip()
            vac_str = ent_vacancy.get().strip()
            
            if not all([title, salary, vac_str]):
                messagebox.showerror("Error", "All fields are required")
                return
            try:
                vacancy = int(vac_str)
                if vacancy <= 0: raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Vacancy must be a positive integer")
                return
                
            res = AdminController.create_job(self.user_info['id'], company_id, title, salary, vacancy)
            if res['success']:
                messagebox.showinfo("Success", res['message'])
                ent_title.delete(0, 'end'); ent_salary.delete(0, 'end'); ent_vacancy.delete(0, 'end')
                pass
            else:
                messagebox.showerror("Error", res['message'])
                
        ctk.CTkButton(form, text="Publish Job", width=200, height=45, corner_radius=8, fg_color="#1bc5bd", hover_color="#15a09a", font=ctk.CTkFont(size=14, weight="bold"), command=submit).pack(pady=(30, 30), anchor="w", padx=40)
