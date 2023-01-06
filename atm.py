import random
from tkinter import *
import tkinter as tk
import sqlite3
from datetime import date
import time
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk

active_account=0

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {'Account':tk.IntVar()}

        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MenuPage, WithdrawPage, DepositPage,TransferPage,RegistrationPage,UserDetailsPage,AccountStatementPage,ChangePinPage,ReportsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller

        self.controller.title('ATM SIMULATOR')
        self.controller.state('zoomed')
    #creating heading label
        heading_label = tk.Label(self,
                                                     text='ATM SIMULATOR',
                                                     font=('orbitron',45,'bold'),
                                                     foreground='#ffffff',
                                                     background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self,height=4,bg='#3d3d5c')
        space_label.pack()

      ## GETTING USER ACCOUNT NUMBER
        account_label = tk.Label(self,
                                  text='Enter account number',
                                  font=('orbitron', 13),
                                  bg='#3d3d5c',
                                  fg='white')
        account_label.pack(pady=6)

        my_account = tk.IntVar()
        account_entry_box = tk.Entry(self,
                                      textvariable=my_account,
                                      font=('orbitron', 12),
                                      width=22)

        account_entry_box.focus_set()
        account_entry_box.pack(ipady=7)

        def handle_focus_in(_):
            account_entry_box.configure(fg='black')

        account_entry_box.bind('<FocusIn>', handle_focus_in)




        def check_account():

            ##SQL TO GET USER ACCOUNT AND USER PIN FROM DATABASE

            # CREATING A COONECTION OBJECT
            conn = sqlite3.connect("database/atm.db")

            # CREATING A CURSOR OBJECT
            c = conn.cursor()
            # SQL QUERY

            #USER ACCOUNT VERIFICATION FROM DATABASE
            get_ac_no_query = '''select ac_no from user_info'''
            ac_no_list = c.execute(get_ac_no_query).fetchall()

            ac_match = "false"

            for each_ac_no in ac_no_list:
                if each_ac_no[0] == my_account.get():
                    ac_match= 'true'

                    break

            #USER PIN VERIFICATION FROM DATABASE

            ac_pin_list = c.execute(f"select pswd from user_info where ac_no ={my_account.get()}").fetchall()
            pin_match = "false"
            for each_pin in ac_pin_list:
                if each_pin[0] == my_password.get():

                    pin_match= 'true'
                    break

            conn.commit()
            c.close()
            ##ACCOUNT NUMBER AND PIN VALIDATION

            if(ac_match=="false"):
                messagebox.showinfo("Invalid Account","Account Number Not Found")

            if(pin_match=="false"):
                messagebox.showinfo("Invalid Pin","Invalid PIN")

            #when both details are correct
            if((ac_match=="true") and (pin_match=="true")):
               global active_account
               active_account =my_account.get()
               controller.shared_data['Account'].set(active_account)
               controller.show_frame('MenuPage')





      ## GETTING USER PIN
        password_label = tk.Label(self,
                                                      text='Enter your password',
                                                      font=('orbitron',13),
                                                      bg='#3d3d5c',
                                                      fg='white')
        password_label.pack(pady=10)

        my_password = tk.IntVar()
        password_entry_box = tk.Entry(self,
                                                              textvariable=my_password,
                                                              font=('orbitron',12),
                                                              width=22)
        password_entry_box.focus_set()
        password_entry_box.pack(ipady=7)

        def handle_focus_in(_):
            password_entry_box.configure(fg='black',show='*')
            
        password_entry_box.bind('<FocusIn>',handle_focus_in)

         #enter button

        enter_button = tk.Button(self,
                                                     text='Enter',
                                                     command=check_account,
                                                     relief='raised',
                                                     borderwidth = 2,
                                                     width=20,
                                                     height=3)
        enter_button.pack(pady=15)

        #new account register button

        def open_account():
            controller.show_frame('RegistrationPage')

        ac_open_button = tk.Button(self,
                                                     text='Open an Account',
                                                     command=open_account,
                                                     relief='raised',
                                                     borderwidth = 2,
                                                     width=40,
                                                     height=3)
        ac_open_button.pack(pady=15)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()


class RegistrationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        self.controller.title('ATM SIMULATOR')
        self.controller.state('zoomed')



        #REGISTRATION FORM ELEMENTS

        #  Form label
        heading = Label(self, text="New Account Registration",
                                                     font=('orbitron',45,'bold'),
                                                     foreground='#ffffff',
                                                     background='#3d3d5c')

        #  Name label
        name = Label(self, text="Name",  font=('orbitron',13),fg='white', bg='#3d3d5c',anchor='n')

        #Father Name label
        fathername= Label(self, text="Father Name",font=('orbitron',13),fg='white', bg='#3d3d5c',anchor='n')

        # Age label
        gender = Label(self, text="Gender", font=('orbitron',13),fg='white', bg='#3d3d5c',anchor='n')

        # gender label

        age = Label(self, text="Age", font=('orbitron',13),fg='white', bg='#3d3d5c',anchor='n')

        #  phone label
        phone_no = Label(self, text="Phone No.", font=('orbitron',13),fg='white', bg='#3d3d5c',anchor='n')

        #  address label
        address = Label(self, text="Address",font=('orbitron',13),fg='white', bg='#3d3d5c',anchor='n')

        # Password label
        pin = Label(self, text="PIN", font=('orbitron',13),fg='white', bg='#3d3d5c',anchor='n')

        # place method  for placing
        # the widgets at respective positions

        heading.place(x=400,y=50)
        name.place(x=500,y=150)
        fathername.place(x=500,y=200)
        gender.place(x=500,y=250)
        age.place(x=500,y=300)
        phone_no.place(x=500,y=350)
        address.place(x=500,y=400)
        pin.place(x=500,y=450)

        #  text entry boxes to collect user information

        name_field = Entry(self)
        fathername_field = Entry(self)


        # Gender Option list

        def callback(selection):
            global user_gender
            user_gender = str(selection)


        value_inside = tk.StringVar(self)

        gender_field = tk.OptionMenu(self, value_inside, "Male", "Female", "Other",command=callback)

        age_field = Entry(self)
        phone_no_field = Entry(self)
        address_field = Entry(self)
        pin_field = Entry(self)


        name_field.place(x=600,y=150)
        fathername_field.place(x=600,y=200)
        gender_field.place(x=600,y=250)
        age_field.place(x=600,y=300)
        phone_no_field.place(x=600,y=350)
        address_field.place(x=600,y=400)
        pin_field.place(x=600,y=450)

        #Buttons

        #REGISTER BUTTON
        def register_success():
            ac_no = random.randint(100000 , 999999)

            username=name_field.get()

            userfathername =fathername_field.get()

            userage = int(age_field.get())

            userphone=int(phone_no_field.get())

            useraddress = address_field.get()

            userpin =int(pin_field.get())

            balance=1000

            withdraw=0
            trans_type ="Deposit"
            today = date.today()

            # dd/mm/YY

            today_date = today.strftime("%d/%m/%Y")

            usergender = user_gender


            # CREATING A COONECTION OBJECT
            conn = sqlite3.connect("database/atm.db")

            # CREATING A CURSOR OBJECT
            c = conn.cursor()
            # SQL QUERY


            c.execute("INSERT INTO user_info(ac_no, name, fathername, age, phone, address, pswd, balance, gender) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                                      (ac_no, username,userfathername,userage,userphone,useraddress,userpin,balance,usergender))
            c.execute("insert into transactions(ac_no,deposit,withdraw,date,type,balance)values(?,?,?,?,?,?)",
                      (ac_no, balance, withdraw, today_date, trans_type, balance))

            conn.commit()
            c.close()

            info = "Dear "+name_field.get()+" your Account has been Created Successfully.Your Account Number is :"+str(ac_no)
            messagebox.showinfo("Registration", info)



        register_button = tk.Button(self,text='Register',relief='raised',
                                                     borderwidth = 2,
                                                    command=register_success,
                                                     width=10,
                                                     height=2)

        register_button.place(x=500,y= 500)

        #CANCEL BUTTON
        def exit():
            controller.show_frame('StartPage')

        register_button = tk.Button(self, text='Cancel',relief='raised',
                                                    command=exit,
                                                     borderwidth = 2,
                                                     width=10,
                                                     height=2)

        register_button.place(x=700,y= 500)


        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                                     text='ATM SIMULATOR',
                                                     font=('orbitron',45,'bold'),
                                                     foreground='#ffffff',
                                                     background='#3d3d5c')
        heading_label.pack(pady=25)

        main_menu_label = tk.Label(self,
                                                           text='Main Menu',
                                                           font=('orbitron',13),
                                                           fg='white',
                                                           bg='#3d3d5c')
        main_menu_label.pack()

        selection_label = tk.Label(self,
                                                           text='Please make a selection',
                                                           font=('orbitron',13),
                                                           fg='white',
                                                           bg='#3d3d5c',
                                                           anchor='w')
        selection_label.pack(fill='x')

        button_frame = tk.Frame(self,bg='#33334d')
        button_frame.pack(fill='both',expand=True)


        def withdraw():
            controller.show_frame('WithdrawPage')
            
        withdraw_button = tk.Button(button_frame,
                                                            text='Withdraw',
                                                            command=withdraw,
                                                            relief='raised',
                                                            borderwidth=3,
                                                            width=50,
                                                            height=5)
        withdraw_button.grid(row=0,column=0,pady=5)

        def deposit():
            controller.show_frame('DepositPage')
            
        deposit_button = tk.Button(button_frame,
                                                            text='Deposit',
                                                            command=deposit,
                                                            relief='raised',
                                                            borderwidth=3,
                                                            width=50,
                                                            height=5)
        deposit_button.grid(row=1,column=0,pady=5)

        def transfer():
            controller.show_frame('TransferPage')
            
        balance_button = tk.Button(button_frame,
                                                            text='Transfer',
                                                            command=transfer,
                                                            relief='raised',
                                                            borderwidth=3,
                                                            width=50,
                                                            height=5)
        balance_button.grid(row=2,column=0,pady=5)

        def accountstatement():
            controller.show_frame('AccountStatementPage')

        accountstatement_button = tk.Button(button_frame,
                                text='Account Statement',
                                command=accountstatement,
                                relief='raised',
                                borderwidth=3,
                                width=50,
                                height=5)
        accountstatement_button.grid(row=3, column=0, pady=5)

        def changepin():
            controller.show_frame('ChangePinPage')

        exit_button = tk.Button(button_frame,
                                text='Change PIN',
                                command=changepin,
                                relief='raised',
                                borderwidth=3,
                                width=50,
                                height=5)
        exit_button.grid(row=0, column=1, padx=300, pady=5, sticky=E)

        def useraccountdetails():
            controller.show_frame('UserDetailsPage')

        exit_button = tk.Button(button_frame,
                                text='User Account Details',
                                command=useraccountdetails,
                                relief='raised',
                                borderwidth=3,
                                width=50,
                                height=5)
        exit_button.grid(row=1, column=1, padx=300, pady=5, sticky=E)

        def depositwithdrawreports():
            controller.show_frame('ReportsPage')

        exit_button = tk.Button(button_frame,
                                text='Deposit/Withdraw Reports',
                                command=depositwithdrawreports,
                                relief='raised',
                                borderwidth=3,
                                width=50,
                                height=5)
        exit_button.grid(row=2, column=1, padx=300, pady=5, sticky=E)

        def exit():
            controller.show_frame('StartPage')
            
        exit_button = tk.Button(button_frame,
                                                            text='Exit',
                                                            command=exit,
                                                            relief='raised',
                                                            borderwidth=3,
                                                            width=50,
                                                            height=5)
        exit_button.grid(row=3,column=1,padx=300,pady=5,sticky=E)


        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()


class WithdrawPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='ATM SIMULATOR',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#3d3d5c')
        space_label.pack()

        enter_amount_label = tk.Label(self,
                                      text='Enter Withdrawl Amount',
                                      font=('orbitron', 13),
                                      bg='#3d3d5c',
                                      fg='white')
        enter_amount_label.pack(pady=10)

        cash = tk.IntVar()
        deposit_entry = tk.Entry(self,
                                 textvariable=cash,
                                 font=('orbitron', 12),
                                 width=22)
        deposit_entry.pack(ipady=7)

        def withdraw_cash():
            global active_account
            account = controller.shared_data['Account'].get()
            amount = int(deposit_entry.get())
            deposit= 0
            trans_type = "Withdraw"

            today = date.today()

            # dd/mm/YY

            today_date = today.strftime("%d/%m/%Y")

            # CREATING A CONNECTION OBJECT
            conn = sqlite3.connect("database/atm.db")

            # CREATING A CURSOR OBJECT
            c = conn.cursor()
            # SQL QUERy
            balance_tup = c.execute(f"select balance from transactions where ac_no ={account}").fetchall()
            balance = balance_tup[-1]

            #validating whether user enter amount less than available balance

            if(amount > int(balance[0])):
                messagebox.showinfo("Limit Exceeded",f"Withdraw Amount is greater than Available Balance. Your Available Balance is {balance}")
            else:
                updated_balace = balance[0] - amount

                c.execute("insert into transactions(ac_no,deposit,withdraw,date,type,balance)values(?,?,?,?,?,?)",
                          (account, deposit, amount, today_date, trans_type, updated_balace))

                conn.commit()
                c.close()

                transaction_msg = "Amount of " + str(
                    amount) + " has been successfully Withdrawn from your Account.Your Updated Account Balance is :" + str(updated_balace)
                messagebox.showinfo("Transaction Status", transaction_msg)

        enter_button = tk.Button(self,
                                 text='Withdraw',
                                 command=withdraw_cash,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10)

        def menupage():
            controller.show_frame("MenuPage")

        back_button = tk.Button(self,
                                 text='Main Menu',
                                 command=menupage,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        back_button.pack(pady=15)

        two_tone_label = tk.Label(self, bg='#33334d')
        two_tone_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()
   

class DepositPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                                     text='ATM SIMULATOR',
                                                     font=('orbitron',45,'bold'),
                                                     foreground='#ffffff',
                                                     background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self,height=4,bg='#3d3d5c')
        space_label.pack()

        enter_amount_label = tk.Label(self,
                                                      text='Enter amount',
                                                      font=('orbitron',13),
                                                      bg='#3d3d5c',
                                                      fg='white')
        enter_amount_label.pack(pady=10)

        cash = tk.IntVar()
        deposit_entry = tk.Entry(self,
                                                  textvariable=cash,
                                                  font=('orbitron',12),
                                                  width=22)
        deposit_entry.pack(ipady=7)

        def deposit_cash():
            global active_account
            account = controller.shared_data['Account'].get()
            amount = int(deposit_entry.get())
            withdraw=0
            trans_type="Deposit"

            today = date.today()

            # dd/mm/YY

            today_date = today.strftime("%d/%m/%Y")

            # CREATING A COONECTION OBJECT
            conn = sqlite3.connect("database/atm.db")

            # CREATING A CURSOR OBJECT
            c = conn.cursor()
            # SQL QUERy
            balance_tup = c.execute(f"select balance from transactions where ac_no ={account}").fetchall()
            balance = balance_tup[-1]

            updated_balace = balance[0]+amount

            c.execute("insert into transactions(ac_no,deposit,withdraw,date,type,balance)values(?,?,?,?,?,?)",(account,amount,withdraw,today_date,trans_type,updated_balace))

            conn.commit()
            c.close()

            transaction_msg = "Amount of "+str(amount) + " has been successfully Deposited to your Account.Your Updated Account Balance is :"+str(updated_balace)
            messagebox.showinfo("Transaction Status",transaction_msg)
            
        enter_button = tk.Button(self,
                                                     text='Enter',
                                                     command=deposit_cash,
                                                     relief='raised',
                                                     borderwidth=3,
                                                     width=40,
                                                     height=3)
        enter_button.pack(pady=10)

        def menupage():
            controller.show_frame("MenuPage")

        back_button = tk.Button(self,
                                 text='Main Menu',
                                 command=menupage,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        back_button.pack(pady=15)

        two_tone_label = tk.Label(self,bg='#33334d')
        two_tone_label.pack(fill='both',expand=True)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()

#####################CLASS FOR TRANSFER PAGE #######################

class TransferPage(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='ATM SIMULATOR',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#3d3d5c')
        space_label.pack()

        enter_account_label = tk.Label(self,
                                      text='Enter Account Number',
                                      font=('orbitron', 13),
                                      bg='#3d3d5c',
                                      fg='white')
        enter_account_label.pack(pady=10)

        account_number = tk.IntVar()
        account_number_entry = tk.Entry(self,
                                 textvariable=account_number,
                                 font=('orbitron', 12),
                                 width=22)
        account_number_entry.pack(ipady=7)

        transfer_amount_label = tk.Label(self,
                                      text='Enter Transfer Amount',
                                      font=('orbitron', 13),
                                      bg='#3d3d5c',
                                      fg='white')
        transfer_amount_label.pack(pady=10)

        cash = tk.IntVar()
        transfer_amount_entry = tk.Entry(self,
                                 textvariable=cash,
                                 font=('orbitron', 12),
                                 width=22)
        transfer_amount_entry.pack(ipady=7)

        def transfer_cash():
            global active_account
            account = controller.shared_data['Account'].get()
            transfer_account= int(account_number_entry.get())


            today = date.today()

            # dd/mm/YY

            today_date = today.strftime("%d/%m/%Y")

            ##SQL TO GET USER ACCOUNT AND USER PIN FROM DATABASE

            # CREATING A COONECTION OBJECT
            conn = sqlite3.connect("database/atm.db")

            # CREATING A CURSOR OBJECT
            c = conn.cursor()
            # SQL QUERY

            # USER ACCOUNT VERIFICATION FROM DATABASE
            get_ac_no_query = '''select ac_no from user_info'''
            ac_no_list = c.execute(get_ac_no_query).fetchall()


            match='false'

            for each_ac_no in ac_no_list:
                if each_ac_no[0] == int(account_number_entry.get()):
                    match='true'




            if(match=='true'):
                active_account_balance = c.execute(f"select balance from transactions where ac_no={account}").fetchall()
                balance = active_account_balance[-1]

                transfer_account_balance = c.execute(
                    f"select balance from user_info where ac_no={account_number_entry.get()}").fetchall()
                transfer_balance = transfer_account_balance[-1]

                if((balance[0] > int(transfer_amount_entry.get()))):
                    c.execute(f"update user_info set balance={balance[0]-int(transfer_amount_entry.get())} where ac_no={account}")
                    c.execute("insert into transactions(ac_no,deposit,withdraw,date,type,balance)values(?,?,?,?,?,?)",(account,0,int(transfer_amount_entry.get()),today_date,"Out-Transfer",balance[0]-int(transfer_amount_entry.get())))
                    c.execute(f"update user_info set balance={transfer_balance[0]+int(transfer_amount_entry.get())} where ac_no={int(account_number_entry.get())}")
                    c.execute("insert into transactions(ac_no,deposit,withdraw,date,type,balance)values(?,?,?,?,?,?)", (int(account_number_entry.get()), int(transfer_amount_entry.get()),0, today_date, "In-Transfer",transfer_balance[0]+int(transfer_amount_entry.get())))

                    message = "Amount of : "+ transfer_amount_entry.get()+ " has been Successfully Transferred to : "+account_number_entry.get()
                    messagebox.showinfo("Transfer SUccessful!",message)
                    conn.commit()
                    c.close()
                else:
                    error_msg ="Insufficient Balance ! Your Account Balance is "+str(balance[0])
                    messagebox.showinfo("Insufficient Balance",error_msg)
            else:
                messagebox.showinfo("Not Found","Account Number Not Found")


        enter_button = tk.Button(self,
                                 text='Transfer',
                                 command=transfer_cash,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10)

        def menupage():
            controller.show_frame("MenuPage")

        back_button = tk.Button(self,
                                text='Main Menu',
                                command=menupage,
                                relief='raised',
                                borderwidth=3,
                                width=40,
                                height=3)
        back_button.pack(pady=15)

        two_tone_label = tk.Label(self, bg='#33334d')
        two_tone_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


class AccountStatementPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                                     text='ATM SIMULATOR',
                                                     font=('orbitron',45,'bold'),
                                                     foreground='#ffffff',
                                                     background='#3d3d5c')
        heading_label.pack(pady=25)

        def getstatement():
            global active_account
            account = controller.shared_data['Account'].get()

            # CREATING A COONECTION OBJECT
            conn = sqlite3.connect("database/atm.db")

            # CREATING A CURSOR OBJECT
            c = conn.cursor()
            # SQL QUERy
            r_set = c.execute(f'SELECT * from transactions where ac_no={account} ')

            my_w = tk.Tk(screenName="Account Statement")

            i = 0  # row value inside the loop
            tk.Label(my_w, width=10, fg='red', text="A/C NUMBER", font=('bold') ,anchor='w').grid(row=0,column=0,padx=2)
            tk.Label(my_w, width=10, fg='red', text="DEPOSITS", anchor='w').grid(row=0, column=1, padx=2)
            tk.Label(my_w, width=10, fg='red', text="WITHDRAWS", anchor='w').grid(row=0, column=2, padx=2)
            tk.Label(my_w, width=10, fg='red', text="DATE", anchor='w').grid(row=0, column=3, padx=2)
            tk.Label(my_w, width=10, fg='red', text="TRANSACTION", anchor='w').grid(row=0, column=4, padx=2)
            tk.Label(my_w, width=10, fg='red', text="BALANCE", anchor='w').grid(row=0, column=5, padx=2)
            for data in r_set:
                for j in range(len(data)):
                    e = tk.Label(my_w, width=10, fg='black', text=data[j], anchor='w')
                    e.grid(row=i+1, column=j, padx=2)
                i = i + 1

            conn.commit()
            c.close()


        enter_button = tk.Button(self,
                                 text='Get Statement',
                                 command=getstatement,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=50)

        def menupage():
            controller.show_frame("MenuPage")

        back_button = tk.Button(self,
                                text='Main Menu',
                                command=menupage,
                                relief='raised',
                                borderwidth=3,
                                width=40,
                                height=3)
        back_button.pack(pady=55)


class ChangePinPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='ATM SIMULATOR',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#3d3d5c')
        space_label.pack()

        pin_label = tk.Label(self,
                                      text='Enter New PIN',
                                      font=('orbitron', 13),
                                      bg='#3d3d5c',
                                      fg='white')
        pin_label.pack(pady=10)

        pin = tk.IntVar()
        pin_entry = tk.Entry(self,
                                 textvariable=pin,
                                 font=('orbitron', 12),
                                 width=22)
        pin_entry.pack(ipady=7)

        def change_pin():
            global active_account
            account = controller.shared_data['Account'].get()
            new_pin= int(pin_entry.get())

            # CREATING A COONECTION OBJECT
            conn = sqlite3.connect("database/atm.db")

            # CREATING A CURSOR OBJECT
            c = conn.cursor()
            # SQL QUERy
            c.execute(f"update user_info set pswd ={new_pin} where ac_no ={account}")

            conn.commit()
            c.close()

            change_msg ="Your PIN has been Changed Successfully !"
            messagebox.showinfo("Transaction Status", change_msg)

        enter_button = tk.Button(self,
                                 text='Change PIN',
                                 command=change_pin,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10)

        def menupage():
            controller.show_frame("MenuPage")

        back_button = tk.Button(self,
                                text='Main Menu',
                                command=menupage,
                                relief='raised',
                                borderwidth=3,
                                width=40,
                                height=3)
        back_button.pack(pady=15)

        two_tone_label = tk.Label(self, bg='#33334d')
        two_tone_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


   ##USER DETAILS PAGE

class UserDetailsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        self.controller.title('ATM SIMULATOR')
        self.controller.state('zoomed')

        # REGISTRATION FORM ELEMENTS

        #  Form label

        name_field = Label(self, text="", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')
        name_field.place(x=600, y=150)

        heading = Label(self, text="User Details",
                        font=('orbitron', 45, 'bold'),
                        foreground='#ffffff',
                        background='#3d3d5c')

        #  Name label
        name = Label(self, text="Name", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')

        # Father Name label
        fathername = Label(self, text="Father Name", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')

        # Age label
        gender = Label(self, text="Gender", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')

        # gender label

        age = Label(self, text="Age", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')

        #  phone label
        phone_no = Label(self, text="Phone No.", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')

        #  address label
        address = Label(self, text="Address", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')




        heading.place(x=400, y=50)
        name.place(x=500, y=150)
        fathername.place(x=500, y=200)
        gender.place(x=500, y=250)
        age.place(x=500, y=300)
        phone_no.place(x=500, y=350)
        address.place(x=500, y=400)


        ###################info display labels################

        def getDetails(data):
            if(data=="run"):
                global active_account

                account = controller.shared_data['Account'].get()

                # CREATING A COONECTION OBJECT
                conn = sqlite3.connect("database/atm.db")

                # CREATING A CURSOR OBJECT
                c = conn.cursor()
                # SQL QUERy
                check = c.execute(f"select * from user_info where ac_no={account}").fetchone()
                print(check)

                conn.commit()
                c.close()

                # Name label



                name_field = Label(self)
                name_field.config(text=check[1]+"                           ", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')

                # Father Name label
                fathername_field = Label(self)
                fathername_field.config(text=check[2]+"                          ", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')


                # Gender label
                gender_field = Label(self)
                gender_field.config(text=check[8]+"               ", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')

                # age label

                age_field = Label(self)
                age_field.config(text=str(check[3]), font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')

                #  phone label
                phone_no_field = Label(self)
                phone_no_field.config(text=str(check[4]), font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')

                #  address label
                address_field = Label(self)
                address_field.config(text=check[5]+"                               ", font=('orbitron', 13), fg='white', bg='#3d3d5c', anchor='n')



                name_field.place(x=600, y=150)
                fathername_field.place(x=600, y=200)
                gender_field.place(x=600, y=250)
                age_field.place(x=600, y=300)
                phone_no_field.place(x=600, y=350)
                address_field.place(x=600, y=400)





        #############getDetail Function calling itself#########


        # Buttons

        # CANCEL BUTTON
        def exit():

            controller.show_frame('MenuPage')


        back_button = tk.Button(self, text='Go Back', relief='raised',
                                    command=exit,
                                    borderwidth=2,
                                    width=10,
                                    height=2)

        back_button.place(x=700, y=500)

        #DISPLAY INFO BUTTON

        display_button = tk.Button(self, text='Get Info', relief='raised',
                                    command=lambda:getDetails("run"),
                                    borderwidth=2,
                                    width=10,
                                    height=2)

        display_button.place(x=500, y=500)



        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')



        tick()


#deposit/withdraw transaction ratio reports using graphs

class ReportsPage(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='ATM SIMULATOR',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#3d3d5c')
        space_label.pack()


        def plot_all_trans_type():
            global active_account
            account = controller.shared_data['Account'].get()

            ##SQL TO GET USER ACCOUNT AND USER PIN FROM DATABASE

            # CREATING A COONECTION OBJECT
            conn = sqlite3.connect("database/atm.db")

            # CREATING A CURSOR OBJECT
            c = conn.cursor()

            # getting SUM from all transaction types from database
            #sum of all deposits by self
            deposit_sum = list(c.execute(f"select sum(deposit) from transactions where ac_no={account} and  type='Deposit'").fetchone())
            withdraw_sum = list(c.execute(f"select sum(withdraw) from transactions where ac_no={account} and  type='Withdraw'").fetchone())
            in_transfer_sum = list(c.execute(f"select sum(deposit) from transactions where ac_no={account} and  type='In-Transfer'").fetchone())
            out_transfer_sum = list(c.execute(f"select sum(withdraw) from transactions where ac_no={account} and  type='Out-Transfer'").fetchone())

            #checking whether one transactiion of each type is done for generating reports
            if ((str(withdraw_sum[0]))=="None" or (str(in_transfer_sum[0]))=="None" or (str(out_transfer_sum[0]))=="None") :
                messagebox.showinfo("Not Enough Data","New Account,Not Enough Data to Generate Reports")

            else:

                #merging all type of transaction sum values into one Tuple
                transaction_type_tuple =["Deposit", "Withdraw", "In-Transfers", "Out-Transfers"]
                transactions_sum_tuple = np.array((deposit_sum + withdraw_sum + in_transfer_sum + out_transfer_sum))
                plt.pie(transactions_sum_tuple,labels=transaction_type_tuple,autopct='%1.1f%%',startangle=90)
                plt.legend(title="Transaction Type")
                plt.show()


        #deposit/withdraw bar graph report

        def plot_all_deposit_withdraw():
            global active_account
            account = controller.shared_data['Account'].get()

            ##SQL TO GET USER ACCOUNT AND USER PIN FROM DATABASE

            # CREATING A COONECTION OBJECT
            conn = sqlite3.connect("database/atm.db")

            # CREATING A CURSOR OBJECT
            c = conn.cursor()

            # getting SUM from all transaction types from database
            #sum of all deposits by self
            deposit_sum = list(c.execute(f"select sum(deposit) from transactions where ac_no={account} and  type='Deposit'").fetchone())
            withdraw_sum = list(c.execute(f"select sum(withdraw) from transactions where ac_no={account} and  type='Withdraw'").fetchone())
            in_transfer_sum = list(c.execute(f"select sum(deposit) from transactions where ac_no={account} and  type='In-Transfer'").fetchone())
            out_transfer_sum = list(c.execute(f"select sum(withdraw) from transactions where ac_no={account} and  type='Out-Transfer'").fetchone())

            #checking whether one transactiion of each type is done for generating reports
            if ((str(withdraw_sum[0]))=="None" or (str(in_transfer_sum[0]))=="None" or (str(out_transfer_sum[0]))=="None") :
                messagebox.showinfo("Not Enough Data","New Account,Not Enough Data to Generate Reports")

            else:

                #merging all type of transaction sum values into one Tuple
                transaction_type_tuple =["Deposit", "Withdraw", "In-Transfers", "Out-Transfers"]
                transactions_sum_tuple = np.array((deposit_sum + withdraw_sum + in_transfer_sum + out_transfer_sum))
                plt.bar(transaction_type_tuple,transactions_sum_tuple,color = "#4CAF50")
                plt.show()



        all_trans_type_button = tk.Button(self,
                                 text='Transactions Ratio for Current Month',
                                 command=plot_all_trans_type,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        all_trans_type_button.pack(pady=5)

        deposit_withdraw_type_button = tk.Button(self,
                                 text='Deposit/Withdraw Reports for Current Month',
                                 command=plot_all_deposit_withdraw,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        deposit_withdraw_type_button.pack(pady=8)

        def menupage():
            controller.show_frame("MenuPage")

        back_button = tk.Button(self,
                                text='Main Menu',
                                command=menupage,
                                relief='raised',
                                borderwidth=3,
                                width=40,
                                height=3)
        back_button.pack(pady=12)

        two_tone_label = tk.Label(self, bg='#33334d')
        two_tone_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()





if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
