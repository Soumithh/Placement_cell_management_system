import customtkinter as ctk
from logic.admin_controller import AdminController
from tkinter import messagebox

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master)
        self.app_controller = app_controller
        self.user_info = app_controller.current_user

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")
        
        self.welcome_label = ctk.CTkLabel(self.header, text=f"Admin Dashboard ({self.user_info['name']})", font=("Arial", 20, "bold"))
        self.welcome_label.pack(side="left", padx=20, pady=15)
        
        self.logout_btn = ctk.CTkButton(self.header, text="Logout", width=100, command=self.app_controller.logout)
        self.logout_btn.pack(side="right", padx=20, pady=15)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.tabview.add("Create Student")
        self.tabview.add("Create Company")
        self.tabview.add("Update Placements")
        self.tabview.add("View Users")

        self.setup_create_student_tab()
        self.setup_create_company_tab()
        self.setup_placements_tab()
        self.setup_view_users_tab()

    def setup_create_student_tab(self):
        tab = self.tabview.tab("Create Student")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(2, weight=1)

        form = ctk.CTkFrame(tab)
        form.grid(row=0, column=1, pady=30, padx=30)
        
        ctk.CTkLabel(form, text="Username").pack(pady=5)
        self.st_user = ctk.CTkEntry(form, width=250)
        self.st_user.pack(pady=5)
        
        ctk.CTkLabel(form, text="Password").pack(pady=5)
        self.st_pass = ctk.CTkEntry(form, width=250, show="*")
        self.st_pass.pack(pady=5)

        ctk.CTkLabel(form, text="Full Name").pack(pady=5)
        self.st_name = ctk.CTkEntry(form, width=250)
        self.st_name.pack(pady=5)

        ctk.CTkLabel(form, text="Phone").pack(pady=5)
        self.st_phone = ctk.CTkEntry(form, width=250)
        self.st_phone.pack(pady=5)

        ctk.CTkLabel(form, text="Department").pack(pady=5)
        self.st_dept = ctk.CTkEntry(form, width=250)
        self.st_dept.pack(pady=5)

        ctk.CTkLabel(form, text="CGPA").pack(pady=5)
        self.st_cgpa = ctk.CTkEntry(form, width=250)
        self.st_cgpa.pack(pady=5)

        ctk.CTkButton(form, text="Create Student", command=self.create_student).pack(pady=20)

    def create_student(self):
        if not all([self.st_user.get(), self.st_pass.get(), self.st_name.get()]):
            messagebox.showerror("Error", "Username, Password, and Name are strictly required.")
            return

        res = AdminController.create_student(
            self.st_user.get(), self.st_pass.get(), self.st_name.get(),
            self.st_phone.get(), self.st_dept.get(), self.st_cgpa.get()
        )
        if res['success']:
            messagebox.showinfo("Success", res['message'])
        else:
            messagebox.showerror("Error", res['message'])

    def setup_create_company_tab(self):
        tab = self.tabview.tab("Create Company")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(2, weight=1)

        form = ctk.CTkFrame(tab)
        form.grid(row=0, column=1, pady=30, padx=30)

        ctk.CTkLabel(form, text="Company Login User").pack(pady=5)
        self.cp_user = ctk.CTkEntry(form, width=250)
        self.cp_user.pack(pady=5)

        ctk.CTkLabel(form, text="Password").pack(pady=5)
        self.cp_pass = ctk.CTkEntry(form, width=250, show="*")
        self.cp_pass.pack(pady=5)

        ctk.CTkLabel(form, text="Company Name").pack(pady=5)
        self.cp_name = ctk.CTkEntry(form, width=250)
        self.cp_name.pack(pady=5)

        ctk.CTkLabel(form, text="Location").pack(pady=5)
        self.cp_loc = ctk.CTkEntry(form, width=250)
        self.cp_loc.pack(pady=5)

        ctk.CTkLabel(form, text="Contact Info").pack(pady=5)
        self.cp_contact = ctk.CTkEntry(form, width=250)
        self.cp_contact.pack(pady=5)

        ctk.CTkButton(form, text="Create Company", command=self.create_company).pack(pady=20)

    def create_company(self):
        if not all([self.cp_user.get(), self.cp_pass.get(), self.cp_name.get()]):
            messagebox.showerror("Error", "Required fields missing.")
            return

        res = AdminController.create_company(
            self.cp_user.get(), self.cp_pass.get(), self.cp_name.get(),
            self.cp_contact.get(), self.cp_loc.get(), self.cp_contact.get()
        )
        if res['success']:
            messagebox.showinfo("Success", res['message'])
        else:
            messagebox.showerror("Error", res['message'])

    def setup_placements_tab(self):
        tab = self.tabview.tab("Update Placements")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(2, weight=1)

        form = ctk.CTkFrame(tab)
        form.grid(row=0, column=1, pady=30, padx=30)

        self.students = AdminController.get_all_students()
        self.jobs = AdminController.get_all_jobs()

        s_vals = [f"{s['id']} - {s['name']}" for s in self.students] if self.students else ["No Students"]
        j_vals = [f"{j['id']} - {j['title']} ({j['company_name']})" for j in self.jobs] if self.jobs else ["No Jobs"]

        ctk.CTkLabel(form, text="Select Student").pack(pady=5)
        self.pl_st = ctk.CTkComboBox(form, values=s_vals, width=250)
        self.pl_st.pack(pady=5)

        ctk.CTkLabel(form, text="Select Job").pack(pady=5)
        self.pl_job = ctk.CTkComboBox(form, values=j_vals, width=250)
        self.pl_job.pack(pady=5)

        ctk.CTkLabel(form, text="Status").pack(pady=5)
        self.pl_status = ctk.CTkComboBox(form, values=["Applied", "Selected", "Rejected"], width=250)
        self.pl_status.pack(pady=5)

        ctk.CTkButton(form, text="Update Status", command=self.update_placement).pack(pady=20)

        # Refresh button to fetch latest DB values
        ctk.CTkButton(form, text="Refresh Lists", fg_color="gray", command=self.refresh_placements_tab).pack(pady=5)

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
        self.users_frame = ctk.CTkScrollableFrame(tab)
        self.users_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkButton(tab, text="Refresh Users", command=self.load_users).pack(pady=10)
        self.load_users()

    def load_users(self):
        for widget in self.users_frame.winfo_children():
            widget.destroy()
        
        users = AdminController.get_all_users()
        for idx, u in enumerate(users):
            text = f"[{u['role_name']}] Username: {u['username']} | Name: {u['name']}"
            lbl = ctk.CTkLabel(self.users_frame, text=text, anchor="w", justify="left")
            lbl.grid(row=idx, column=0, sticky="w", pady=2, padx=5)
