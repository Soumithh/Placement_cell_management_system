import customtkinter as ctk
from logic.student_controller import StudentController
from tkinter import messagebox

class StudentDashboard(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master)
        self.app_controller = app_controller
        self.user_info = app_controller.current_user

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")
        
        self.welcome_label = ctk.CTkLabel(self.header, text=f"Student Dashboard - {self.user_info['name']}", font=("Arial", 20, "bold"))
        self.welcome_label.pack(side="left", padx=20, pady=15)
        
        self.logout_btn = ctk.CTkButton(self.header, text="Logout", width=100, command=self.app_controller.logout)
        self.logout_btn.pack(side="right", padx=20, pady=15)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.tabview.add("Job Listings")
        self.tabview.add("My Applications")
        
        self.setup_job_listings()
        self.setup_my_applications()

    def setup_job_listings(self):
        tab = self.tabview.tab("Job Listings")
        self.jobs_frame = ctk.CTkScrollableFrame(tab)
        self.jobs_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        btn = ctk.CTkButton(tab, text="Refresh Jobs", command=self.load_jobs)
        btn.pack(pady=10)
        self.load_jobs()

    def load_jobs(self):
        for w in self.jobs_frame.winfo_children():
            w.destroy()
            
        jobs = StudentController.get_all_jobs()
        for idx, j in enumerate(jobs):
            text = f"{j['title']} at {j['company_name']} | Salary: {j['salary']} | Vacancy: {j['vacancy']}"
            job_entry_frame = ctk.CTkFrame(self.jobs_frame)
            job_entry_frame.pack(fill="x", pady=5)
            
            lbl = ctk.CTkLabel(job_entry_frame, text=text, anchor="w")
            lbl.pack(side="left", padx=10, pady=5)
            
            apply_btn = ctk.CTkButton(job_entry_frame, text="Apply", width=80, 
                                      command=lambda jid=j['id']: self.apply_job(jid))
            apply_btn.pack(side="right", padx=10, pady=5)

    def apply_job(self, job_id):
        res = StudentController.apply_to_job(self.user_info['id'], job_id)
        if res['success']:
            messagebox.showinfo("Success", res['message'])
            self.load_applications()
        else:
            messagebox.showerror("Error", res['message'])

    def setup_my_applications(self):
        tab = self.tabview.tab("My Applications")
        self.apps_frame = ctk.CTkScrollableFrame(tab)
        self.apps_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        btn = ctk.CTkButton(tab, text="Refresh Applications", command=self.load_applications)
        btn.pack(pady=10)
        self.load_applications()

    def load_applications(self):
        for w in self.apps_frame.winfo_children():
            w.destroy()
            
        apps = StudentController.get_my_applications(self.user_info['id'])
        for idx, a in enumerate(apps):
            text = f"Status: {a['status']} | {a['title']} at {a['company_name']}"
            lbl = ctk.CTkLabel(self.apps_frame, text=text, anchor="w", justify="left")
            lbl.pack(fill="x", pady=5, padx=10)
