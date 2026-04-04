import customtkinter as ctk
from logic.admin_controller import AdminController
from tkinter import messagebox

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="#181a2e")
        self.app_controller = app_controller
        self.user_info = app_controller.current_user

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color="#1d1e2b")
        self.header.grid(row=0, column=0, sticky="ew")
        
        self.welcome_label = ctk.CTkLabel(self.header, text=f"Admin Dashboard", text_color="white", font=ctk.CTkFont(family="Inter", size=22, weight="bold"))
        self.welcome_label.pack(side="left", padx=20, pady=20)
        
        self.logout_btn = ctk.CTkButton(self.header, text="Logout", width=100, height=35, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white", command=self.app_controller.logout)
        self.logout_btn.pack(side="right", padx=20, pady=15)

        self.tabview = ctk.CTkTabview(self, fg_color="#181a2e", segmented_button_fg_color="#222433", segmented_button_selected_color="#8c52ff", segmented_button_selected_hover_color="#5e1b9f", text_color="white")
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.tabview.add("Update Placements")
        self.tabview.add("View Users")

        self.setup_placements_tab()
        self.setup_view_users_tab()

    def setup_placements_tab(self):
        tab = self.tabview.tab("Update Placements")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(2, weight=1)

        form = ctk.CTkFrame(tab, fg_color="#2b304c", corner_radius=15, border_width=1, border_color="#3e4368")
        form.grid(row=0, column=1, pady=30, padx=40)

        self.students = AdminController.get_all_students()
        self.jobs = AdminController.get_all_jobs()

        s_vals = [f"{s['id']} - {s['name']}" for s in self.students] if self.students else ["No Students"]
        j_vals = [f"{j['id']} - {j['title']} ({j['company_name']})" for j in self.jobs] if self.jobs else ["No Jobs"]

        ctk.CTkLabel(form, text="Assign Placement", text_color="white", font=ctk.CTkFont(family="Inter", size=20, weight="bold")).pack(pady=(25, 15))

        ctk.CTkLabel(form, text="Select Student", text_color="white", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 0), anchor="w", padx=40)
        self.pl_st = ctk.CTkComboBox(form, values=s_vals, width=280, height=35, corner_radius=8, fg_color="#222433", border_color="#484b6a", button_color="#8338ec", button_hover_color="#6123b3", text_color="white", dropdown_fg_color="#222433", dropdown_text_color="white")
        self.pl_st.pack(pady=5, padx=40)

        ctk.CTkLabel(form, text="Select Job", text_color="white", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 0), anchor="w", padx=40)
        self.pl_job = ctk.CTkComboBox(form, values=j_vals, width=280, height=35, corner_radius=8, fg_color="#222433", border_color="#484b6a", button_color="#8338ec", button_hover_color="#6123b3", text_color="white", dropdown_fg_color="#222433", dropdown_text_color="white")
        self.pl_job.pack(pady=5, padx=40)

        ctk.CTkLabel(form, text="Status Requirement", text_color="white", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 0), anchor="w", padx=40)
        self.pl_status = ctk.CTkComboBox(form, values=["Applied", "Selected", "Rejected"], width=280, height=35, corner_radius=8, fg_color="#222433", border_color="#484b6a", button_color="#8338ec", button_hover_color="#6123b3", text_color="white", dropdown_fg_color="#222433", dropdown_text_color="white")
        self.pl_status.pack(pady=5, padx=40)

        ctk.CTkButton(form, text="Update Status", width=280, height=40, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), command=self.update_placement).pack(pady=(25, 10))

        # Refresh
        ctk.CTkButton(form, text="Refresh Lists", fg_color="transparent", hover_color="#3a3c56", text_color="#A0A0BA", command=self.refresh_placements_tab).pack(pady=(0, 20))

    def refresh_placements_tab(self):
        self.students = AdminController.get_all_students()
        self.jobs = AdminController.get_all_jobs()

        s_vals = [f"{s['id']} - {s['name']}" for s in self.students] if self.students else ["No Students"]
        j_vals = [f"{j['id']} - {j['title']} ({j['company_name']})" for j in self.jobs] if self.jobs else ["No Jobs"]

        self.pl_st.configure(values=s_vals)
        self.pl_job.configure(values=j_vals)
        if s_vals: self.pl_st.set(s_vals[0])
        if j_vals: self.pl_job.set(j_vals[0])

    def update_placement(self):
        st_val = self.pl_st.get()
        job_val = self.pl_job.get()
        if "No" in st_val or "No" in job_val:
            messagebox.showerror("Error", "Invalid student or job selection")
            return
            
        st_id = int(st_val.split(" - ")[0])
        job_id = int(job_val.split(" - ")[0])

        res = AdminController.assign_placement(st_id, job_id, self.pl_status.get())
        if res['success']:
            messagebox.showinfo("Success", res['message'])
        else:
            messagebox.showerror("Error", res['message'])

    def setup_view_users_tab(self):
        tab = self.tabview.tab("View Users")
        
        self.users_frame = ctk.CTkScrollableFrame(tab, corner_radius=15, fg_color="#2b304c", border_width=1, border_color="#3e4368")
        self.users_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=20)
        ctk.CTkButton(header_frame, text="↺ Refresh List", width=120, height=35, corner_radius=8, fg_color="#8338ec", hover_color="#6123b3", text_color="white", command=self.load_users).pack(side="right", pady=10)
        
        self.load_users()

    def load_users(self):
        for widget in self.users_frame.winfo_children():
            widget.destroy()
        
        users = AdminController.get_all_users()
        for idx, u in enumerate(users):
            card = ctk.CTkFrame(self.users_frame, fg_color="#3A3C56", corner_radius=8)
            card.pack(fill="x", pady=5, padx=10)
            
            text = f"[{u['role_name'].upper()}]   Username: {u['username']}   |   Full Name: {u['name']}"
            lbl = ctk.CTkLabel(card, text=text, font=ctk.CTkFont(size=13), text_color="white")
            lbl.pack(side="left", padx=15, pady=12)
