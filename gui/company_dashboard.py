import customtkinter as ctk
from logic.company_controller import CompanyController
from tkinter import messagebox

class CompanyDashboard(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="#181a2e")
        self.app_controller = app_controller
        self.user_info = app_controller.current_user

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color="#1d1e2b")
        self.header.grid(row=0, column=0, sticky="ew")
        
        self.welcome_label = ctk.CTkLabel(self.header, text=f"Company Dashboard - {self.user_info['name']}", text_color="white", font=ctk.CTkFont(family="Inter", size=22, weight="bold"))
        self.welcome_label.pack(side="left", padx=20, pady=20)
        
        self.logout_btn = ctk.CTkButton(self.header, text="Logout", width=100, height=35, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white", command=self.app_controller.logout)
        self.logout_btn.pack(side="right", padx=20, pady=15)

        self.tabview = ctk.CTkTabview(self, fg_color="#181a2e", segmented_button_fg_color="#222433", segmented_button_selected_color="#8c52ff", segmented_button_selected_hover_color="#5e1b9f", text_color="white")
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.tabview.add("Post Job")
        self.tabview.add("My Jobs")
        self.tabview.add("View Applicants")
        
        self.setup_post_job()
        self.setup_my_jobs()
        self.setup_view_applicants()

    def setup_post_job(self):
        tab = self.tabview.tab("Post Job")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(2, weight=1)

        form = ctk.CTkFrame(tab, fg_color="#2b304c", corner_radius=15, border_width=1, border_color="#3e4368")
        form.grid(row=0, column=1, pady=30, padx=40)
        
        ctk.CTkLabel(form, text="Create New Job Posting", text_color="white", font=ctk.CTkFont(family="Inter", size=20, weight="bold")).pack(pady=(25, 20))

        ctk.CTkLabel(form, text="Job Title", text_color="white", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(5, 0), anchor="w", padx=40)
        self.j_title = ctk.CTkEntry(form, width=280, height=40, corner_radius=8, fg_color="#222433", border_color="#484b6a", text_color="white")
        self.j_title.pack(pady=5, padx=40)

        ctk.CTkLabel(form, text="Salary Package", text_color="white", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(5, 0), anchor="w", padx=40)
        self.j_salary = ctk.CTkEntry(form, width=280, height=40, corner_radius=8, fg_color="#222433", border_color="#484b6a", text_color="white")
        self.j_salary.pack(pady=5, padx=40)

        ctk.CTkLabel(form, text="Total Vacancies", text_color="white", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(5, 0), anchor="w", padx=40)
        self.j_vac = ctk.CTkEntry(form, width=280, height=40, corner_radius=8, fg_color="#222433", border_color="#484b6a", text_color="white")
        self.j_vac.pack(pady=5, padx=40)

        ctk.CTkButton(form, text="Launch Job Posting", width=280, height=40, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), command=self.post_job).pack(pady=(25, 25))

    def post_job(self):
        res = CompanyController.create_job(
            self.user_info['id'], self.j_title.get(), self.j_salary.get(), int(self.j_vac.get() or 1)
        )
        if res['success']:
            messagebox.showinfo("Success", res['message'])
            self.j_title.delete(0, 'end')
            self.j_salary.delete(0, 'end')
            self.j_vac.delete(0, 'end')
            self.load_my_jobs()
        else:
            messagebox.showerror("Error", res['message'])

    def setup_my_jobs(self):
        tab = self.tabview.tab("My Jobs")
        self.jobs_frame = ctk.CTkScrollableFrame(tab, corner_radius=15, fg_color="#2b304c", border_width=1, border_color="#3e4368")
        self.jobs_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=20)
        ctk.CTkButton(header_frame, text="↺ Refresh List", width=120, height=35, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white", command=self.load_my_jobs).pack(side="right", pady=10)
        
        self.load_my_jobs()

    def load_my_jobs(self):
        for w in self.jobs_frame.winfo_children():
            w.destroy()
        
        jobs = CompanyController.get_my_jobs(self.user_info['id'])
        for idx, j in enumerate(jobs):
            card = ctk.CTkFrame(self.jobs_frame, fg_color="#3A3C56", corner_radius=8)
            card.pack(fill="x", pady=5, padx=10)
            
            text = f"{j['title']}   |   Salary: {j['salary']}   |   Vacancies: {j['vacancy']}"
            lbl = ctk.CTkLabel(card, text=text, font=ctk.CTkFont(size=13, weight="bold"), text_color="white")
            lbl.pack(side="left", padx=15, pady=15)

    def setup_view_applicants(self):
        tab = self.tabview.tab("View Applicants")
        self.apps_frame = ctk.CTkScrollableFrame(tab, corner_radius=15, fg_color="#2b304c", border_width=1, border_color="#3e4368")
        self.apps_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=20)
        ctk.CTkButton(header_frame, text="↺ Refresh List", width=120, height=35, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white", command=self.load_applicants).pack(side="right", pady=10)
        
        self.load_applicants()

    def load_applicants(self):
        for w in self.apps_frame.winfo_children():
            w.destroy()
        
        apps = CompanyController.get_applicants(self.user_info['id'])
        for idx, a in enumerate(apps):
            card = ctk.CTkFrame(self.apps_frame, fg_color="#3A3C56", corner_radius=8)
            card.pack(fill="x", pady=5, padx=10)
            
            # Simple color mapping for statuses
            status_color = "#32CD32" if a['status'] == 'Selected' else ("#FF4C4C" if a['status'] == 'Rejected' else "#FFA500")
            
            ctk.CTkLabel(card, text=f"■ {a['status'].upper()}", text_color=status_color, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(15, 10), pady=15)
            
            text = f"{a['student_name']} (CGPA: {a['cgpa']}) applied to {a['title']}"
            lbl = ctk.CTkLabel(card, text=text, font=ctk.CTkFont(size=13), text_color="white")
            lbl.pack(side="left", padx=5, pady=15)
