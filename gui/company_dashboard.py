import customtkinter as ctk
from logic.company_controller import CompanyController
from tkinter import messagebox

class CompanyDashboard(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master)
        self.app_controller = app_controller
        self.user_info = app_controller.current_user

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")
        
        self.welcome_label = ctk.CTkLabel(self.header, text=f"Company Dashboard - {self.user_info['name']}", font=("Arial", 20, "bold"))
        self.welcome_label.pack(side="left", padx=20, pady=15)
        
        self.logout_btn = ctk.CTkButton(self.header, text="Logout", width=100, command=self.app_controller.logout)
        self.logout_btn.pack(side="right", padx=20, pady=15)

        self.tabview = ctk.CTkTabview(self)
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

        form = ctk.CTkFrame(tab)
        form.grid(row=0, column=1, pady=30, padx=30)
        
        ctk.CTkLabel(form, text="Job Title").pack(pady=5)
        self.j_title = ctk.CTkEntry(form, width=250)
        self.j_title.pack(pady=5)

        ctk.CTkLabel(form, text="Salary Package").pack(pady=5)
        self.j_salary = ctk.CTkEntry(form, width=250)
        self.j_salary.pack(pady=5)

        ctk.CTkLabel(form, text="Vacancies").pack(pady=5)
        self.j_vac = ctk.CTkEntry(form, width=250)
        self.j_vac.pack(pady=5)

        ctk.CTkButton(form, text="Post Job", command=self.post_job).pack(pady=20)

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
        self.jobs_frame = ctk.CTkScrollableFrame(tab)
        self.jobs_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        btn = ctk.CTkButton(tab, text="Refresh Jobs", command=self.load_my_jobs)
        btn.pack(pady=10)
        self.load_my_jobs()

    def load_my_jobs(self):
        for w in self.jobs_frame.winfo_children():
            w.destroy()
        
        jobs = CompanyController.get_my_jobs(self.user_info['id'])
        for idx, j in enumerate(jobs):
            text = f"{j['title']} | Salary: {j['salary']} | Vacancy: {j['vacancy']}"
            lbl = ctk.CTkLabel(self.jobs_frame, text=text, anchor="w", justify="left")
            lbl.grid(row=idx, column=0, sticky="w", pady=2, padx=5)

    def setup_view_applicants(self):
        tab = self.tabview.tab("View Applicants")
        self.apps_frame = ctk.CTkScrollableFrame(tab)
        self.apps_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        btn = ctk.CTkButton(tab, text="Refresh Applicants", command=self.load_applicants)
        btn.pack(pady=10)
        self.load_applicants()

    def load_applicants(self):
        for w in self.apps_frame.winfo_children():
            w.destroy()
        
        apps = CompanyController.get_applicants(self.user_info['id'])
        for idx, a in enumerate(apps):
            text = f"[{a['status']}] {a['student_name']} (CGPA: {a['cgpa']}) applied to {a['title']}"
            lbl = ctk.CTkLabel(self.apps_frame, text=text, anchor="w", justify="left")
            lbl.grid(row=idx, column=0, sticky="w", pady=2, padx=5)
