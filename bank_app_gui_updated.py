import datetime
import customtkinter as ctk
from tkinter import messagebox, filedialog
import pymysql as myconn
import pandas as pd
from random import randint
import smtplib

# Database Connection
def get_db_connection():
    return myconn.connect(
        host="localhost",
        user="root",
        password="root",
        database="new_bank")

db=get_db_connection()
cur=db.cursor()

# CustomTkinter setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BankingAppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x600")
        self.title("Banking Application")
                                                
        self.curr_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cyear = datetime.datetime.today().strftime("%Y")
        self.cmonth = datetime.datetime.today().strftime("%m")
        self.cday = datetime.datetime.today().strftime("%d")

        self.unames_query='select username from customer_info'
        self.unames_list=[]
        self.ids_query='select c_id from customer_info'
        self.ids_list=[]
        self.current_user=""
        self.df3=pd.DataFrame()

        self.valid_fname=""
        self.valid_mname=""
        self.valid_lname=""
        self.valid_phoneno=""
        self.valid_aadhaar=""
        self.valid_username=""
        self.valid_password=""
        self.email=""
        self.verified_email=self.email
        self.tablename=""
        self.c_id=0

        self.gender=""
        self.valid_year=""
        self.valid_month=""
        self.valid_day=""
        self.occ=""
        self.edu=""
        self.mstatus=""
        self.income=""
        self.dob=""
        self.age=0
        self.income_range=['Select option','<50K','50K-100K','100K-150K','None']
        self.edu_level=['Select option','10th','12th','Graduation','Masters','PHD']
        self.occupations=['Select option','Housewife','Business','Job','Student','Retired','Other']

        self.show_main_menu()
        self.all_customers()

    # MAIN MENU PAGE
    def show_main_menu(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Welcome to HDFC Bank", font=("Arial", 24))
        label.pack(pady=15)
        label_ = ctk.CTkLabel(self, text=f"{self.curr_date}", font=("Arial", 15))
        label_.pack(pady=5)

        signup_btn = ctk.CTkButton(self, text="Sign Up", command=self.show_signup_form)
        signup_btn.pack(pady=10)

        signin_btn = ctk.CTkButton(self, text="Sign In", command=self.show_signin_form)
        signin_btn.pack(pady=10)

        admin_login_btn = ctk.CTkButton(self, text="Admin Login", command=self.show_admin_login)
        admin_login_btn.pack(pady=10)

    # CLEAR CONTENTS IN PAGE
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    # SIGNUP FORM PAGE
    def show_signup_form(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Sign Up", font=("Arial", 20))
        label.pack(pady=10)

        fnamelabel = ctk.CTkLabel(self, text="First Name", font=("Arial", 15))
        fnamelabel.place(x=50,y=53)
        self.fname_entry = ctk.CTkEntry(self, placeholder_text="e.g. User")
        self.fname_entry.pack(pady=5)

        mnamelabel = ctk.CTkLabel(self, text="Middle Name", font=("Arial", 15))
        mnamelabel.place(x=50,y=92)
        self.mname_entry = ctk.CTkEntry(self, placeholder_text="e.g. Abc")
        self.mname_entry.pack(pady=5)

        lnamelabel = ctk.CTkLabel(self, text="Last Name", font=("Arial", 15))
        lnamelabel.place(x=50,y=131)
        self.lname_entry = ctk.CTkEntry(self, placeholder_text="e.g. Xyz")
        self.lname_entry.pack(pady=5)

        phonenolabel = ctk.CTkLabel(self, text="Phone No.", font=("Arial", 15))
        phonenolabel.place(x=50,y=170)
        self.phoneno_entry = ctk.CTkEntry(self, placeholder_text="Phone No.")
        self.phoneno_entry.pack(pady=5)

         # Gender selection using radio buttons
        gender_label = ctk.CTkLabel(self, text="Gender", font=("Arial", 15))
        gender_label.place(x=50,y=205)

        self.gender_var = ctk.StringVar(value="M")  # Default value is Male

        gender_frame = ctk.CTkFrame(self)
        gender_frame.pack(pady=5)

        male_radio = ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="M")
        male_radio.pack(side="left", padx=5)

        female_radio = ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="F")
        female_radio.pack(side="left", padx=5)

        aadhaarnolabel = ctk.CTkLabel(self, text="Aadhaar No.", font=("Arial", 15))
        aadhaarnolabel.place(x=50,y=241)
        self.aadhaarno_entry = ctk.CTkEntry(self, placeholder_text="Aadhaar No.")
        self.aadhaarno_entry.pack(pady=5)

        usernamelabel = ctk.CTkLabel(self, text="Username", font=("Arial", 15))
        usernamelabel.place(x=50,y=279)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="e.g. userabc")
        self.username_entry.pack(pady=5)

        passwordlabel = ctk.CTkLabel(self, text="Set Password", font=("Arial", 15))
        passwordlabel.place(x=50,y=317)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="e.g. 1234")
        self.password_entry.pack(pady=5)

        confirm_passwordlabel = ctk.CTkLabel(self, text="Confirm Password", font=("Arial", 15))
        confirm_passwordlabel.place(x=50,y=355)
        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text=" ")
        self.confirm_password_entry.pack(pady=5)

        signup_btn = ctk.CTkButton(self, text="Submit Info", command=self.submit_info )
        signup_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_main_menu)
        back_btn.pack(pady=5)

    # SUBMITS VALID INFO IN DATABASE - ACTION
    def submit_info(self):
        self.fname = self.fname_entry.get()
        self.mname = self.mname_entry.get()
        self.lname = self.lname_entry.get()
        self.gender = self.gender_var.get()
        self.phoneno = self.phoneno_entry.get()
        self.aadhaarno = self.aadhaarno_entry.get()
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # checks if all fields are filled or not
        if not all([self.fname, self.mname, self.lname, self.phoneno, self.aadhaarno, self.username, self.password, confirm_password]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            db=get_db_connection()
            cur=db.cursor()

            # fetches all usernames 
            unames_query='select username from customer_info'
            cur.execute(unames_query)
            unames_list=[]
            unames=cur.fetchall()
            for i in unames:
                unames_list.append(i[0])

            # first_name validation
            if not self.fname.isalpha():
                messagebox.showerror("Error", "First Name: No Digits or Special Charaters Allowed!")
                return
            else:
                self.valid_fname=self.fname.title()

            # middle_name validation
            if not self.mname.isalpha():
                messagebox.showerror("Error", "Middle Name: No Digits or Special Charaters Allowed!")
                return
            else:
                self.valid_mname=self.mname.title()

            # last_name validation
            if not self.lname.isalpha():
                messagebox.showerror("Error", "Last Name: No Digits or Special Charaters Allowed!")
                return
            else:
                self.valid_lname=self.lname.title()    

            # username validation
            if str(self.username) not in unames_list:
                if not ((len(self.username)>=4 and len(self.username)<=10 )and self.username.isalpha()):
                    messagebox.showerror("Error", "Username must be of 4-10 alphabets !")
                    return
                else:
                    self.valid_username = self.username.lower()
                    self.tablename=self.valid_username
            else:
                messagebox.showerror("Error","An error occurred: Username exists already ! \nTry a new one !! ")

            # phone no. validation
            if not (len(self.phoneno)==10 and self.phoneno.isdigit()):
                messagebox.showerror("Error", "Phone No. must be of 10 digits!")
                return
            else:
                self.valid_phoneno=self.phoneno

            # aadhaar no. validation
            if not (len(self.aadhaarno)==12 and self.aadhaarno.isdigit()):
                messagebox.showerror("Error", "Aadhaar No. must be of 12 digits!")
                return
            else:
                self.valid_aadhaar=self.aadhaarno

            # password validation
            if self.password != confirm_password:
                messagebox.showerror("Error", "Check Password Again!")
                return
 
            self.valid_password = self.password
            
            # if all fields are valid then only show the create account option
            if self.valid_fname and self.valid_mname and self.valid_lname and self.valid_phoneno and self.valid_aadhaar and self.valid_username and self.valid_password:
                next_btn = ctk.CTkButton(self, text="Next", command=self.more_info )
                next_btn.pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # MORE INFO PAGE
    def more_info(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Sign Up", font=("Arial", 20))
        label.pack(pady=10)

        # MARITAL STATUS - SINGLE, MARRIED - RADIO BUTTON
        maritalstatus_label = ctk.CTkLabel(self, text="Marital Status", font=("Arial", 15))
        maritalstatus_label.place(x=50,y=50)

        self.mstatus_var = ctk.StringVar(value="Single")  # Default value is Single

        mstatus_frame = ctk.CTkFrame(self)
        mstatus_frame.pack(pady=5)

        single_radio = ctk.CTkRadioButton(mstatus_frame, text="Single", variable=self.mstatus_var, value="Single")
        single_radio.pack(side="left")

        married_radio = ctk.CTkRadioButton(mstatus_frame, text="Married", variable=self.mstatus_var, value="Married")
        married_radio.pack(side="left")
    
        # DOB -> AGE
        doblabel = ctk.CTkLabel(self, text="Date Of Birth", font=("Arial", 15))
        doblabel.place(x=50,y=90)

        self.year_entry = ctk.CTkEntry(self, placeholder_text="YYYY",width=50)
        self.year_entry.place(x=200,y=90)
        self.month_entry = ctk.CTkEntry(self, placeholder_text="MM",width=35)
        self.month_entry.place(x=260,y=90)
        self.day_entry = ctk.CTkEntry(self, placeholder_text="DD",width=30)
        self.day_entry.place(x=305,y=90)

        # EDUCATION LEVEL - 10th, 12th, Graduation, PHD, Masters
        education_label = ctk.CTkLabel(self, text="Education Level", font=("Arial", 15))
        education_label.place(x=50,y=130)
        self.edu_var = ctk.StringVar(value='Select option')  # set initial value
        edu_dd = ctk.CTkComboBox(self, values=self.edu_level, variable=self.edu_var) 
        edu_dd.place(x=200,y=130)

        # OCCUPATION - HOUSEWIFE, BUSINESS, JOB, STUDENT, RETIRED
        occ_label = ctk.CTkLabel(self, text="Occupation", font=("Arial", 15))
        occ_label.place(x=50,y=170)
        self.occupation_var = ctk.StringVar(value='Select option')  # set initial value
        occupation_dd = ctk.CTkComboBox(self, values=self.occupations, variable=self.occupation_var) #,command=combobox_callback
        occupation_dd.place(x=200,y=170)

        # MONTHLY INCOME RANGE - <50K, 50K-100K, 100K-150K, 150K-200K - DROPDOWN
        mon_income_label = ctk.CTkLabel(self, text="Monthly Income", font=("Arial", 15))
        mon_income_label.place(x=50,y=210)
        self.mon_income_var = ctk.StringVar(value='Select option')  # set initial value
        mon_income_dd = ctk.CTkComboBox(self, values=self.income_range, variable=self.mon_income_var) 
        mon_income_dd.place(x=200,y=210) 

        confirm_btn = ctk.CTkButton(self, text="Confirm", command=self.submit_more_info)
        confirm_btn.place(x=180,y=350)

        back_btn = ctk.CTkButton(self, text="Cancel", command=self.show_signup_form)
        back_btn.place(x=180,y=400)

    # SUBMIT MORE INFO ACTION
    def submit_more_info(self):
        year=self.year_entry.get()
        month=self.month_entry.get()
        day=self.day_entry.get()
        self.occ=self.occupation_var.get()
        self.income=self.mon_income_var.get()
        self.mstatus=self.mstatus_var.get()
        self.edu=self.edu_var.get()

        # checks if all fields are filled or not
        if not all([year, month, day, self.occ, self.income, self.mstatus, self.edu]):
            if self.occ=="Select Option" or self.income=="Select Option" or self.edu=="Select Option":
                messagebox.showerror("Error", "All fields are required!")
                return
        
        # dob validation
        non_leapdates_in_months={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        leapdates_in_months={1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

        try:
            # year validation
            if len(year)==4:
                if str(year).isdigit():
                    year=int(year)
                    self.cyear=int(self.cyear)
                    if (self.cyear-year)>=18:
                        self.valid_year=year
                    else:
                        messagebox.showerror("Error","Invalid Year : User must be 18 years old")
                else:
                    messagebox.showerror("Error","Invalid Year: No alphabets allowed in Year")
            else:
                messagebox.showerror("Error","Invalid Year: Year must be of 4 digits")

            # month validation
            if len(month)==2:
                if str(month).isdigit():
                    month=int(month)
                    if month<=12:
                        self.valid_month=month
                    else:
                        messagebox.showerror("Error","Invalid Month: There are only 12 months")
                else:
                    messagebox.showerror("Error","Invalid Month: No alphabets allowed in Month")
            else:
                messagebox.showerror("Error","Invalid Month: Month must be of 2 digits")

            # day validation
            if len(day)==2:
                if str(day).isdigit():
                    day=int(day)
                    if (year%4==0 and year%100!=0)or(year%400==0):
                        # "leap"
                        if day<=(leapdates_in_months[month]):
                            self.valid_day=day
                        else:
                            messagebox.showerror("Error","Invalid Date: Leap Year contains 29 in month of February")
                    else:
                        # "nonleap" 
                        if day<=(non_leapdates_in_months[month]):
                            self.valid_day=day
                        else:
                            messagebox.showerror("Error","Invalid Date: Non Leap Year contains 28 in month of February")
                else:
                    messagebox.showerror("Error","Invalid Date: No alphabets allowed")
            else:
                messagebox.showerror("Error","Invalid Date: Date must be of 2 digits")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        if self.valid_year and self.valid_month and self.valid_day:
            self.dob=f'{self.valid_year}-{self.valid_month}-{self.valid_day}'
            self.age=self.cyear-self.valid_year

        # if all fields are valid then only show the create account option
        if self.dob and self.occ and self.edu and self.income and self.mstatus:
            next_btn = ctk.CTkButton(self, text="Next", command=self.show_otp_verification_form )
            next_btn.place(x=180,y=450)

    # EMAIL AND OTP VERIFICATION PAGE
    def show_otp_verification_form(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="VERIFICATION", font=("Arial", 20))
        label.pack(padx=75,pady=25)

        email_label = ctk.CTkLabel(self, text="Email", font=("Arial", 20))
        email_label.place(x=75,y=85)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="e.g. your_email@example.com",width=200)
        self.email_entry.pack(pady=5)

        send_otp_btn=ctk.CTkButton(self, text="Send OTP", command=self.handle_send_otp)
        send_otp_btn.pack(pady=10)

        self.otp_entry = ctk.CTkEntry(self, placeholder_text="Enter OTP")
        self.otp_entry.pack(pady=10)

        verify_btn = ctk.CTkButton(self, text="Verify OTP", command=self.verify_otp)
        verify_btn.pack(pady=5)

        back_btn = ctk.CTkButton(self, text="Cancel", command=self.show_signup_form)
        back_btn.pack(pady=25)

    # SENDS OTP THROUGH EMAIL ACTION
    def handle_send_otp(self):
        #Handle sending OTP and proceed to verification.
        email = self.email_entry.get()
        if not email:
            messagebox.showerror("Error", "Email is required!")
            return

        if self.send_otp(email):
            messagebox.showinfo("Success", "OTP sent to your email!")
            self.email=email
        else:
            messagebox.showerror("Error", "Failed to send OTP. Check your email address.")

    #  GENERATES OTP (ACTION)
    def send_otp(self,email):
        #"""Send OTP to the user's email."""
        self.generated_otp = randint(1000, 9999)  # Generate 4-digit OTP
        subject = "Your OTP for Account Verification"
        body = f"Your OTP for verifying your email address is: {self.generated_otp}"

        try:
            # Setup SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("pkkarkera2@gmail.com", "qqdq lvsd ovcy exzs")  # Replace with sender email credentials

            # Compose and send the email
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail("pkkarkera2@gmail.com", email, message)
            server.quit()

            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
        
    # VERIFIES THE OTP
    def verify_otp(self):
        # """Verify the entered OTP."""
        entered_otp = self.otp_entry.get()
        if not entered_otp:
            messagebox.showerror("Error", "OTP is required!")
            return

        if entered_otp == str(self.generated_otp):
            messagebox.showinfo("Success", "OTP verified !!!")
            create_btn = ctk.CTkButton(self, text="Create Account", command=self.create_account )
            create_btn.pack(pady=10)
        else:
            messagebox.showerror("Error", "Invalid OTP!")

    # CREATES ACCOUNT - ADD DETAILS IN CUSTOMER INFO AND CREATES TABLE  (SIGNUP ACTION)
    def create_account(self):
        if self.valid_fname and self.valid_mname and self.valid_lname and self.valid_phoneno and self.email and self.valid_aadhaar and self.valid_username and self.valid_password:
            try:
                db=get_db_connection()
                cur=db.cursor()

                # insert query inserts records in customer info
                query = "insert into customer_info (fname, mname, lname, gender, phoneno, email, aadhaarno, age, dob, occupation, monthly_income, marital_status, education_level, date, username, password, balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(query, (self.valid_fname, self.valid_mname, self.valid_lname, self.gender, self.valid_phoneno, self.email, self.valid_aadhaar, self.age, self.dob, self.occ, self.income, self.mstatus, self.edu, {self.curr_date}, self.valid_username, self.valid_password,0))

                # to fetch customer id 
                id=f'select c_id from customer_info where username="{self.username}"'
                cur.execute(id)
                c_id=cur.fetchall()
                for i in c_id:
                    self.c_id=i[0]

                # message displays after the account is created
                messagebox.showinfo("Success", f'''Account created successfully!
                FULL NAME : {self.valid_fname} {self.valid_mname} {self.valid_lname}
                CUSTOMER ID : {self.c_id}
                EMAIL ID : {self.email}
                DOB : {self.dob}
                PHONE NO. : {self.valid_phoneno}
                AADHAAR NO. : {self.valid_aadhaar}
                USERNAME : {self.valid_username}
                                    ''')
                
                # new table on username is created
                create_table_query=f'create table {self.tablename} (`Sr_No` int primary key auto_increment,`Date` date, `Transaction` varchar(10), `Amount` int)'
                cur.execute(create_table_query)
                db.commit()
                self.show_main_menu()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                db.close()

    # SIGNIN ACTION
    def signin(self):
        username = self.login_username_entry.get()
        self.current_user = username.lower()
        password = self.login_password_entry.get()
        input_password = password

        # checks if all fields are filled or not
        if not all([username, password]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            db=get_db_connection()
            cur=db.cursor()

            # fetches all usernames 
            cur.execute(self.unames_query)
            unames=cur.fetchall()
            for i in unames:
                self.unames_list.append(i[0])
            
            # checks if username exists 
            if str(self.current_user) in self.unames_list:
                get_ps=f'select password from customer_info where username="{self.current_user}"'
                # if username exists then it fetches its password
                cur.execute(get_ps)
                ps=cur.fetchall()
                for i in ps:
                    stored_ps=i[0]

                # fetches first name of user
                fname=f'select fname from customer_info where username="{self.current_user}" '
                cur.execute(fname)
                fname=cur.fetchall()
                for i in fname:
                    fname=i[0]

                if str(input_password)==stored_ps:
                    messagebox.showinfo("Success", f"Welcome back, {fname}!")
                    self.show_after_login_options() 
                else:
                    messagebox.showerror("Error", f"Invalid Password !")
            else:
                messagebox.showerror("Error", "Invalid username !")
        except Exception as e:
            messagebox.showerror("Error",f"An error occurred: {e} !! ")
        finally:
            db.close()

    # SIGNIN FORM
    def show_signin_form(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Sign In", font=("Arial", 20))
        label.pack(pady=10)

        self.login_username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.login_username_entry.pack(pady=5)

        self.login_password_entry = ctk.CTkEntry(self, placeholder_text="Password") 
        self.login_password_entry.pack(pady=5)

        login_btn = ctk.CTkButton(self, text="Log In", command=self.signin)
        login_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_main_menu)
        back_btn.pack(pady=5)

    # AFTER LOGIN OPTION PAGE
    def show_after_login_options(self):
        self.clear_frame()
        
        db=get_db_connection()
        cur=db.cursor()

        # fetches first name of admin
        get_fname=f'select fname from customer_info where username="{self.current_user}"'
        cur.execute(get_fname)
        fname=cur.fetchone()[0]
        
        label = ctk.CTkLabel(self, text=f"Welcome, {fname}", font=("Arial", 20))
        label.pack(pady=20)

        deposit_btn = ctk.CTkButton(self, text="Deposit", command=self.show_deposit_form)
        deposit_btn.pack(pady=10)

        withdraw_btn = ctk.CTkButton(self, text="Withdraw", command=self.show_withdraw_form)
        withdraw_btn.pack(pady=10)

        balance_btn = ctk.CTkButton(self, text="Check Balance", command=self.check_balance)
        balance_btn.pack(pady=10)

        report_btn = ctk.CTkButton(self, text="Transaction Report", command=self.transaction_report)
        report_btn.pack(pady=10)

        change_password_btn = ctk.CTkButton(self, text="Change Password", command=self.show_change_password_form)
        change_password_btn.pack(pady=10)

        exit_btn = ctk.CTkButton(self, text="Log Out", command=self.logout)
        exit_btn.pack(pady=10)

    # DEPOSIT PAGE
    def show_deposit_form(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Deposit Amount", font=("Arial", 20))
        label.pack(pady=20)

        self.deposit_entry = ctk.CTkEntry(self, placeholder_text="Enter Amount")
        self.deposit_entry.pack(pady=10)

        deposit_btn = ctk.CTkButton(self, text="Deposit", command=self.deposit)
        deposit_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_after_login_options)
        back_btn.pack(pady=5)

    # WITHDRAW PAGE
    def show_withdraw_form(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Withdraw Amount", font=("Arial", 20))
        label.pack(pady=20)

        self.withdraw_entry = ctk.CTkEntry(self, placeholder_text="Enter Amount")
        self.withdraw_entry.pack(pady=10)

        withdraw_btn = ctk.CTkButton(self, text="Withdraw", command=self.withdraw)
        withdraw_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_after_login_options)
        back_btn.pack(pady=5)

    # CHECK BALANCE ACTION
    def check_balance(self):
        try:
            db = get_db_connection()
            cur = db.cursor()

            # fetches the balance of the user
            query = f'SELECT balance FROM customer_info WHERE username ="{self.current_user}"'
            cur.execute(query)
            balance = cur.fetchone()[0]

            messagebox.showinfo("Balance", f"Your current balance is: {balance}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # CHANGE PASSWORD PAGE
    def show_change_password_form(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Change Password", font=("Arial", 20))
        label.pack(pady=20)

        self.current_password_entry = ctk.CTkEntry(self, placeholder_text="Current Password")
        self.current_password_entry.pack(pady=10)

        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="New Password")
        self.new_password_entry.pack(pady=10)

        change_btn = ctk.CTkButton(self, text="Change Password", command=self.change_password)
        change_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_after_login_options)
        back_btn.pack(pady=5)

    # CHANGE PASSWORD ACTION
    def change_password(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()

        # checks if all fields are filled
        if not all([current_password, new_password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            db = get_db_connection()
            cur = db.cursor()

            # fetches the current password 
            query = f'SELECT password FROM customer_info WHERE username = "{self.current_user}"'
            cur.execute(query)
            stored_password = cur.fetchone()[0]

            # checks if the entered password is correct
            if stored_password==current_password:
                # new password validation
                if len(new_password)==4 and new_password.isdigit():
                    update_query = f'UPDATE customer_info SET password ="{new_password}"  WHERE username = "{self.current_user}"'
                    cur.execute(update_query)
                    db.commit()
                    messagebox.showinfo("Success", "Password changed successfully!")
            else:
                messagebox.showerror("Error","Wrong Password")
            self.show_after_login_options()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # TRANSACTION REPORT ACTION
    def transaction_report(self):
        try:
            db = get_db_connection()
            cur = db.cursor()
            initial_balance=0

            all=f'select * from {self.current_user}'
            cur.execute(all)
            all_info=cur.fetchall()
            tablecolumns=["sr_no","date","transaction","amount"]
            dataframe=pd.DataFrame(all_info,columns=tablecolumns)
            dataframe["amount"] = dataframe.apply(
            lambda row: -row["amount"] if row["transaction"] == "Withdraw" else row["amount"],axis=1)
            dataframe["Cumulative Balance"] = dataframe["amount"].cumsum() + initial_balance

            # fetches user information
            info_query=f'select fname,mname,lname from customer_info where username="{self.current_user}"'
            cur.execute(info_query)
            info = cur.fetchall()
            for i in info:
                file_name = f"HDFC Bank Transaction Report for {i[0],"_",i[1],"_",i[2]}_{self.current_user}.xlsx"

            file_path = filedialog.asksaveasfilename(initialfile=file_name,defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if file_path:
                dataframe.to_excel(file_path, index=False)
                messagebox.showinfo("Success", "Transaction report saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # DEPOSIT ACTION
    def deposit(self):
        amount = self.deposit_entry.get()
        if not amount.isdigit():
            messagebox.showerror("Error", "Please enter a valid amount!")
            return

        try:
            db = get_db_connection()
            cur = db.cursor()

            # updates the balance amount after deposit
            query = f'UPDATE customer_info SET balance = balance +{amount} WHERE username = "{self.current_user}"'
            cur.execute(query)

            # inserts withdrawal transaction record in user's table
            trans_query = f'INSERT INTO {self.current_user} (Date, Transaction, Amount) VALUES ("{self.curr_date}","Deposit",{amount})'
            cur.execute(trans_query)

            db.commit()
            messagebox.showinfo("Success", f"Deposited {amount} successfully!")
            self.show_after_login_options()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # WITHDRAW ACTION
    def withdraw(self):
        amount = self.withdraw_entry.get()
        if not amount.isdigit():
            messagebox.showerror("Error", "Please enter a valid amount!")
            return

        try:
            db = get_db_connection()
            cur = db.cursor()

            query = f'SELECT balance FROM customer_info WHERE username = "{self.current_user}" '
            cur.execute(query)
            balance = cur.fetchone()[0]

            # insufficient balance for withdrawal
            if int(amount) > balance:
                messagebox.showerror("Error", "Insufficient balance!")
                return

            # updates the balance amount after withdrawal
            update_query = f'UPDATE customer_info SET balance = balance-{amount} WHERE username = "{self.current_user}" '
            cur.execute(update_query)

            # inserts withdrawal transaction record in user's table
            trans_query = f'INSERT INTO {self.current_user} (Date, Transaction, Amount) VALUES ("{self.curr_date}","Withdraw",{amount})'
            cur.execute(trans_query)

            db.commit()
            messagebox.showinfo("Success", f"Withdrew {amount} successfully!")
            self.show_after_login_options()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # ADMIN LOGIN PAGE
    def show_admin_login(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Admin Login", font=("Arial", 20))
        label.pack(pady=10)

        self.admin_username_entry = ctk.CTkEntry(self, placeholder_text="Admin Username")
        self.admin_username_entry.pack(pady=5)

        self.admin_password_entry = ctk.CTkEntry(self, placeholder_text="Admin Password")
        self.admin_password_entry.pack(pady=5)

        login_btn = ctk.CTkButton(self, text="Log In", command=self.admin_login)
        login_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_main_menu)
        back_btn.pack(pady=5)

    # ADMIN OPTIONS PAGE
    def show_admin_options(self):
        self.clear_frame()

        get_fname=f'select ad_name from admin_info where ad_username="{self.current_admin}"'
        cur.execute(get_fname)
        ad_name=cur.fetchone()[0]

        label = ctk.CTkLabel(self, text=f"Admin Panel - Welcome, {ad_name}", font=("Arial", 20))
        label.pack(pady=20)

        view_customers_btn = ctk.CTkButton(self, text="View All Customers", command=self.view_customers)
        view_customers_btn.pack(pady=10)

        close_account_btn = ctk.CTkButton(self, text="Close Customer Account", command=self.show_close_account_form)
        close_account_btn.pack(pady=10)

        update_customer_btn = ctk.CTkButton(self, text="Update Customer Info", command=self.show_update_customer_form)
        update_customer_btn.pack(pady=10)

        logout_btn = ctk.CTkButton(self, text="Log Out", command=self.logout_admin)
        logout_btn.pack(pady=10)

    # CLOSE ACCOUNT FORM PAGE
    def show_close_account_form(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Close Customer Account", font=("Arial", 20))
        label.pack(pady=20)

        self.customer_id_entry = ctk.CTkEntry(self, placeholder_text="Enter Customer ID")
        self.customer_id_entry.pack(pady=10)

        self.customer_uname_entry = ctk.CTkEntry(self, placeholder_text="Enter Customer Username")
        self.customer_uname_entry.pack(pady=10)

        close_btn = ctk.CTkButton(self, text="Close Account", command=self.close_account)
        close_btn.pack(pady=10) 

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_admin_options)
        back_btn.pack(pady=5)

    # ADMIN LOGIN ACTION
    def admin_login(self):
        ad_username = self.admin_username_entry.get()
        ad_password = self.admin_password_entry.get()
        if ad_password.isdigit():
            ad_password=int(ad_password)

        if not all([ad_username, ad_password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            db = get_db_connection()
            cur = db.cursor()

            # fetches admin password 
            query = f'SELECT ad_passkey FROM admin_info WHERE ad_username = "{ad_username}"'
            cur.execute(query)
            result = cur.fetchall()
            for i in result:
                result=i[0]       

            # fetches all admin usernames
            query2 = 'SELECT ad_username FROM admin_info'
            cur.execute(query2)
            ad_unames_list=[]
            result2 = cur.fetchall()
            for i in result2:
                ad_unames_list.append(i[0])
            
            # checks if admin username exists
            if str(ad_username) in ad_unames_list:
                if ad_password==result:
                    self.current_admin = ad_username
                    messagebox.showinfo("Success", "Admin login successful!")
                    self.show_admin_options()
                else:
                    messagebox.showerror("Error", "Invalid admin credentials!")
            else:
                messagebox.showerror("Error", "Invalid admin credentials \n Admin Not Found!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # VIEW CUSTOMER INFO PAGE
    def view_customers(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="View Customer Details", font=("Arial", 20))
        label.pack(pady=20)

        self.customer_id_entry = ctk.CTkEntry(self, placeholder_text="Enter Customer ID")
        self.customer_id_entry.pack(pady=10)

        close_btn = ctk.CTkButton(self, text="See Info", command=self.see_info)
        close_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_admin_options)
        back_btn.pack(pady=5)

    # SEE INFO ACTION
    def see_info(self):
        customer_id=self.customer_id_entry.get()
        
        try:
            db = get_db_connection()
            cur = db.cursor()

            # fetches customer ids
            cur.execute(self.ids_query)
            ids=cur.fetchall()
            for i in ids:
                self.ids_list.append(i[0])

            # checks if customer id exists
            if int(customer_id) in self.ids_list:
                query = f"SELECT c_id, fname, mname, lname, phoneno, email, date, username, balance FROM customer_info where c_id={customer_id}"
                cur.execute(query)
                customers = cur.fetchall()
                for i in customers:
                    messagebox.showinfo("Customer Details", f'''     CUSTOMER INFO  
                                        
            CUSTOMER ID :   {i[0]}
            FULL NAME :     {i[1]} {i[2]} {i[3]}
            EMAIL ID :     {i[5]}
            PHONE NO. :     {i[4]}
            DATE (ACCOUNT CREATED) :    {i[6]}
            USERNAME :  {i[7]}
            BALANCE :    {i[8]}
    ''')
            else:
                messagebox.showinfo("Customers", "No customers found!")

        except Exception as e:

            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # CLOSE ACCOUNT ACTION
    def close_account(self):
        customer_id = self.customer_id_entry.get()

        try:
            db = get_db_connection()
            cur = db.cursor()

            # checks if customer id is entered in digits
            if not customer_id.isdigit():
                messagebox.showerror("Error", "Please enter a valid customer ID!")
                return
            else:
                # fetches all customer ids
                cur.execute(self.ids_query)
                ids=cur.fetchall()
                for i in ids:
                    self.ids_list.append(i[0])

                # checks if customer id exists
                if int(customer_id) in self.ids_list:
                    customer_uname=self.customer_uname_entry.get()

                    # fetches all usernames
                    cur.execute(self.unames_query)
                    res=cur.fetchall()
                    for i in res:
                        self.unames_list.append(i[0])

                    # checks if username exists
                    if str(customer_uname) in self.unames_list:
                        tablename=customer_uname

                        # query to delete record from customer_info table
                        query = f'DELETE FROM customer_info WHERE c_id = {customer_id}'
                        cur.execute(query)
                        # query to delete the user's table
                        delete_table_query = f'drop table {tablename} '
                        cur.execute(delete_table_query)
                        db.commit()
                        messagebox.showinfo("Success", f"Customer ID {customer_id} account closed successfully!")
                    else:
                        messagebox.showerror("Error","Wrong Username !")
                        self.close_account()
                else:
                    messagebox.showerror("Error","Wrong Customer ID  \n ID not Found !")
                    self.close_account()

            self.show_admin_options()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # UPDATE CUSTOMER FORM PAGE
    def show_update_customer_form(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Update Customer Info", font=("Arial", 20))
        label.pack(pady=20)

         # User ID Entry
        label = ctk.CTkLabel(self, text="User Id", font=("Arial", 15))
        label.place(x=50,y=70)
        self.user_id_var = ctk.StringVar()
        self.user_id_entry = ctk.CTkEntry(self, placeholder_text="Enter User ID", textvariable=self.user_id_var)
        self.user_id_entry.pack(pady=5)

        # Retrieve Button
        self.retrieve_button = ctk.CTkButton(self, text="Retrieve Info", command=self.retrieve_user_info)
        self.retrieve_button.pack(pady=5)

        # Editable Fields
        fname_label = ctk.CTkLabel(self, text="First Name", font=("Arial", 15))
        fname_label.place(x=50,y=150)
        self.first_name_var = ctk.StringVar()
        self.first_name_entry = ctk.CTkEntry(self, textvariable=self.first_name_var)
        self.first_name_entry.pack(pady=5)

        mname_label = ctk.CTkLabel(self, text="Middle Name", font=("Arial", 15))
        mname_label.place(x=50,y=190)
        self.middle_name_var = ctk.StringVar()
        self.middle_name_entry = ctk.CTkEntry(self, textvariable=self.middle_name_var)
        self.middle_name_entry.pack(pady=5)

        lname_label = ctk.CTkLabel(self, text="Last Name", font=("Arial", 15))
        lname_label.place(x=50,y=230)
        self.last_name_var = ctk.StringVar()
        self.last_name_entry = ctk.CTkEntry(self, textvariable=self.last_name_var)
        self.last_name_entry.pack(pady=5)

        phonenolabel = ctk.CTkLabel(self, text="Phone No.", font=("Arial", 15))
        phonenolabel.place(x=50,y=265)
        self.phoneno_var = ctk.IntVar()
        self.phoneno_entry = ctk.CTkEntry(self, textvariable=self.phoneno_var)
        self.phoneno_entry.pack(pady=5)

        gender_label = ctk.CTkLabel(self, text="Gender", font=("Arial", 15))
        gender_label.place(x=50,y=300)
        gender_frame = ctk.CTkFrame(self)
        gender_frame.pack(pady=5)
        self.gender_var = ctk.StringVar()  # *
        male_radio = ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="M")
        male_radio.pack(side="left", padx=5)
        female_radio = ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="F")
        female_radio.pack(side="left", padx=5)

        maritalstatus_label = ctk.CTkLabel(self, text="Marital Status", font=("Arial", 15))
        maritalstatus_label.place(x=50,y=335)
        self.marital_status_var = ctk.StringVar()  
        mstatus_frame = ctk.CTkFrame(self)
        mstatus_frame.pack(pady=5)
        single_radio = ctk.CTkRadioButton(mstatus_frame, text="Single", variable=self.marital_status_var, value="Single")
        single_radio.pack(side="left")
        married_radio = ctk.CTkRadioButton(mstatus_frame, text="Married", variable=self.marital_status_var, value="Married")
        married_radio.pack(side="left")

        education_label = ctk.CTkLabel(self, text="Education Level", font=("Arial", 15))
        education_label.place(x=50,y=370)
        self.education_var = ctk.StringVar()  # set initial value
        edu_dd = ctk.CTkComboBox(self, values=self.edu_level, variable=self.education_var) 
        edu_dd.pack(pady=5)

        occ_label = ctk.CTkLabel(self, text="Occupation", font=("Arial", 15))
        occ_label.place(x=50,y=410)
        self.occ_var = ctk.StringVar()
        self.occupation_ = ctk.CTkComboBox(self, values=self.occupations, variable=self.occ_var)
        self.occupation_.pack(pady=5)

        income_label = ctk.CTkLabel(self, text="Monthly Income", font=("Arial", 15))
        income_label.place(x=50,y=450)
        self.monthly_income_var = ctk.StringVar()
        self.income_ = ctk.CTkComboBox(self, values=self.income_range, variable=self.monthly_income_var)
        self.income_.pack(pady=5)

        # Save Button
        self.save_button = ctk.CTkButton(self, text="Save Changes", command=self.update_user_info)
        self.save_button.pack(pady=5)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_admin_options)
        back_btn.pack(pady=5)

    def retrieve_user_info(self):
        """Retrieve user information from the database."""
        user_id = self.user_id_var.get()
        try:
            db = get_db_connection()
            cursor = db.cursor()
            query = "SELECT fname, mname, lname, phoneno, gender, marital_status, education_level,  occupation, monthly_income FROM customer_info WHERE c_id = %s"
            cursor.execute(query, (user_id))
            result = cursor.fetchone()
            if result:
                self.first_name_var.set(result[0])
                self.middle_name_var.set(result[1])
                self.last_name_var.set(result[2])
                self.phoneno_var.set(result[3])
                self.gender_var.set(result[4])
                self.marital_status_var.set(result[5])
                self.education_var.set(result[6])
                self.occ_var.set(result[7])
                self.monthly_income_var.set(result[8])
            else:
                messagebox.showerror("Error", "User ID not found.")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            db.close()
        
    def update_user_info(self):
        """Update user information in the database."""
        user_id = self.user_id_var.get()
        first_name = self.first_name_var.get()
        middle_name = self.middle_name_var.get()
        last_name = self.last_name_var.get()
        phoneno = self.phoneno_var.get()
        gender = self.gender_var.get()
        marital_status = self.marital_status_var.get()
        education = self.education_var.get()
        occupation = self.occ_var.get()
        income = self.monthly_income_var.get()

        if not all([first_name, middle_name, last_name, phoneno, gender, marital_status, education, occupation, income]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Name validation
        if first_name.isalpha() and middle_name.isalpha() and last_name.isalpha():
            valid_fname=first_name 
            valid_mname=middle_name
            valid_lname=last_name
        else:
            messagebox.showerror("Error",f"Check names again \nNo digits or special characters allowed")

        if phoneno:
            phoneno=str(phoneno)
            if str(phoneno).isdigit() and len(phoneno)==10:
                valid_phoneno=phoneno
            else:
                messagebox.showerror("Error",f"Check phone again Phone No. must be of 10 digits\nNo alphabets or special characters allowed")

        try:
            db = get_db_connection()
            cursor = db.cursor()
            query = """
                UPDATE customer_info 
                SET fname = %s, mname = %s, lname = %s, phoneno = %s, gender = %s, marital_status = %s, education_level = %s, occupation = %s, monthly_income = %s 
                WHERE c_id = %s
            """
            cursor.execute(query, (valid_fname, valid_mname, valid_lname, valid_phoneno, gender, marital_status, education,  occupation, income, user_id))
            db.commit()
            messagebox.showinfo("Success", "User information updated successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if db:
                db.close()


    # LOGOUT ADMIN ACTION
    def logout_admin(self):
        self.current_admin = None
        self.show_main_menu()

    # LOGOUT USER ACTION
    def logout(self):
        self.current_user = None
        self.show_main_menu()

    # STORE ALL CUSTOMER DATA IN EXCEL FILE
    def all_customers(self):
        all='select * from customer_info'
        cur.execute(all)
        all_info=cur.fetchall()
        tablecolumns=["c_id","fname","mname","lname","gender","phoneno","email","aadhaarno","dob","age","occupation","monthly_income","marital_status","education_level","date","username","password","balance"]
        df3=pd.DataFrame(all_info,columns=tablecolumns)
        df3.to_excel('HDFC BANK CUSTOMER INFO.xlsx',index=False)



if __name__ == "__main__":
    app = BankingAppGUI()
    app.mainloop()