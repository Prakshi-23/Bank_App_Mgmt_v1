

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

        self.show_main_menu()
        self.all_customers()

    #MAIN MENU 
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

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

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

        signup_btn = ctk.CTkButton(self, text="Create Account", command=self.signup)
        signup_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.show_main_menu)
        back_btn.pack(pady=5)

    def signup(self):
        fname = self.fname_entry.get()
        mname = self.mname_entry.get()
        lname = self.lname_entry.get()
        phoneno = self.phoneno_entry.get()
        aadhaarno = self.aadhaarno_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not all([fname, mname, lname, phoneno, aadhaarno, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            db=get_db_connection()
            cur=db.cursor()
            unames_query='select username from customer_info'
            cur.execute(unames_query)
            unames_list=[]
            unames=cur.fetchall()
            for i in unames:
                unames_list.append(i[0])

            if not fname.isalpha():
                messagebox.showerror("Error", "First Name: No Digits or Special Charaters Allowed!")
                return
            else:
                fname=fname.title()

            if not mname.isalpha():
                messagebox.showerror("Error", "Middle Name: No Digits or Special Charaters Allowed!")
                return
            else:
                mname=mname.title()

            if not lname.isalpha():
                messagebox.showerror("Error", "Last Name: No Digits or Special Charaters Allowed!")
                return
            else:
                lname=lname.title()    

            if str(username) not in unames_list:
                if not ((len(username)>=4 and len(username)<=10 )and username.isalpha()):
                    messagebox.showerror("Error", "Username must be of 4-10 alphabets !")
                    return
                else:
                    username = username.lower()
            else:
                messagebox.showerror("Error","An error occurred: Username exists already ! \nTry a new one !! ")

            if fname and mname and lname and username:
                query = "insert into customer_info (fname, mname, lname, date, username, balance) VALUES (%s, %s, %s, %s, %s, %s)"
                cur.execute(query, (fname, mname, lname,{self.curr_date}, username,0))
                tablename=username

                id=f'select c_id from customer_info where username="{username}"'
                cur.execute(id)
                c_id=cur.fetchall()
                for i in c_id:
                    c_id=i[0]
            else:
                messagebox.showerror("Error","Check info again !! ")
            

            if not (len(phoneno)==10 and phoneno.isdigit()):
                messagebox.showerror("Error", "Phone No. must be of 10 digits!")
                return
            else:
                set_phone=f'update customer_info set phoneno="{phoneno}" where c_id={c_id}'
                cur.execute(set_phone)
                db.commit()

            if not (len(aadhaarno)==12 and aadhaarno.isdigit()):
                messagebox.showerror("Error", "Aadhaar No. must be of 12 digits!")
                return
            else:
                set_aadhaar=f'update customer_info set aadhaarno="{aadhaarno}" where c_id={c_id}'
                cur.execute(set_aadhaar)
                db.commit()

            if (len(password)==4 and password.isdigit()):
                if password != confirm_password:
                    messagebox.showerror("Error", "Check Password Again!")
                    return

                else:
                    set_ps=f'update customer_info set password="{password}" where c_id={c_id}'
                    cur.execute(set_ps)
                    db.commit()
            else:
                messagebox.showerror("Error", "Password must be of 4 digits!")
                return

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

        try:
            db=get_db_connection()
            cur=db.cursor()

            messagebox.showinfo("Success", f'''Account created successfully!
            FULL NAME : {fname} {mname} {lname}
            CUSTOMER ID : {c_id}
            PHONE NO. : {phoneno}
            AADHAAR NO. : {aadhaarno}
            USERNAME : {username}
                                ''')
            create_table_query=f'create table {tablename} (`Sr_No` int primary key auto_increment,`Date` date, `Transaction` varchar(10), `Amount` int)'
            cur.execute(create_table_query)
            db.commit()
            self.show_main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()


    def signin(self):
        username = self.login_username_entry.get()
        self.current_user = username.lower()
        password = self.login_password_entry.get()

        if not all([username, password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            db=get_db_connection()
            cur=db.cursor()
            cur.execute(self.unames_query)
            unames=cur.fetchall()
            for i in unames:
                self.unames_list.append(i[0])
            if str(self.current_user) in self.unames_list:
                get_ps=f'select password from customer_info where username="{self.current_user}"'
                cur.execute(get_ps)
                ps=cur.fetchall()
                for i in ps:
                    ps=i[0]
                fname=f'select fname from customer_info where username="{self.current_user}" '
                cur.execute(fname)
                fname=cur.fetchall()
                for i in fname:
                    fname=i[0]
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

    def c_ids(self):
        cur.execute(self.ids_list)
        cids=cur.fetchall()
        for i in cids:
            self.ids_list.append(i)

    def show_after_login_options(self):
        self.clear_frame()
        
        db=get_db_connection()
        cur=db.cursor()

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

    def check_balance(self):
        try:
            db = get_db_connection()
            cur = db.cursor()

            query = f'SELECT balance FROM customer_info WHERE username ="{self.current_user}"'
            cur.execute(query)
            balance = cur.fetchone()[0]

            messagebox.showinfo("Balance", f"Your current balance is: {balance}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

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

    def change_password(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()

        if not all([current_password, new_password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            db = get_db_connection()
            cur = db.cursor()

            query = f'SELECT password FROM customer_info WHERE username = "{self.current_user}"'
            cur.execute(query)
            stored_password = cur.fetchone()[0]
            if stored_password==current_password:
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

    def transaction_report(self):
        try:
            db = get_db_connection()
            cur = db.cursor()

            info_query=f'select c_id,fname,mname,lname,balance from customer_info where username="{self.current_user}"'
            cur.execute(info_query)
            info = cur.fetchone()

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
                title="Save Transaction Report"
            )

            if not file_path:
                return  # User canceled the save dialog

            # Generate the PDF
            self.generate_pdf(info, transactions, file_path)

            messagebox.showinfo("Success", "Transaction report saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

    def generate_pdf(self, info, transactions, file_path):
        try:
            get_fname=f'select fname from customer_info where username="{self.current_user}"'
            cur.execute(get_fname)
            fname_=cur.fetchone()[0]

            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter

            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 50, f"Transaction Report for {fname_}")

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


    def deposit(self):
        amount = self.deposit_entry.get()
        if not amount.isdigit():
            messagebox.showerror("Error", "Please enter a valid amount!")
            return

        try:
            db = get_db_connection()
            cur = db.cursor()

            query = f'UPDATE customer_info SET balance = balance +{amount} WHERE username = "{self.current_user}"'
            cur.execute(query)

            trans_query = f'INSERT INTO {self.current_user} (Date, Transaction, Amount) VALUES ("{self.curr_date}","Deposit",{amount})'
            cur.execute(trans_query)

            db.commit()
            messagebox.showinfo("Success", f"Deposited {amount} successfully!")
            self.show_after_login_options()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

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

            if int(amount) > balance:
                messagebox.showerror("Error", "Insufficient balance!")
                return

            update_query = f'UPDATE customer_info SET balance = balance-{amount} WHERE username = "{self.current_user}" '
            cur.execute(update_query)

            trans_query = f'INSERT INTO {self.current_user} (Date, Transaction, Amount) VALUES ("{self.curr_date}","Deposit",{amount})'
            cur.execute(trans_query)

            db.commit()
            messagebox.showinfo("Success", f"Withdrew {amount} successfully!")
            self.show_after_login_options()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

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
            if not customer_id.isdigit():
                messagebox.showerror("Error", "Please enter a valid customer ID!")
                return
            if field=="fname" or field=="mname" or field=="lname":
                if new_value.isalpha():
                    update_info=f'update customer_info set {field} = "{new_value.title()}" where c_id={customer_id}'
                    cur.execute(update_info)
                    db.commit()
                    messagebox.showinfo("Success",f" Customer ID : {customer_id} Updated successfully !")

                else:
                    messagebox.showerror("Error",f"Check {field} again \nNo digits or special characters allowed")

            elif field=="phoneno":
                if new_value.isdigit() and len(new_value)==10:
                    update_info=f'update customer_info set {field} = "{new_value}" where c_id={customer_id}'
                    cur.execute(update_info)
                    db.commit()
                    messagebox.showinfo("Success",f" Customer ID : {customer_id} Updated successfully !")
                else:
                    messagebox.showerror("Error",f"Check {field} again Phone No. must be of 10 digits\nNo alphabets or special characters allowed")

            elif field=="username":
                old_uname=f'select username from customer_info where c_id={customer_id}'
                cur.execute(old_uname)
                old_customer_uname=cur.fetchone()[0]

                tablename=old_customer_uname
                cur.execute(self.unames_query)
                unames=cur.fetchall()
                for i in unames:
                    self.unames_list.append(i[0])
                # messagebox.showinfo("usernames",f"{self.unames_list}")
                if str(new_value) not in self.unames_list:
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

    def logout_admin(self):
        self.current_admin = None
        self.show_main_menu()

    def logout(self):
        self.current_user = None
        self.show_main_menu()

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