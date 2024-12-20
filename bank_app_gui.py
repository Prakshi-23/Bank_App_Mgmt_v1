

import datetime
import customtkinter as ctk
from tkinter import messagebox, filedialog
import pymysql as myconn
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


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
        self.curr_date=datetime.datetime.now().strftime("%Y-%m-%d")
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
        self.tablename=""
        self.c_id=0

        self.show_main_menu()
        self.all_customers()

    # MAIN MENU PAGE
    def show_main_menu(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Welcome to HDFC Bank", font=("Arial", 24))
        label.pack(pady=20)

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

        aadhaarnolabel = ctk.CTkLabel(self, text="Aadhaar No.", font=("Arial", 15))
        aadhaarnolabel.place(x=50,y=209)
        self.aadhaarno_entry = ctk.CTkEntry(self, placeholder_text="Aadhaar No.")
        self.aadhaarno_entry.pack(pady=5)

        usernamelabel = ctk.CTkLabel(self, text="Username", font=("Arial", 15))
        usernamelabel.place(x=50,y=248)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="e.g. userabc")
        self.username_entry.pack(pady=5)

        passwordlabel = ctk.CTkLabel(self, text="Set Password", font=("Arial", 15))
        passwordlabel.place(x=50,y=287)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="e.g. 1234")
        self.password_entry.pack(pady=5)

        confirm_passwordlabel = ctk.CTkLabel(self, text="Confirm Password", font=("Arial", 15))
        confirm_passwordlabel.place(x=50,y=326)
        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text=" ")
        self.confirm_password_entry.pack(pady=5)

        signup_btn = ctk.CTkButton(self, text="Submit Info", command=self.submit_info )
        signup_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_main_menu)
        back_btn.pack(pady=5)

    # SUBMIT ALL THE DETAILS - CHECKS ALL THE FIELDS IF VALID
    def submit_info(self):
        self.fname = self.fname_entry.get()
        self.mname = self.mname_entry.get()
        self.lname = self.lname_entry.get()
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
            if (len(self.password)==4 and self.password.isdigit()):
                if self.password != confirm_password:
                    messagebox.showerror("Error", "Check Password Again!")
                    return
                else:
                    self.valid_password=self.password
            else:
                messagebox.showerror("Error", "Password must be of 4 digits!")
                return
            
            # if all fields are valid then only show the create account option
            if self.valid_fname and self.valid_mname and self.valid_lname and self.valid_phoneno and self.valid_aadhaar and self.valid_username and self.valid_password:
                create_btn = ctk.CTkButton(self, text="Create Account", command=self.create_account )
                create_btn.pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # CREATES ACCOUNT - ADD DETAILS IN CUSTOMER INFO AND CREATES TABLE  (SIGNUP ACTION)
    def create_account(self):
        if self.valid_fname and self.valid_mname and self.valid_lname and self.valid_phoneno and self.valid_aadhaar and self.valid_username and self.valid_password:
            try:
                db=get_db_connection()
                cur=db.cursor()

                # insert query inserts records in customer info
                query = "insert into customer_info (fname, mname, lname, phoneno, aadhaarno, date, username, password, balance) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
                cur.execute(query, (self.valid_fname, self.valid_mname, self.valid_lname, self.valid_phoneno, self.valid_aadhaar, {self.curr_date}, self.valid_username, self.valid_password,0))

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
                    ps=i[0]

                # fetches first name of user
                fname=f'select fname from customer_info where username="{self.current_user}" '
                cur.execute(fname)
                fname=cur.fetchall()
                for i in fname:
                    fname=i[0]

                # if user enter correct password 
                if password==ps:
                    messagebox.showinfo("Success", f"Welcome back, {fname}!")
                    self.show_after_login_options()
                else:
                    messagebox.showerror("Error", "Invalid Password !")
            else:
                messagebox.showerror("Error", "Invalid username !")
        except Exception as e:
            messagebox.showerror("Error",f"An error occurred: {e} !! ")
        finally:
            db.close()

    # SIGNIN ACTION
    def show_signin_form(self):
        self.clear_frame()

        label = ctk.CTkLabel(self, text="Sign In", font=("Arial", 20))
        label.pack(pady=10)

        self.login_username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.login_username_entry.pack(pady=5)

        self.login_password_entry = ctk.CTkEntry(self, placeholder_text="Password") # , show="*"
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

            # fetches user information
            info_query=f'select c_id,fname,mname,lname,balance from customer_info where username="{self.current_user}"'
            cur.execute(info_query)
            info = cur.fetchone()

            # fetches all transaction records stored in user's table
            query = f'SELECT * FROM {self.current_user}'
            cur.execute(query)
            transactions = cur.fetchall()

            if not transactions:
                messagebox.showinfo("Transactions", "No transactions found!")
                return

            # Ask the user for a file location to save the PDF
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Transaction Report")

            if not file_path:
                return  # User canceled the save dialog

            # Generate the PDF
            self.generate_pdf(info, transactions, file_path)

            messagebox.showinfo("Success", "Transaction report saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    # CONTENT INSIDE PDF
    def generate_pdf(self, info, transactions, file_path):
        try:
            # fetches firstname of user
            get_fname=f'select fname from customer_info where username="{self.current_user}"'
            cur.execute(get_fname)
            fname_=cur.fetchone()[0]

            # pdf page
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter

            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 50, f"Transaction Report for {fname_}")

            # info at top of pdf
            c.setFont("Helvetica", 12)
            y = height - 80
            customer_details = [
                f"Customer ID: {info[0]}                   Full Name: {info[1]}  {info[2]} {info[3]}",
                f"Current Balance: Rs. {info[4]}"
            ]

            for detail in customer_details:
                c.drawString(50, y, detail)
                y -= 20

            # Leave some space before transaction data
            y -= 10
            c.drawString(50, y, "Transactions:")
            y -= 20


            c.setFont("Helvetica", 12)
            y = height - 170

            c.drawString(50, y, "Sr.No.")
            c.drawString(100, y, "Date")
            c.drawString(200, y, "Transaction")
            c.drawString(300, y, "Amount")
            y -= 20

            for trans_action in transactions:
                sr_no, date, transaction, amount = trans_action
                c.drawString(50, y, str(sr_no))
                c.drawString(100, y, str(date))
                c.drawString(200, y, str(transaction))
                c.drawString(300, y, str(amount))
                y -= 20

                

                if y < 50:  # Create a new page if space runs out
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = height - 50

            c.save()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {e}")

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
            trans_query = f'INSERT INTO {self.current_user} (Date, Transaction, Amount) VALUES ("{self.curr_date}","Deposit",{amount})'
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
            query = f'SELECT ad_passkey FROM admin_info WHERE ad_username = "{ad_username}"'
            cur.execute(query)
            result = cur.fetchall()
            for i in result:
                result=i[0]       

            query2 = 'SELECT ad_username FROM admin_info'
            cur.execute(query2)
            ad_unames_list=[]
            result2 = cur.fetchall()
            for i in result2:
                ad_unames_list.append(i[0])
            
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

            cur.execute(self.ids_query)
            ids=cur.fetchall()
            for i in ids:
                self.ids_list.append(i[0])

            if int(customer_id) in self.ids_list:
                query = f"SELECT c_id,fname,mname,lname,phoneno,date,username,balance FROM customer_info where c_id={customer_id}"
                cur.execute(query)
                customers = cur.fetchall()
                for i in customers:
                    messagebox.showinfo("Customer Details", f'''     CUSTOMER INFO  
                                        
            CUSTOMER ID :   {i[0]}
            FULL NAME :     {i[1]} {i[2]} {i[3]}
            PHONE NO. :     {i[4]}
            DATE (ACCOUNT CREATED) :    {i[5]}
            USERNAME :  {i[6]}
            BALANCE :    {i[7]}
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

            if not customer_id.isdigit():
                messagebox.showerror("Error", "Please enter a valid customer ID!")
                return
            else:
                cur.execute(self.ids_query)
                ids=cur.fetchall()
                for i in ids:
                    self.ids_list.append(i[0])
                if int(customer_id) in self.ids_list:
                    customer_uname=self.customer_uname_entry.get()
                    cur.execute(self.unames_query)
                    res=cur.fetchall()
                    for i in res:
                        self.unames_list.append(i[0])
                    if str(customer_uname) in self.unames_list:
                        tablename=customer_uname
                        query = f'DELETE FROM customer_info WHERE c_id = {customer_id}'
                        cur.execute(query)
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

        self.customer_id_entry = ctk.CTkEntry(self, placeholder_text="Enter Customer ID")
        self.customer_id_entry.pack(pady=10)

        self.field_selector = ctk.CTkOptionMenu(self, values=["fname", "mname", "lname", "phoneno", "username"])
        self.field_selector.set("Select Field")
        self.field_selector.pack(pady=10)

        self.new_value_entry = ctk.CTkEntry(self, placeholder_text="New Value")
        self.new_value_entry.pack(pady=10)

        update_btn = ctk.CTkButton(self, text="Update Info", command=self.update_customer_info)
        update_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_admin_options)
        back_btn.pack(pady=5)

    # UPDATE CUSTOMER INFO ACTION
    def update_customer_info(self):
        customer_id = self.customer_id_entry.get()
        field = self.field_selector.get()
        new_value = self.new_value_entry.get()

        if not all([customer_id, field, new_value]) or field == "Select Field":
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            db = get_db_connection()
            cur = db.cursor()

            # checks customer id
            if not customer_id.isdigit():
                messagebox.showerror("Error", "Please enter a valid customer ID!")
                return
            
            # Name validation
            if field=="fname" or field=="mname" or field=="lname":
                if new_value.isalpha():
                    update_info=f'update customer_info set {field} = "{new_value.title()}" where c_id={customer_id}'
                    cur.execute(update_info)
                    db.commit()
                    messagebox.showinfo("Success",f" Customer ID : {customer_id} Updated successfully !")

                else:
                    messagebox.showerror("Error",f"Check {field} again \nNo digits or special characters allowed")

            # phone no validation
            elif field=="phoneno":
                if new_value.isdigit() and len(new_value)==10:
                    update_info=f'update customer_info set {field} = "{new_value}" where c_id={customer_id}'
                    cur.execute(update_info)
                    db.commit()
                    messagebox.showinfo("Success",f" Customer ID : {customer_id} Updated successfully !")
                else:
                    messagebox.showerror("Error",f"Check {field} again Phone No. must be of 10 digits\nNo alphabets or special characters allowed")

            # username validation
            elif field=="username":
                old_uname=f'select username from customer_info where c_id={customer_id}'
                cur.execute(old_uname)
                old_customer_uname=cur.fetchone()[0]

                # rename user's table
                tablename=old_customer_uname
                cur.execute(self.unames_query)
                unames=cur.fetchall()
                for i in unames:
                    self.unames_list.append(i[0])

                # messagebox.showinfo("usernames",f"{self.unames_list}")

                # checks if new username doesn't exists already
                if str(new_value) not in self.unames_list:

                    # new username validation
                    if new_value.isalpha() and (len(new_value)>=4 and len(new_value)<=10):
                        update=f'update customer_info set username="{new_value}" where c_id={customer_id}'
                        
                        update_tablename_query = f'rename table {tablename} to {new_value}'
                        cur.execute(update)
                        cur.execute(update_tablename_query)
                        db.commit()
                        messagebox.showinfo("Success",f" Customer ID : {customer_id} Updated successfully !")

                    else:
                        messagebox.showerror("Error","Wrong Username - Username must be of 4-10 alphabets !")
                else:
                    messagebox.showerror("Error","Username exists already !")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
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
        tablecolumns=["c_id","fname","mname","lname","phoneno","aadhaarno","date","username","password","balance"]
        df3=pd.DataFrame(all_info,columns=tablecolumns)
        df3.to_excel('HDFC BANK CUSTOMER INFO.xlsx',index=False)
        
if __name__ == "__main__":
    app = BankingAppGUI()
    app.mainloop()
