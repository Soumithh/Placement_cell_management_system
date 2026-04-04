import customtkinter as ctk
from logic.student_controller import StudentController
from tkinter import messagebox

class StudentDashboard(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="#181a2e")
        self.app_controller = app_controller
        self.user_info = app_controller.current_user

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color="#1d1e2b")
        self.header.grid(row=0, column=0, sticky="ew")
        
        self.welcome_label = ctk.CTkLabel(self.header, text=f"Student Dashboard - {self.user_info['name']}", text_color="white", font=ctk.CTkFont(family="Inter", size=22, weight="bold"))
        self.welcome_label.pack(side="left", padx=20, pady=20)
        
        self.logout_btn = ctk.CTkButton(self.header, text="Logout", width=100, height=35, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white", command=self.app_controller.logout)
        self.logout_btn.pack(side="right", padx=20, pady=15)

        self.tabview = ctk.CTkTabview(self, fg_color="#181a2e", segmented_button_fg_color="#222433", segmented_button_selected_color="#8c52ff", segmented_button_selected_hover_color="#5e1b9f", text_color="white")
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.tabview.add("Job Listings")
        self.tabview.add("My Applications")
        
        self.setup_job_listings()
        self.setup_my_applications()

    def setup_job_listings(self):
        tab = self.tabview.tab("Job Listings")
        self.jobs_frame = ctk.CTkScrollableFrame(tab, corner_radius=15, fg_color="#2b304c", border_width=1, border_color="#3e4368")
        self.jobs_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=20)
        ctk.CTkButton(header_frame, text="↺ Reload Jobs", width=120, height=35, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white", command=self.load_jobs).pack(side="right", pady=10)
        self.load_jobs()

    def load_jobs(self):
        for w in self.jobs_frame.winfo_children():
            w.destroy()
            
        jobs = StudentController.get_all_jobs()
        for idx, j in enumerate(jobs):
            card = ctk.CTkFrame(self.jobs_frame, fg_color="#3A3C56", corner_radius=8)
            card.pack(fill="x", pady=6, padx=10)
            
            text = f"{j['title']} at {j['company_name']}   |   Salary: {j['salary']}   |   Vacancies: {j['vacancy']}"
            
            lbl = ctk.CTkLabel(card, text=text, text_color="white", font=ctk.CTkFont(size=14, weight="bold"))
            lbl.pack(side="left", padx=15, pady=15)
            
            apply_btn = ctk.CTkButton(card, text="Apply Now", width=100, height=35, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white",
                                      command=lambda jid=j['id']: self.apply_job(jid))
            apply_btn.pack(side="right", padx=15, pady=10)

    def apply_job(self, job_id):
        res = StudentController.apply_to_job(self.user_info['id'], job_id)
        if res['success']:
            messagebox.showinfo("Success", res['message'])
            self.load_applications()
        else:
            messagebox.showerror("Error", res['message'])

    def setup_my_applications(self):
        tab = self.tabview.tab("My Applications")
        self.apps_frame = ctk.CTkScrollableFrame(tab, corner_radius=15, fg_color="#2b304c", border_width=1, border_color="#3e4368")
        self.apps_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=20)
        ctk.CTkButton(header_frame, text="↺ Refresh Applications", width=150, height=35, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white", command=self.load_applications).pack(side="right", pady=10)
        self.load_applications()

    def load_applications(self):
        for w in self.apps_frame.winfo_children():
            w.destroy()
            
        apps = StudentController.get_my_applications(self.user_info['id'])
        for idx, a in enumerate(apps):
            card = ctk.CTkFrame(self.apps_frame, fg_color="#3A3C56", corner_radius=8)
            card.pack(fill="x", pady=6, padx=10)
            
            status_color = "#32CD32" if a['status'] == 'Selected' else ("#FF4C4C" if a['status'] == 'Rejected' else "#FFA500")
            
            status_indicator = ctk.CTkLabel(card, text=f" {a['status'].upper()} ", text_color=status_color, font=ctk.CTkFont(size=12, weight="bold"))
            status_indicator.pack(side="left", padx=(15, 10), pady=15)
            
            text = f"{a['title']} at {a['company_name']}"
            lbl = ctk.CTkLabel(card, text=text, text_color="white", font=ctk.CTkFont(size=14))
            lbl.pack(side="left", padx=10, pady=15)
