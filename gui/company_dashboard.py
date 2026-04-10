import customtkinter as ctk
from logic.company_controller import CompanyController
from tkinter import messagebox

class CompanyDashboard(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="#f4f6fa")
        self.app_controller = app_controller
        self.user_info = app_controller.current_user

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=220) # Fixed sidebar
        self.grid_columnconfigure(1, weight=1)

        # -------------------------------------
        # LEFT SIDEBAR
        # -------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#15142d")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Placement Cell", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40), sticky="w")

        self.btn_home = self.create_nav_button("⌂ Home", 1, lambda: self.show_page("home"))
        self.btn_post = self.create_nav_button("➕ Post Job", 2, lambda: self.show_page("post"))
        self.btn_jobs = self.create_nav_button("📄 My Jobs", 3, lambda: self.show_page("jobs"))
        self.btn_apps = self.create_nav_button("👥 View Applicants", 4, lambda: self.show_page("apps"))

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
        ctk.CTkLabel(header_text_frame, text="Manage your recruitment pipeline", font=ctk.CTkFont(size=13), text_color="#7b7a8a").pack(anchor="w")

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
        self.build_post_page()
        self.build_jobs_page()
        self.build_apps_page()
        
        self.refresh_all()

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

        jobs = CompanyController.get_my_jobs(self.user_info['id'])
        apps = CompanyController.get_applicants(self.user_info['id'])

        # Summary Cards
        self.create_summary_card(page, "Total Jobs", str(len(jobs)), "#7158fe", 0, 0)
        self.create_summary_card(page, "Total Applicants", str(len(apps)), "#f64e60", 0, 1)
        self.create_summary_card(page, "Hired", str(len([a for a in apps if a['status']=='Selected'])), "#1bc5bd", 0, 2)
        self.create_summary_card(page, "Rejected", str(len([a for a in apps if a['status']=='Rejected'])), "#ffb822", 0, 3)

        table_cont = ctk.CTkFrame(page, fg_color="white", corner_radius=8)
        table_cont.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=(30, 0))
        table_cont.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(table_cont, text="Recent Applicants", font=ctk.CTkFont(size=18, weight="bold"), text_color="#15142d").pack(anchor="w", padx=20, pady=(20, 10))
        
        hdr = ctk.CTkFrame(table_cont, fg_color="#f8f9fa", height=40, corner_radius=0)
        hdr.pack(fill="x", padx=20)
        hdr.grid_columnconfigure((0,1,2), weight=1)
        ctk.CTkLabel(hdr, text="Applicant", font=ctk.CTkFont(size=12, weight="bold"), text_color="#15142d").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkLabel(hdr, text="Job Applied", font=ctk.CTkFont(size=12, weight="bold"), text_color="#15142d").grid(row=0, column=1, sticky="w", padx=10, pady=10)
        ctk.CTkLabel(hdr, text="Status", font=ctk.CTkFont(size=12, weight="bold"), text_color="#15142d").grid(row=0, column=2, sticky="w", padx=10, pady=10)

        for i, a in enumerate(apps[:5]):
            row_frame = ctk.CTkFrame(table_cont, fg_color="white", height=50, corner_radius=0)
            row_frame.pack(fill="x", padx=20)
            row_frame.grid_columnconfigure((0,1,2), weight=1)
            if i > 0: ctk.CTkFrame(table_cont, height=1, fg_color="#e2e5ec").pack(fill="x", padx=20)
            
            ctk.CTkLabel(row_frame, text=f"{a['student_name']} (CGPA: {a['cgpa']})", text_color="#3f4254").grid(row=0, column=0, sticky="w", padx=10, pady=15)
            ctk.CTkLabel(row_frame, text=a['title'], text_color="#7b7a8a").grid(row=0, column=1, sticky="w", padx=10, pady=15)
            ctk.CTkLabel(row_frame, text=a['status'], text_color="#1bc5bd" if a['status']=="Selected" else "#ffb822").grid(row=0, column=2, sticky="w", padx=10, pady=15)

    def create_summary_card(self, parent, title, number, color, row, col):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
        ctk.CTkLabel(card, text=title, text_color="#3f4254", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
        ctk.CTkLabel(card, text=number, text_color=color, font=ctk.CTkFont(size=32, weight="bold")).pack(pady=(5, 20))

    # ==========================
    # PAGE: POST JOB
    # ==========================
    def build_post_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["post"] = page
        page.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(page, text="Post New Job", font=ctk.CTkFont(size=20, weight="bold"), text_color="#15142d").grid(row=0, column=0, sticky="w", pady=(0, 15))

        form = ctk.CTkFrame(page, fg_color="white", corner_radius=15)
        form.grid(row=1, column=0, sticky="nsew", pady=10)

        ctk.CTkLabel(form, text="Job Title", text_color="#15142d", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(25, 5), anchor="w", padx=40)
        self.j_title = ctk.CTkEntry(form, width=350, height=45, corner_radius=8, fg_color="#f4f6fa", border_width=1, border_color="#e2e5ec", text_color="black")
        self.j_title.pack(pady=5, padx=40, anchor="w")

        ctk.CTkLabel(form, text="Salary Package", text_color="#15142d", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(15, 5), anchor="w", padx=40)
        self.j_salary = ctk.CTkEntry(form, width=350, height=45, corner_radius=8, fg_color="#f4f6fa", border_width=1, border_color="#e2e5ec", text_color="black")
        self.j_salary.pack(pady=5, padx=40, anchor="w")

        ctk.CTkLabel(form, text="Total Vacancies", text_color="#15142d", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(15, 5), anchor="w", padx=40)
        self.j_vac = ctk.CTkEntry(form, width=350, height=45, corner_radius=8, fg_color="#f4f6fa", border_width=1, border_color="#e2e5ec", text_color="black")
        self.j_vac.pack(pady=5, padx=40, anchor="w")

        ctk.CTkButton(form, text="Publish Job", width=180, height=45, corner_radius=8, fg_color="#8c52ff", hover_color="#5e1b9f", font=ctk.CTkFont(size=14, weight="bold"), command=self.post_job).pack(pady=(35, 30), anchor="w", padx=40)

    def post_job(self):
        res = CompanyController.create_job(self.user_info['id'], self.j_title.get(), self.j_salary.get(), int(self.j_vac.get() or 1))
        if res['success']:
            messagebox.showinfo("Success", res['message'])
            self.j_title.delete(0, 'end'); self.j_salary.delete(0, 'end'); self.j_vac.delete(0, 'end')
            self.refresh_all()
        else:
            messagebox.showerror("Error", res['message'])

    # ==========================
    # PAGE: MY JOBS
    # ==========================
    def build_jobs_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["jobs"] = page
        page.grid_rowconfigure(1, weight=1); page.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(page, text="My Jobs", font=ctk.CTkFont(size=20, weight="bold"), text_color="#15142d").grid(row=0, column=0, sticky="w", pady=(0, 15))
        ctk.CTkButton(page, text="↺ Reload", width=100, height=30, corner_radius=8, fg_color="#8c52ff", hover_color="#5e1b9f", command=self.refresh_all).grid(row=0, column=0, sticky="e")

        self.jobs_frame = ctk.CTkScrollableFrame(page, corner_radius=10, fg_color="white")
        self.jobs_frame.grid(row=1, column=0, sticky="nsew")

    # ==========================
    # PAGE: VIEW APPLICANTS
    # ==========================
    def build_apps_page(self):
        page = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.pages["apps"] = page
        page.grid_rowconfigure(1, weight=1); page.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(page, text="Applicants Tracking", font=ctk.CTkFont(size=20, weight="bold"), text_color="#15142d").grid(row=0, column=0, sticky="w", pady=(0, 15))
        ctk.CTkButton(page, text="↺ Reload", width=100, height=30, corner_radius=8, fg_color="#8c52ff", hover_color="#5e1b9f", command=self.refresh_all).grid(row=0, column=0, sticky="e")

        self.apps_frame = ctk.CTkScrollableFrame(page, corner_radius=10, fg_color="white")
        self.apps_frame.grid(row=1, column=0, sticky="nsew")

    def refresh_all(self):
        # Refresh Jobs
        for w in self.jobs_frame.winfo_children(): w.destroy()
        jobs = CompanyController.get_my_jobs(self.user_info['id'])
        if not jobs:
            ctk.CTkLabel(self.jobs_frame, text="You haven't posted any jobs yet.", text_color="#7b7a8a", font=ctk.CTkFont(size=15, slant="italic")).pack(pady=40)
        else:
            for j in jobs:
                card = ctk.CTkFrame(self.jobs_frame, fg_color="#f8f9fa", corner_radius=8)
                card.pack(fill="x", pady=6, padx=10)
                ctk.CTkLabel(card, text=j['title'], text_color="#15142d", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=15, pady=15)
                ctk.CTkLabel(card, text=f"Salary: {j['salary']}  |  Openings: {j['vacancy']}", text_color="#7b7a8a").pack(side="left", padx=10)
                ctk.CTkButton(card, text="🗑 Delete", width=80, height=32, corner_radius=16, fg_color="#f64e60", hover_color="#c83f4f",
                              command=lambda jid=j['id']: self.delete_job(jid)).pack(side="right", padx=15)

        # Refresh Applicants
        for w in self.apps_frame.winfo_children(): w.destroy()
        apps = CompanyController.get_applicants(self.user_info['id'])
        if not apps:
            ctk.CTkLabel(self.apps_frame, text="No one has applied to your jobs yet.", text_color="#7b7a8a", font=ctk.CTkFont(size=15, slant="italic")).pack(pady=40)
        else:
            for a in apps:
                card = ctk.CTkFrame(self.apps_frame, fg_color="#f8f9fa", corner_radius=8)
                card.pack(fill="x", pady=6, padx=10)
                c = "#1bc5bd" if a['status'] == 'Selected' else ("#f64e60" if a['status'] == 'Rejected' else "#ffb822")
                ctk.CTkLabel(card, text=f"■ {a['status'].upper()}", text_color=c, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(15, 10), pady=15)
                ctk.CTkLabel(card, text=f"{a['student_name']} ({a['cgpa']}) -> {a['title']}", text_color="#15142d", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=5)
                
                ctk.CTkButton(card, text="🔍 View", width=70, height=32, corner_radius=16, fg_color="#3b3a5a", hover_color="#2a294a",
                              command=lambda app=a: self.view_applicant(app)).pack(side="right", padx=10)
                
                if a['status'] == 'Applied':
                    ctk.CTkButton(card, text="✕ Reject", width=80, height=32, corner_radius=16, fg_color="#f64e60", hover_color="#c83f4f",
                                  command=lambda pid=a['placement_id']: self.update_status(pid, 'Rejected')).pack(side="right", padx=15)
                    ctk.CTkButton(card, text="✓ Hire", width=80, height=32, corner_radius=16, fg_color="#1bc5bd", hover_color="#15a09a",
                                  command=lambda pid=a['placement_id']: self.update_status(pid, 'Selected')).pack(side="right", padx=5)

    def delete_job(self, job_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this job?"):
            res = CompanyController.delete_job(self.user_info['id'], job_id)
            if res['success']:
                messagebox.showinfo("Success", res['message'])
                self.refresh_all()
            else:
                messagebox.showerror("Error", res['message'])
                
    def update_status(self, placement_id, status):
        res = CompanyController.update_placement_status(self.user_info['id'], placement_id, status)
        if res['success']:
            messagebox.showinfo("Success", res['message'])
            self.refresh_all()
        else:
            messagebox.showerror("Error", res['message'])
            
    def view_applicant(self, app):
        win = ctk.CTkToplevel(self)
        win.title("Applicant Profile")
        win.geometry("500x550")
        win.transient(self.winfo_toplevel())
        win.grab_set()
        win.configure(fg_color="#f4f6fa")
        
        hdr = ctk.CTkFrame(win, fg_color="#15142d", height=100, corner_radius=0)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=app['student_name'], font=ctk.CTkFont(size=22, weight="bold"), text_color="white").pack(pady=(20, 0))
        ctk.CTkLabel(hdr, text=f"Applicant for {app['title']}", font=ctk.CTkFont(size=14), text_color="#c8c7d4").pack(pady=(5, 20))
        
        main_f = ctk.CTkFrame(win, fg_color="white", corner_radius=10)
        main_f.pack(fill="both", expand=True, padx=20, pady=20)
        
        def add_row(lbl, val):
            row = ctk.CTkFrame(main_f, fg_color="transparent")
            row.pack(fill="x", pady=10, padx=20)
            ctk.CTkLabel(row, text=lbl, width=120, anchor="w", font=ctk.CTkFont(size=13, weight="bold"), text_color="#15142d").pack(side="left")
            ctk.CTkLabel(row, text=val if val else "Not provided", font=ctk.CTkFont(size=13), text_color="#7b7a8a").pack(side="left", fill="x", expand=True)

        add_row("Department:", app.get('dept'))
        add_row("CGPA:", app.get('cgpa'))
        add_row("Email:", app.get('email'))
        add_row("Phone:", app.get('phone'))
        
        ctk.CTkLabel(main_f, text="Applicant Full Profile & Skills:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#15142d").pack(anchor="w", padx=20, pady=(15, 5))
        txt = ctk.CTkTextbox(main_f, height=250, fg_color="#f4f6fa", text_color="black")
        txt.pack(fill="x", padx=20, pady=(0, 20))
        txt.insert("0.0", app.get('description', 'No description provided.'))
        txt.configure(state="disabled")
