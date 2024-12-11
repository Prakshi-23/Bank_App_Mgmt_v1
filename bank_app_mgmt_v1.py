import pymysql as myconn
# import mysql.connector as myconn
 
db=myconn.connect(host="localhost",
                  user="root",
                  password="root",
                  database="new_bank")

cur=db.cursor()

class BANK():

    def __init__(self,bank_name):
        import datetime
        self.bank_name=bank_name
        self.username=""
        self.password=""
        self.cid=""
        self.fname=""
        self.mname=""
        self.lname=""
        self.cust_list=[]
        self.all_customers=""
        self.records=""
        self.tablename=""
        self.count=0
        self.t=0
        self.c_ids_list=[]
        self.x=datetime.datetime.now()
        self.curr_date=self.x.strftime("%Y-%m-%d")
        self.c_id=0
        


    def welcome_user(self):
        
        print("====================================")
        print(f"\tWELCOME TO {self.bank_name.upper()} BANK APP")
        print("====================================")
        
        print("DATE:",self.curr_date )

    def main_menu(self):
        print("1.SIGNUP \n2.SIGNIN \n3.ADMIN LOGIN")
        self.op=int(input("SELECT OPTION : "))

    def create_new_acc(self):
        print('''
        ----------------------------
               CREATE ACCOUNT 
        ----------------------------''')

        self.update_fname()
        self.update_mname()
        self.update_lname()
        insertname_query = f'insert into customer_info(fname,mname,lname) values("{self.fname}","{self.mname}","{self.lname}")' 
        cur.execute(insertname_query)
        db.commit()
        self.id=f'select c_id from customer_info where fname="{self.fname}"'
        cur.execute(self.id)
        #db.commit()
        self.result=cur.fetchall()
        for i in self.result:
            self.cid=(i[0])

        self.update_phoneno()
        self.update_aadhaar()
        self.update_username()
        self.update_password()
        self.set_balance_date()
        self.create_table()
        self.print_acc_details()

    def create_table(self):
        self.tablename=self.username
        create_table_query=f'create table `{self.tablename}` (`Sr_no` int primary key auto_increment,`Date` date, `Transaction` varchar(10), `Amount` int)'
        cur.execute(create_table_query)
        db.commit()

    def update_fname(self):
        self.fname=input('ENTER FIRST NAME : ')
        if self.fname.isalpha():
            self.fname=self.fname.title()
        else:
            print("NO DIGITS OR SPECIAL CHARACTERS ALLOWED")
            self.update_fname()

    def update_mname(self):
        self.mname=input('ENTER MIDDLE NAME : ')
        if self.fname.isalpha():
            self.mname=self.mname.title()
        else:
            print("NO DIGITS OR SPECIAL CHARACTERS ALLOWED")
            self.update_mname()

    def update_lname(self):
        self.lname=input('ENTER LAST NAME : ')
        if self.lname.isalpha():
            self.lname=self.lname.title()
        else:
            print("NO DIGITS OR SPECIAL CHARACTERS ALLOWED")
            self.update_lname()

    def update_phoneno(self):
        self.phoneno=input("ENTER PHONE NO. : ")
        updatephone_query=f'update customer_info set phoneno="{self.phoneno}" where c_id={self.cid}'
        if len(self.phoneno)==10 and str(self.phoneno).isdigit():
            cur.execute(updatephone_query)
            db.commit()
        else:
            print("PLEASE CHECK PHONE NO. AGAIN  MUST CONTAIN 10 DIGITS")
            self.update_phoneno()

    def update_aadhaar(self):
        self.adharno=input("ENTER AADHAAR NO. : ")
        updateadhar_query=f'update customer_info set aadhaarno="{self.adharno}" where c_id={self.cid}'
        if len(self.adharno)==12 and str(self.adharno).isdigit():
            cur.execute(updateadhar_query)
            db.commit()
        else:
            print("PLEASE CHECK AADHAAR NO. AGAIN MUST CONTAIN 12 DIGITS")
            self.update_aadhaar()   

    def update_username(self):
        self.username=input("ENTER USERNAME : ")
        self.username=self.username.lower()
        updateuname_query=f'update customer_info set username="{self.username}" where c_id={self.cid}'
        if self.username in self.cust_list:
            print("USERNAME ALREADY EXISTS \n TRY NEW USERNAME ")
            self.update_username()
        else:
            if (len(self.username)>=4 and len(self.username)<=10) and str(self.username).isalpha():
                cur.execute(updateuname_query)
                db.commit()
            else:
                print("PLEASE CHECK AGAIN USERNAME MUST CONTAIN 4-10 ALPHABETS IN SMALL CAPS \nNO DIGITS OR SPECIAL CHARACTERS E.G.- @,!,#,$ etc")
                self.update_username()

    def update_password(self):
        self.password=input("SET PASSWORD : ")
        updateps_query=f'update customer_info set password="{self.password}" where c_id={self.cid}'
        if len(self.password)==4 and str(self.password).isdigit():
            self.cps=input("CONFIRM PASSWORD : ")
            if self.cps==self.password:
                cur.execute(updateps_query)
                db.commit()
            else:
                print("PASSWORD DOESN'T MATCH \n CHECK AGAIN")
                self.update_password()
        else:
            print("PLEASE CHECK AGAIN PASSWORD MUST CONTAIN 4 DIGITS \nNO ALPHABETS OR SPECIAL CHARACTERS E.G.- @,!,#,$ etc")
            self.update_password()        

    def print_acc_details(self):
        print('''
        --------------------------------------
            ACCOUNT CREATED SUCCESSFULLY!!!
        --------------------------------------''')
        print("---------- ACCOUNT DETAILS --------------")
        self.details=f'select * from customer_info where c_id="{self.cid}"'
        cur.execute(self.details)
        self.results=cur.fetchall()
        for i in self.results:
            print("FULL NAME : ",i[1],i[2],i[3])
            print("CUSTOMER ID : ",i[0])
            print("PHONE NO. : ",i[4])
            print("AADHAAR NO. : ",i[5])
            print("USERNAME : ",i[7])
            print("================================")

    def set_balance_date(self):
        set_bal_query=f'update customer_info set balance=0 where username="{self.username}"'
        set_date_query=f'update customer_info set date="{self.curr_date}" where username="{self.username}"'
        cur.execute(set_bal_query)
        cur.execute(set_date_query)
        db.commit()


    def login(self):
        while(True):
            self.cust_list=[]
            self.all_customers='select username from customer_info'
            cur.execute(self.all_customers)
            self.records=cur.fetchall()
            for i in self.records:
                self.cust_list.append(i[0])
            #print(self.cust_list)
            print('''
            -----------------------
                    LOGIN 
            -----------------------''')
            self.ask_username()

    def ask_username(self):
        self.u_name=input("ENTER USERNAME : ")
        self.u_name=self.u_name.lower()
        if self.u_name in self.cust_list:
            self.ask_password()
        else:
            print("WRONG USERNAME")
            self.ask_username()
            

    def ask_password(self):
        self.ps=input("ENTER PASSWORD : ")
        self.trueps=f'select password from customer_info where username="{self.u_name}"'
        cur.execute(self.trueps)
        self.passkey=cur.fetchall()
        for i in self.passkey:
            self.true_ps=(i[0])
        if self.ps==self.true_ps:
            print('''
    ----------------------------
        LOGIN SUCCESSFUL!!!
    ----------------------------''')
            while(True):
                self.afterlogin_options()
        else:
            self.count+=1
            print("INCORRECT PASSWORD")
            print(self.count)
            if self.count==3:
                self.count=0
                self.wrong_password()
                
            else:
                self.ask_password()

    def wrong_password(self):
        import time
        print("3 UNSUCCESSFUL TRIES")
        print("TRY LOGIN AGAIN AFTER 30 SECS ")
        self.countdown() 
        time.sleep(3)
        self.login()

    def countdown(self): 
        import time 
        self.t = 30
        while self.t: 
            mins, secs = divmod(self.t, 60) 
            timer = '{:02d}:{:02d}'.format(mins, secs) 
            print(timer, end="\r") 
            time.sleep(1) 
            self.t -= 1

    def afterlogin_options(self):
            print('''
                1.DEPOSIT
                2.WITHDRAW
                3.CHECK BALANCE
                4.TRANSACTION REPORT
                5.CHANGE PASSWORD
                6.EXIT
                ''' )
            self.choice=int(input("SELECT A OPTION : "))
            if self.choice==1:
                self.deposit()
            elif self.choice==2:
                self.withdraw()
            elif self.choice==3:
                self.check_balance()
            elif self.choice==4:
                self.transaction_report()
            elif self.choice==5:
                self.change_password()
            elif self.choice==6:
                self.exit()

            else:
                print("INVALID CHOICE")

    def deposit(self):
        self.tablename=self.u_name
        self.amt=int(input("ENTER AMOUNT TO DEPOSIT : "))
        deposit_query=f'update customer_info set balance=balance+{self.amt} where username="{self.u_name}"'
        depo_entry_query=f'insert into {self.tablename}(Date,Transaction,Amount) values("{self.curr_date}","Deposit",{self.amt})'
        cur.execute(deposit_query)
        cur.execute(depo_entry_query)
        db.commit()
        print(f"Rs.{self.amt} SUCCESSFULLY DEPOSITED IN YOUR ACCOUNT !")

    def withdraw(self):
        self.tablename=self.u_name
        self.amt=int(input("ENTER AMOUNT TO WITHDRAW : "))
        self.bal=f'select balance from customer_info where username="{self.u_name}"'
        cur.execute(self.bal)
        cbal=cur.fetchall()
        for i in cbal:
            self.balance=i[0]
        if self.amt>self.balance:
            print("!!!!!! INSUFFICIENT BALANCE \n  WITHDRAW UNSUCCESSFUL !!!!!!")
                
        else:
            withdraw_query=f'update customer_info set balance=balance-{self.amt} where username="{self.u_name}"'
            wdrw_entry_query=f'insert into {self.tablename}(Date,Transaction,Amount) values("{self.curr_date}","Withdraw",{self.amt})'
            cur.execute(withdraw_query)
            cur.execute(wdrw_entry_query)
            db.commit()
            print(f"RS.{self.amt} SUCCESSFULLY WITHDRAWN FROM YOUR ACCOUNT !")

    def check_balance(self):
        print("-----------------------------")
        self.u_name=self.u_name
        self.bal=f'select balance from customer_info where username="{self.u_name}"'
        cur.execute(self.bal)
        self.balance=cur.fetchall()
        for i in self.balance:
            print("CURRENT BALANCE : ","RS.",i[0])
        print("-----------------------------")

    def transaction_report(self):
        print('''
    ============================
        TRANSACTION REPORT
    ============================''')
        self.tablename=self.u_name
        records_query=f'select * from {self.tablename}'
        cur.execute(records_query)
        transac_records=cur.fetchall()
        print("-----------------------------------------------------------")
        print("Sr.No.","      ","Date","        ","Transaction","         ","Amount")
        print("-----------------------------------------------------------")
        for i in transac_records:
            print("------------------------------------------------------------")
            print(i[0],"        ",i[1],"        ",i[2],"        ",i[3])
            print("------------------------------------------------------------")
        self.check_balance()

    def exit(self):
        print('''
    ----------------------------
        !!     BYE     !!
    ----------------------------''')
        self.process()

    def change_password(self):
        self.passwd=input("ENTER CURRENT PASSWORD : ")
        self.true_ps=self.true_ps
        if self.passwd==self.true_ps:
            self.newpass=input("SET NEW PASSWORD : ")
            updatepskey_query=f'update customer_info set password="{self.newpass}" where username="{self.u_name}"'
            if len(self.newpass)==4 and str(self.newpass).isdigit():
                self.cps=input("CONFIRM NEW PASSWORD : ")
                if self.cps==self.newpass:
                    cur.execute(updatepskey_query)
                    db.commit()
                else:
                    print("PASSWORD DOESN'T MATCH \n CHECK AGAIN")
                    self.change_password()
            else:
                print("PLEASE CHECK AGAIN PASSWORD MUST CONTAIN 4 DIGITS \nNO ALPHABETS OR SPECIAL CHARACTERS E.G.- @,!,#,$ etc")
                self.change_password()
        else:
            print("INCORRECT PASSWORD")
            self.change_password()


    def admin_login(self):
        print('''
        ----------------------------
                ADMIN LOGIN
        ----------------------------''')
        self.ask_username_admin()


    def ask_username_admin(self):
        self.list2=[]
        admin_list=f'select ad_username from admin_info'
        cur.execute(admin_list)
        #db.commit()
        list2=cur.fetchall()
        for i in list2:
            self.list2.append(i[0])
        print(self.list2)
        self.u_name_=input("ENTER USERNAME : ")
        self.u_name_=self.u_name_.lower()
        if self.u_name_ in self.list2:
            self.ask_password_admin()
        else:
            print("WRONG USERNAME")
            self.ask_username_admin()
            

    def ask_password_admin(self):
        self.list3=[]
        admin_ps_list=f'select ad_passkey from admin_info'
        cur.execute(admin_ps_list)
        #db.commit()
        list3=cur.fetchall()
        for i in list3:
            self.list3.append(i[0])
        print(self.list3)
        self.pskey=input("ENTER PASSWORD : ")
        self.pskey=int(self.pskey)
        self.actualps=f'select ad_passkey from admin_info where ad_username="{self.u_name_}"'
        cur.execute(self.actualps)
        self.passkey=cur.fetchall()
        for i in self.passkey:
            self.actual_ps=(i[0])
        print(self.actual_ps)
        if self.pskey==self.actual_ps:
            print('''
    ----------------------------
        LOGIN SUCCESSFUL!!!
    ----------------------------''')
            while(True):
                self.admin_options()
        else:
            print("INCORRECT PASSWORD")
            self.ask_password_admin()

    def admin_options(self):
        print('''
            1.SEE CUSTOMERS INFO
            2.CLOSE CUSTOMER ACCOUNT
            3.UPDATE CUSTOMER INFO
            4.EXIT
        ''')
        opt=int(input("SELECT A OPTION : "))
        if opt==1:
            self.customer_details()
        elif opt==2:
            self.close_cust_acc()
        elif opt==3:
            self.update_cust_details()
        elif opt==4:
            self.admin_exit_()
           
    def customer_details(self):
        c_ids_query='select c_id from customer_info'
        cur.execute(c_ids_query)
        self.c_ids_list=[]
        c_ids=cur.fetchall()
        for i in c_ids:
            self.c_ids_list.append(i[0])
        #print(self.c_ids_list)
        print("CUSTOMER DETAILS")
        self.c_id=input("ENTER CUSTOMER ID : ")
        if self.c_id.isdigit():
            self.c_id=int(self.c_id)
            if self.c_id in self.c_ids_list:
                one_customer=f'select * from customer_info where c_id={self.c_id}'
                cur.execute(one_customer)
                self.records=cur.fetchall()
                print('''
                --------------------------
                    CUSTOMER DETAILS
                --------------------------''')
                for i in self.records:
                    print(f'''
                        CUSTOMER ID : {i[0]}
                        FULL NAME : {i[1]} {i[2]} {i[3]}
                        PHONE NO. : {i[4]}
                        AADHAAR NO. : {i[5]}
                        DATE (ACCOUNT CREATION): {i[6]}
                        USERNAME : {i[7]}
                        PASSWORD : {i[8]}
                        BALANCE : {i[9]}
                        ''')
                    
                transac_also=input("DO YOU WANT TO SEE TRANSACTION HISTORY AS WELL ? \nYES (Y) OR NO (N) ")
                transac_also=transac_also.lower()

                if transac_also=='y':
                    get_uname=f'select username from customer_info where c_id={self.c_id}'
                    cur.execute(get_uname)
                    username=cur.fetchall()
                    for i in username:
                        username=i[0]
                    tablename=username
                    transac_hist_query=f'select * from {tablename}'
                    cur.execute(transac_hist_query)
                    transac_hist=cur.fetchall()
                    if len(transac_hist)==0:
                        print("NO TRANSACTIONS YET")
                    else:
                        for i in transac_hist:
                            print(i[0],i[1],i[2],i[3])
            else:
                print("ID NOT FOUND")
                self.update_cust_details()

    def close_cust_acc(self):
        print('''
        ----------------------------
           CLOSE CUSTOMER ACCOUNT
        ----------------------------''')
        self.all_customers='select username from customer_info'
        cur.execute(self.all_customers)
        self.records=cur.fetchall()
        for i in self.records:
            self.cust_list.append(i[0])
        #print(self.cust_list)
        self.cust_id=input("ENTER CUSTOMER ID : ")
        if self.cust_id.isnumeric():
            self.cust_id=int(self.cust_id)
        else:
            print("CUSTOMER ID NOT FOUND")
            self.admin_options()
        c_ids_query='select c_id from customer_info'
        cur.execute(c_ids_query)
        self.c_ids_list=[]
        c_ids=cur.fetchall()
        for i in c_ids:
            self.c_ids_list.append(i[0])
        #print(self.c_ids_list)

        if self.cust_id in self.c_ids_list:
            self.cust_uname=input("ENTER CUSTOMER USERNAME : ")
            self.tablename=self.cust_uname
            if self.cust_uname in self.cust_list:
                confirm_del=input("ARE YOU SURE YOU WANT TO DELETE ? \nYES (Y) OR NO (N) ")
                confirm_del=confirm_del.lower()
                if confirm_del=='y':
                    close_acc_query=f'delete from customer_info where c_id={self.cust_id}'
                    del_table_query=f'drop table {self.tablename}'
                    cur.execute(close_acc_query)
                    cur.execute(del_table_query)
                    db.commit()
                    print(f"USERNAME : {self.cust_uname} WITH CUSTOMER ID : {self.cust_id}  ACCOUNT SUCCESSFULLY DELETED ")
                elif confirm_del=='n':
                    self.admin_options()
                else:
                    print("INVALID")
                    self.close_cust_acc()
            else:
                print("WRONG USERNAME")
                self.close_cust_acc()
        else:
            print("CUSTOMER ID NOT FOUND")
            self.close_cust_acc()

    def update_cust_details(self):
        print('''
        -----------------------------
        UPDATE CUSTOMER DETAILS
        -----------------------------
        ''')

        self.c_id=input("ENTER CUSTOMER ID : ")
        if self.c_id.isdigit():
            self.c_id=int(self.c_id)
            if self.c_id in self.c_ids_list:
                self.update_details()
            else:
                print("ID NOT FOUND")
        else:
            print("INVALID CUSTOMER ID")

    def update_details(self):
        print('''
        1.FIRST NAME
        2.MIDDLE NAME
        3.LAST NAME
        4.PHONE NO.
        5.USERNAME
        6.EXIT
        ''')
        opt1=int(input("SELECT A OPTION : "))
        if opt1==1:
            self.update_cust_fname()
        elif opt1==2:
            self.update_cust_mname()
        elif opt1==3:
            self.update_cust_lname()
        elif opt1==4:
            self.update_cust_phoneno()
        elif opt1==5:
            self.update_cust_username()
        elif opt1==6:
            self.exit_adminoptions_()
        else:
            print("INVALID OPTION")

    def update_cust_username(self):
        self.all_customers='select username from customer_info'
        cur.execute(self.all_customers)
        self.records=cur.fetchall()
        for i in self.records:
            self.cust_list.append(i[0])
        old_username=input("ENTER OLD USERNAME : ")
        if old_username in self.cust_list:
            new_username=input("ENTER NEW USERNAME : ")
            new_username=new_username.lower()
            uname_query=f'update customer_info set username="{new_username}" where c_id={self.c_id}'
            change_tablename_query=f'rename table {old_username} to {new_username}'
            if new_username in self.cust_list:
                print("USERNAME ALREADY EXISTS \n TRY NEW USERNAME ")
                self.update_cust_username()
            else:
                if (len(new_username)>=4 and len(new_username)<=10) and str(new_username).isalpha():
                    cur.execute(change_tablename_query)
                    cur.execute(uname_query)
                    db.commit()
                    print(f"USERNAME FOR CUSTOMER ID : {self.c_id} UPDATED SUCCESSFULLY")
                else:
                    print("PLEASE CHECK AGAIN USERNAME MUST CONTAIN 4-10 ALPHABETS IN SMALL CAPS \nNO DIGITS OR SPECIAL CHARACTERS E.G.- @,!,#,$ etc")
                    self.update_cust_username()
        else:
            print("USERNAME NOT FOUND CHECK AGAIN")
            self.update_cust_username()


    def update_cust_phoneno(self):
        new_phoneno=input("ENTER PHONE NO. : ")
        phone_query=f'update customer_info set phoneno="{new_phoneno}" where c_id={self.c_id}'
        if len(new_phoneno)==10 and str(new_phoneno).isdigit():
            cur.execute(phone_query)
            db.commit()
            print(F"PHONE NO. FOR CUSTOMER ID : {self.c_id} UPDATED SUCCESSFULLY ")
        else:
            print("PLEASE CHECK PHONE NO. AGAIN  MUST CONTAIN 10 DIGITS")
            self.update_cust_phoneno()
    
    def update_cust_fname(self):
        new_fname=input("ENTER NEW FIRST NAME : ")
        fname_query=f'update customer_info set fname="{new_fname} where c_id={self.c_id}'
        cur.execute(fname_query)
        db.commit()
        print(f"FIRST NAME FOR CUSTOMER ID : {self.c_id} UPDATED SUCCESSFULLY ")

    def update_cust_mname(self):
        new_mname=input("ENTER NEW MIDDLE NAME : ")
        mname_query=f'update customer_info set mname="{new_mname} where c_id={self.c_id}'
        cur.execute(mname_query)
        db.commit()
        print(f"MIDDLE NAME FOR CUSTOMER ID : {self.c_id} UPDATED SUCCESSFULLY ")

    def update_cust_lname(self):
        new_lname=input("ENTER NEW LAST NAME : ")
        lname_query=f'update customer_info set lname="{new_lname} where c_id={self.c_id}'
        cur.execute(lname_query)
        db.commit()
        print(f"LAST NAME FOR CUSTOMER ID : {self.c_id} UPDATED SUCCESSFULLY ")

    def admin_exit_(self):
        print('''
        ----------------------------
                    BYE
        ----------------------------
        ''')
        self.process()

    def exit_adminoptions_(self):
        self.admin_options()

    def process(self):
        while(True):
            self.welcome_user()
            self.main_menu()
            if self.op==1:
                self.create_new_acc()
            elif self.op==2:
                    self.login()
            elif self.op==3:
                self.admin_login()
            else:
                print("INVALID CHOICE")
                break

if __name__=='__main__':
    hdfc=BANK("HDFC")
    hdfc.process()
            
