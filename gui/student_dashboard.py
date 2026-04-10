import customtkinter as ctk
from logic.student_controller import StudentController
from tkinter import messagebox

class StudentDashboard(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        # Base Light Theme Canvas
        super().__init__(master, fg_color="#f4f6fa")
        self.app_controller = app_controller
        self.user_info = app_controller.current_user

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # -------------------------------------
        # LEFT SIDEBAR
        # -------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#15142d")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1) # Push logout to bottom
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Placement Cell", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40), sticky="w")

        # Sidebar Navigation Buttons
        self.btn_home = self.create_nav_button("⌂ Home", 1, lambda: self.show_page("home"))
        self.btn_jobs = self.create_nav_button("📄 Job Listings", 2, lambda: self.show_page("jobs"))
        self.btn_apps = self.create_nav_button("👥 View Applications", 3, lambda: self.show_page("apps"))
        self.btn_profile = self.create_nav_button("👤 My Profile", 4, lambda: self.show_page("profile"))
        

        # -------------------------------------
        # RIGHT MAIN AREA
        # -------------------------------------
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        # Top Header Bar
        self.header = ctk.CTkFrame(self.main_area, height=80, corner_radius=0, fg_color="white")
        self.header.grid(row=0, column=0, sticky="ew")
        
        header_text_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        header_text_frame.pack(side="left", padx=30, pady=20)
        ctk.CTkLabel(header_text_frame, text=f"Welcome back, {self.user_info['name']}", font=ctk.CTkFont(size=22, weight="bold"), text_color="#15142d").pack(anchor="w")
        ctk.CTkLabel(header_text_frame, text="You have new jobs waiting to be matched.", font=ctk.CTkFont(size=13), text_color="#7b7a8a").pack(anchor="w")

        r_btns = ctk.CTkFrame(self.header, fg_color="transparent")
        r_btns.pack(side="right", padx=30)
        ctk.CTkButton(r_btns, text="⎋ Log Out", width=100, height=35, corner_radius=18, fg_color="#8c52ff", hover_color="#5e1b9f", command=self.app_controller.logout).pack(side="left")

        # Page Container
        self.pages_container = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.pages_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.pages_container.grid_rowconfigure(0, weight=1)
        self.pages_container.grid_columnconfigure(0, weight=1)

        # Initialize Pages
        self.pages = {}
        self.build_home_page()
        self.build_jobs_page()
        self.build_apps_page()
        self.build_profile_page()

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

        # Load fresh stats
        jobs = StudentController.get_all_jobs()
        apps = StudentController.get_my_applications(self.user_info['id'])

        # Summary Cards
        self.create_summary_card(page, "Total Jobs", str(len(jobs)), "#7158fe", 0, 0)
        self.create_summary_card(page, "Applications", str(len(apps)), "#f64e60", 0, 1)
        self.create_summary_card(page, "Selections", str(len([a for a in apps if a['status']=='Selected'])), "#1bc5bd", 0, 2)
        self.create_summary_card(page, "Rejected", str(len([a for a in apps if a['status']=='Rejected'])), "#ffb822", 0, 3)

        # Mini Jobs Table
        table_container = ctk.CTkFrame(page, fg_color="white", corner_radius=8)
        table_container.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=(30, 0))
        table_container.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(table_container, text="Recent Jobs", font=ctk.CTkFont(size=18, weight="bold"), text_color="#15142d").pack(anchor="w", padx=20, pady=(20, 10))
        
        # Header Row
        hdr = ctk.CTkFrame(table_container, fg_color="#f8f9fa", height=40, corner_radius=0)
        hdr.pack(fill="x", padx=20)
        hdr.grid_columnconfigure((0,1,2), weight=1)
        ctk.CTkLabel(hdr, text="Job Title", font=ctk.CTkFont(size=12, weight="bold"), text_color="#15142d").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkLabel(hdr, text="Company", font=ctk.CTkFont(size=12, weight="bold"), text_color="#15142d").grid(row=0, column=1, sticky="w", padx=10, pady=10)
        ctk.CTkLabel(hdr, text="Salary", font=ctk.CTkFont(size=12, weight="bold"), text_color="#15142d").grid(row=0, column=2, sticky="w", padx=10, pady=10)

        # Rows
        for i, j in enumerate(jobs[:5]): # Show up to 5
            row_frame = ctk.CTkFrame(table_container, fg_color="white", height=50, corner_radius=0)
            row_frame.pack(fill="x", padx=20)
            row_frame.grid_columnconfigure((0,1,2), weight=1)
            # Add separation line
            if i > 0:
                ctk.CTkFrame(table_container, height=1, fg_color="#e2e5ec").pack(fill="x", padx=20)

            ctk.CTkLabel(row_frame, text=j['title'], text_color="#3f4254").grid(row=0, column=0, sticky="w", padx=10, pady=15)
            ctk.CTkLabel(row_frame, text=j['company_name'], text_color="#7b7a8a").grid(row=0, column=1, sticky="w", padx=10, pady=15)
            ctk.CTkLabel(row_frame, text=j['salary'], text_color="#7b7a8a").grid(row=0, column=2, sticky="w", padx=10, pady=15)

    def create_summary_card(self, parent, title, number, color, row, col):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
        ctk.CTkLabel(card, text=title, text_color="#3f4254", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
        ctk.CTkLabel(card, text=number, text_color=color, font=ctk.CTkFont(size=32, weight="bold")).pack(pady=(5, 20))

    # ==========================
    # PAGE: JOB LISTINGS
    # ==========================
    def build_jobs_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["jobs"] = page
        page.grid_rowconfigure(1, weight=1)
        page.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(page, text="All Job Listings", font=ctk.CTkFont(size=20, weight="bold"), text_color="#15142d").grid(row=0, column=0, sticky="w", pady=(0, 15))
        ctk.CTkButton(page, text="↺ Reload", width=100, height=30, corner_radius=8, fg_color="#8c52ff", hover_color="#5e1b9f", command=self.refresh_jobs).grid(row=0, column=0, sticky="e")

        self.jobs_frame = ctk.CTkScrollableFrame(page, corner_radius=10, fg_color="white")
        self.jobs_frame.grid(row=1, column=0, sticky="nsew")
        self.refresh_jobs()

    def refresh_jobs(self):
        for w in self.jobs_frame.winfo_children(): w.destroy()
        jobs = StudentController.get_all_jobs()
        my_apps = StudentController.get_my_applications(self.user_info['id'])
        applied_job_ids = [a['job_id'] for a in my_apps]

        for idx, j in enumerate(jobs):
            card = ctk.CTkFrame(self.jobs_frame, fg_color="#f8f9fa", corner_radius=8)
            card.pack(fill="x", pady=6, padx=10)
            
            ctk.CTkLabel(card, text=j['title'], text_color="#15142d", font=ctk.CTkFont(size=15, weight="bold")).pack(side="left", padx=15, pady=15)
            ctk.CTkLabel(card, text=f"{j['company_name']}  |  {j['salary']}  |  Openings: {j['vacancy']}", text_color="#7b7a8a").pack(side="left", padx=10)
            
            if j['id'] in applied_job_ids:
                ctk.CTkButton(card, text="Applied", width=100, height=32, corner_radius=16, fg_color="#1bc5bd", hover_color="#1bc5bd", text_color="white").pack(side="right", padx=15)
            else:
                ctk.CTkButton(card, text="Apply Now", width=100, height=32, corner_radius=16, fg_color="#8c52ff", hover_color="#5e1b9f",
                              command=lambda jid=j['id'], jt=j['title'], cn=j['company_name']: self.apply_job(jid, jt, cn)).pack(side="right", padx=15)

    def apply_job(self, job_id, job_title=None, company_name=None):
        apply_win = ctk.CTkToplevel(self)
        apply_win.title("Job Application")
        apply_win.geometry("600x750")
        apply_win.transient(self.winfo_toplevel())
        apply_win.grab_set()
        apply_win.configure(fg_color="#f4f6fa") # Main background color
        
        # Professional Header Bar
        header_frame = ctk.CTkFrame(apply_win, fg_color="#15142d", corner_radius=0, height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(header_frame, text=f"Apply for {job_title or 'Job'}", font=ctk.CTkFont(size=22, weight="bold"), text_color="white").pack(pady=(25, 5))
        if company_name:
            ctk.CTkLabel(header_frame, text=f"at {company_name}", font=ctk.CTkFont(size=14), text_color="#c8c7d4").pack(pady=(0, 25))
            
        scroll_frame = ctk.CTkScrollableFrame(apply_win, fg_color="transparent")
        scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)

        def create_card_section(parent, label_text, subtitle, is_textarea=False):
            card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
            card.pack(fill="x", pady=8, padx=10)
            
            ctk.CTkLabel(card, text=label_text, font=ctk.CTkFont(size=15, weight="bold"), text_color="#15142d").pack(anchor="w", padx=20, pady=(15, 2))
            if subtitle:
                ctk.CTkLabel(card, text=subtitle, font=ctk.CTkFont(size=12), text_color="#7b7a8a").pack(anchor="w", padx=20, pady=(0, 10))
                
            if is_textarea:
                entry = ctk.CTkTextbox(card, height=80, corner_radius=6, fg_color="#f4f6fa", border_width=1, border_color="#e2e5ec", text_color="black")
                entry.pack(fill="x", padx=20, pady=(0, 20))
            else:
                entry = ctk.CTkEntry(card, height=40, corner_radius=6, fg_color="#f4f6fa", border_width=1, border_color="#e2e5ec", text_color="black")
                entry.pack(fill="x", padx=20, pady=(0, 20))
            return entry

        def create_small_field(parent, label_text, placeholder):
            ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=13, weight="bold"), text_color="#15142d").pack(anchor="w", padx=20, pady=(10, 2))
            entry = ctk.CTkEntry(parent, height=40, corner_radius=6, fg_color="#f4f6fa", border_width=1, border_color="#e2e5ec", text_color="black", placeholder_text=placeholder)
            entry.pack(fill="x", padx=20, pady=(0, 10))
            return entry

        tech_skills = create_card_section(scroll_frame, "Technical Skills *", "e.g., Python, C++, HTML/CSS, MySQL", True)
        soft_skills = create_card_section(scroll_frame, "Soft Skills *", "e.g., Communication, Teamwork", False)
        experience = create_card_section(scroll_frame, "Experience *", "Internships, Projects, Hackathons", True)
        
        links_card = ctk.CTkFrame(scroll_frame, fg_color="white", corner_radius=10)
        links_card.pack(fill="x", pady=8, padx=10)
        ctk.CTkLabel(links_card, text="Online Presence", font=ctk.CTkFont(size=15, weight="bold"), text_color="#15142d").pack(anchor="w", padx=20, pady=(15, 5))
        
        linkedin = create_small_field(links_card, "LinkedIn URL *", "https://linkedin.com/in/...")
        github = create_small_field(links_card, "GitHub URL *", "https://github.com/...")
        portfolio = create_small_field(links_card, "Portfolio Website (Optional)", "https://...")
        
        ctk.CTkFrame(links_card, height=10, fg_color="transparent").pack()

        def submit_application():
            t_skills = tech_skills.get("1.0", "end-1c").strip()
            s_skills = soft_skills.get().strip()
            exp = experience.get("1.0", "end-1c").strip()
            ldin = linkedin.get().strip()
            ghub = github.get().strip()
            port = portfolio.get().strip()
            
            if not t_skills or not s_skills or not exp or not ldin or not ghub:
                messagebox.showerror("Validation Error", "Please fill in all mandatory fields marked with *")
                return
            
            desc = f"--- Technical Skills ---\n{t_skills}\n\n--- Soft Skills ---\n{s_skills}\n\n--- Experience ---\n{exp}\n\n--- Links ---\nLinkedIn: {ldin}\nGitHub: {ghub}\nPortfolio: {port if port else 'N/A'}"
            
            res = StudentController.apply_to_job(self.user_info['id'], job_id, desc)
            if res['success']:
                messagebox.showinfo("Success", res['message'])
                self.refresh_apps()
                apply_win.destroy()
            else:
                messagebox.showerror("Error", res['message'])
                
        # Footer for button
        footer = ctk.CTkFrame(apply_win, fg_color="transparent", height=80)
        footer.pack(fill="x", pady=10)
        ctk.CTkButton(footer, text="Submit Application", width=250, height=50, corner_radius=25, fg_color="#8c52ff", hover_color="#5e1b9f", font=ctk.CTkFont(size=16, weight="bold"), command=submit_application).pack(pady=10)

    # ==========================
    # PAGE: APPLIED JOBS
    # ==========================
    def build_apps_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["apps"] = page
        page.grid_rowconfigure(1, weight=1)
        page.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(page, text="My Applications", font=ctk.CTkFont(size=20, weight="bold"), text_color="#15142d").grid(row=0, column=0, sticky="w", pady=(0, 15))
        ctk.CTkButton(page, text="↺ Reload", width=100, height=30, corner_radius=8, fg_color="#8c52ff", hover_color="#5e1b9f", command=self.refresh_apps).grid(row=0, column=0, sticky="e")

        self.apps_frame = ctk.CTkScrollableFrame(page, corner_radius=10, fg_color="white")
        self.apps_frame.grid(row=1, column=0, sticky="nsew")
        self.refresh_apps()

    def refresh_apps(self):
        for w in self.apps_frame.winfo_children(): w.destroy()
        apps = StudentController.get_my_applications(self.user_info['id'])

        for idx, a in enumerate(apps):
            card = ctk.CTkFrame(self.apps_frame, fg_color="#f8f9fa", corner_radius=8)
            card.pack(fill="x", pady=6, padx=10)
            
            c_sts = "#1bc5bd" if a['status'] == 'Selected' else ("#f64e60" if a['status'] == 'Rejected' else "#ffb822")
            ctk.CTkLabel(card, text=f"■ {a['status'].upper()}", text_color=c_sts, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(15,10), pady=15)
            
            ctk.CTkLabel(card, text=a['title'], text_color="#15142d", font=ctk.CTkFont(size=15, weight="bold")).pack(side="left", padx=10)
            ctk.CTkLabel(card, text=f"at {a['company_name']}", text_color="#7b7a8a").pack(side="left", padx=5)

    # ==========================
    # PAGE: MY PROFILE
    # ==========================
    def build_profile_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["profile"] = page
        page.grid_rowconfigure(1, weight=1)
        page.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(page, text="My Profile", font=ctk.CTkFont(size=20, weight="bold"), text_color="#15142d").grid(row=0, column=0, sticky="w", pady=(0, 15))

        profile_frame = ctk.CTkFrame(page, corner_radius=15, fg_color="white")
        profile_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        
        # Profile Header
        header = ctk.CTkFrame(profile_frame, fg_color="#f8f9fa", height=100, corner_radius=15)
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header, text="👤", font=ctk.CTkFont(size=50)).pack(side="left", padx=20, pady=20)
        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.pack(side="left", padx=10, fill="y", pady=20)
        
        ctk.CTkLabel(info_frame, text=self.user_info['name'], font=ctk.CTkFont(size=22, weight="bold"), text_color="#15142d").pack(anchor="w")
        ctk.CTkLabel(info_frame, text="Student Account", font=ctk.CTkFont(size=14), text_color="#8c52ff").pack(anchor="w")

        # Profile Details
        details_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
        details_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        profile_data = StudentController.get_student_profile(self.user_info['id'])
        if not profile_data:
            ctk.CTkLabel(details_frame, text="Profile information could not be loaded.", text_color="red").pack(anchor="w")
            return

        def add_detail_row(label, val):
            row = ctk.CTkFrame(details_frame, fg_color="transparent")
            row.pack(fill="x", pady=15)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=14, weight="bold"), text_color="#7b7a8a", width=150, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=val if val else "Not provided", font=ctk.CTkFont(size=15), text_color="#15142d").pack(side="left")
            ctk.CTkFrame(details_frame, height=1, fg_color="#e2e5ec").pack(fill="x")

        add_detail_row("Username:", profile_data.get('username'))
        add_detail_row("Full Name:", profile_data.get('name'))
        add_detail_row("Department:", profile_data.get('dept'))
        add_detail_row("CGPA:", str(profile_data.get('cgpa')))
        add_detail_row("Contact Number:", profile_data.get('phone'))
