import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import sqlite3
from waterBill import check_bill
import bcrypt
import time
from secrets import compare_digest
import datetime

current_date = datetime.datetime.today()
def show_message(title, message):
   messagebox.showerror(title, message)

def Home(root, frame1, frame2):
    root.configure(bg='steel blue')
    frame1.config(bg="steel blue")
    frame2.config(bg="steel blue")
    for frame in root.winfo_children():
       for widget in frame.winfo_children():
           widget.destroy()

    Button(frame2, text="Home",bg="light steel blue",width=6,command = lambda: Home(root, frame1, frame2)).grid(row=0,column=0)
    Label(frame2, text="                                                                         ",bg="steel blue").grid(row = 0,column = 1)
    Label(frame2, text="                                                                         ",bg="steel blue").grid(row = 0,column = 2)
    Label(frame2, text="         ",bg="steel blue").grid(row = 1,column = 1)
    frame2.pack()

    root.title("WATERBILLING SYSTEM")

    Label(frame1, text="Home", bg="steel blue",font=('Helvetica', 25, 'bold')).grid(row = 0, column = 1, rowspan=1)
    Label(frame1, text="        ",bg="steel blue").grid(row = 1,column = 0)

    admin = Button(frame1, text="Admin Login",bg="light steel blue", width=15, height=2, command = lambda: AdmLogin(root, frame1))
    user = Button(frame1, text="User Login",bg="light steel blue", width=15, height=2, command = lambda: userLogin(root, frame1))
    reg = Button(frame1, text="Register",bg="light steel blue", width=15, height=2, command = lambda: register(root,frame1))

    Label(frame1, text="",bg="steel blue").grid(row = 2,column = 0)
    Label(frame1, text="",bg="steel blue").grid(row = 4,column = 0)
    Label(frame1, text="",bg="steel blue").grid(row = 6,column = 0)
    admin.grid(row = 3, column = 1, columnspan = 2)
    user.grid(row = 5, column = 1, columnspan = 2)
    reg.grid(row = 7, column = 1, columnspan = 2)

    frame1.pack()
    root.mainloop()

def AdmLogin(root,frame1):

    root.title("Admin Login")
    for widget in frame1.winfo_children():
        widget.destroy()

    Label(frame1, text="Admin Login",bg="steel blue", font=('Helvetica', 18, 'bold'),fg="yellow").grid(row = 0, column = 2, rowspan=1)
    Label(frame1, text="        ",bg="steel blue").grid(row = 1,column = 0)
    Label(frame1, text="Admin ID:      ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 2,column = 0)
    Label(frame1, text="Password:       ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 3,column = 0)

    admin_ID = tk.StringVar()
    password = tk.StringVar()

    e1 = Entry(frame1, textvariable = admin_ID)
    e1.grid(row = 2,column = 2)
    e2 = Entry(frame1, textvariable = password, show = '*')
    e2.grid(row = 3,column = 2)

    sub = Button(frame1, text="Login", bg="light steel blue",width=10, command = lambda: adm_auth(root, frame1, admin_ID.get(), password.get().encode()))
    Label(frame1, text="         ",bg="steel blue").grid(row = 4,column = 0)
    sub.grid(row = 5, column = 1, columnspan = 2)

    frame1.pack()
    root.mainloop()

def log_admin(root,frame1,uid, unm):
      logs = f"{current_date} user with {uid} username {unm} logged in successfully"
      with open('waterbill.log', 'a') as l:
         l.write(f"\n{logs}")
      root.title("Administrator")
      for widget in frame1.winfo_children():
         widget.destroy()
      Label(frame1, text=f"Welcome {unm}", bg="black",fg="white").grid(row=0, column=5, rowspan=1)
      
      update_button = Button(frame1,text='PRINT USERS', bg="cyan", width=20, height=3, command = lambda: p_users(root,frame1,text_box))
      update_button.grid(row = 5, column = 0, columnspan = 2)

      update_button = Button(frame1,text='UPDATE CHARGES', bg="green", fg="white", width=20, height=3, command = lambda: charges_update(root,frame1,uid,unm))
      update_button.grid(row = 5, column = 3, columnspan = 2)
      
      update_button = Button(frame1,text='LOGOUT', bg="orange", width=20, height=3, command = lambda: Admlogout(root,frame1))
      update_button.grid(row = 6, column = 0, columnspan = 2)
      
      p_button = Button(frame1,text='PRINT CHAGES', bg="yellow", width=20, height=3, command = lambda: pCharges(root,frame1,text_box))
      p_button.grid(row=6,column=2,columnspan=2)
      pr_button = Button(frame1,text='LOGS', bg="blue", fg="white", width=20, height=3, command = lambda: readLog())
      pr_button.grid(row=7,column=1,columnspan=2)
      Button(frame1, text="QUIT PROGRAM",bg="red",width=20, height=3,command = lambda: prog_quit(root,frame1,uid,unm)).grid(row=7,column=2, columnspan=2)
      text_box = Text(frame1,width=70,bg="black",fg="white",relief="flat")
      t_box = Text(frame1,width=70,height=1,bg="green",fg="white",relief="flat")
      text_box.edit_separator()
      text_box.grid(row=5,column=10,rowspan=7)
      t_box.grid(row=4,column=10)
      
      t_box.insert(END,f"{current_date}          TERMINAL                              ")
      t_box.config(state='disabled')
      sb = Scrollbar(frame1)
      def clearText():
         a = text_box.index('end-1c').split('.')[0]
         c = text_box.index('end-1c')
         b = (str(int(a)-1)+'.0')
         t = text_box.get("1.0",END)
         text_box.delete(1.0,c)
      def Admlogout(root,frame1):
         log = f"{current_date} user with {uid} username {unm} logged out successfully"
         with open('waterbill.log', 'a') as l:
            l.write(f"\n{log}")
         def x():
            messagebox.showerror('Logout', 'Are you sure of logging out?')
            AdmLogin(root,frame1)
         x()

      def printer(root,frame1,a):
         aa = text_box.index('end-1c').split('.')[0]
         text_box.insert(END,f"\n{a}")
      Label(frame1, text="Safe payment, safe transactions",bg="red",fg="yellow").grid(row=15, column=8, columnspan=2)
      update_button = Button(frame1,text='CLEAR', bg="green", fg="white", width=20, height=2, command = lambda: clearText())
      update_button.grid(row = 15, column = 10, columnspan = 2)
      
      def readLog():
         with open('waterbill.log','r') as l:
            reader = l.read()
            text_box.insert(END,f"\n{reader}")
      

def userLogin(root, frame1):
    root.title("User Login")
    for widget in frame1.winfo_children():
        widget.destroy()

    Label(frame1, text="User Login",bg="steel blue", font=('Helvetica', 18, 'bold'),fg="yellow").grid(row = 0, column = 2, rowspan=1)
    Label(frame1, text="         ",bg="steel blue").grid(row = 1,column = 0)
    Label(frame1, text="User ID:      ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 2,column = 0)
    Label(frame1, text="Password:       ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 3,column = 0)

    user_ID = tk.StringVar()
    password = tk.StringVar()

    e1 = Entry(frame1, textvariable = user_ID)
    e1.grid(row = 2,column = 2)
    e2 = Entry(frame1, textvariable = password, show = '*')
    e2.grid(row = 3,column = 2)

    sub = Button(frame1, text="Login", bg="light steel blue",width=10, command = lambda: auth(root,frame1,user_ID.get(), password.get().encode()))
    Label(frame1, text="       ",bg="steel blue").grid(row = 4,column = 0)
    sub.grid(row = 5, column = 1, columnspan = 2)

    frame1.pack()
    root.mainloop()

def log_user(root, frame1,uid,uname):
      root.title("User page")
      for widget in frame1.winfo_children():
        widget.destroy()
      Label(frame1, text=f"Welcome {uname}", bg="green",fg="white").grid(row=0, column=5, rowspan=1)
      
      update_button = Button(frame1,text='CHECK BILL', bg="orange", width=20, height=3, command = lambda: check_bill(root,frame1,uid,text_box,uname))
      update_button.grid(row = 5, column = 0, columnspan = 2)

      update_button = Button(frame1,text='PAY BILLS', bg="orange", width=20, height=3, command = lambda: pay_bills(root,frame1,uid,uname))
      update_button.grid(row = 5, column = 3, columnspan = 2)
      
      update_button = Button(frame1,text='LOGOUT', bg="orange", width=20, height=3, command = lambda: logout(root,frame1))
      update_button.grid(row = 6, column = 0, columnspan = 2)

      update_button = Button(frame1,text='DELETE ACCOUNT', bg="orange", width=20, height=3, command = lambda: del_user(root,frame1,uid,uname))
      update_button.grid(row = 6, column = 3, columnspan = 2)
      
      update_button = Button(frame1,text='MY DETAILS', bg="orange", width=20, height=3, command = lambda: pr_details(uid,uname))
      update_button.grid(row = 7, column = 0, columnspan = 2)
      
      text_box = Text(frame1,width=70,bg="black",fg="white",relief="flat")
      t_box = Text(frame1,width=70,height=1,bg="green",fg="white",relief="flat")
      text_box.edit_separator()
      text_box.grid(row=5,column=10,rowspan=7)
      t_box.grid(row=4,column=10)
      t_box.insert(END,f"{current_date}            TERMINAL                           ")
      t_box.config(state='disabled')
      sb = Scrollbar(frame1)
      def clearText():
         a = text_box.index('end-1c').split('.')[0]
         c = text_box.index('end-1c')
         b = (str(int(a)-1)+'.0')
         t = text_box.get("1.0",END)
         text_box.delete(1.0,c)
         
      def printer(root,frame1,a):
         aa = text_box.index('end-1c').split('.')[0]
         text_box.insert(END,f"\n{a}")
      Label(frame1, text="Safe payment, safe transactions",bg="red",fg="yellow").grid(row=15, column=8, columnspan=2)
      update_button = Button(frame1,text='CLEAR', bg="green", fg="white", width=20, height=2, command = lambda: clearText())
      update_button.grid(row = 15, column = 10, columnspan = 2)
      
      def pr_details(u_id, u_name):
         try:
            conn = sqlite3.connect('waterbill.db')
            c = conn.cursor()
            c.execute(f"SELECT * FROM users WHERE id={str(u_id)}")
            mydet = c.fetchall()
            for i in range(len(mydet)):
               pr = f"ID number:{mydet[i][0]} Username:{mydet[i][1]}"
               text_box.insert(END,f"\n{pr}")
         except:
            e_msg = f"Cannot retrieve your details right now."
            text_box.insert(END,f"\n{e_msg}")
      

def auth(root,frame1,uname, pwd):
   try:
      conn = sqlite3.connect('waterbill.db')
      c = conn.cursor()
      c.execute(f"SELECT * FROM users WHERE id={str(uname)}")
      cred = c.fetchall()
      if cred != []:
       try:
         for i in range(len(cred)):
            if len(pwd) >= 8 and len(pwd) <= 16:
               passwd = bcrypt.hashpw(pwd, cred[i][3].encode()).decode()
               if compare_digest(passwd, cred[i][2]) is True:
                  log_user(root,frame1,uname,cred[i][1])
               else:
                    for widget in frame1.winfo_children():
                       widget.destroy()
                    Label(frame1, text="Login failed", bg="red").grid(row=0, column=2, rowspan=1)
                    Label(frame1, text="           ",bg="steel blue").grid(row=2, column=2, rowspan=1)
                    Button(frame1,text="BACK",bg="blue",width=15,height=2,command= lambda: userLogin(root, frame1)).grid(row=4,column=2)
            else:
               show_message("Error","Invalid password length, should be at least 8 and less or equals to 16")
       except:
         show_message("Database error","Authentication error")
      else:
         show_message("Error", "User account does not exist, you can register your account!")
   except sqlite3.Error:
      show_message("Database error","User Authentication Error")
      
def adm_auth(root,frame1,uname, pwd):
   try:
      conn = sqlite3.connect('waterbill.db')
      c = conn.cursor()
      c.execute(f"SELECT * FROM admin WHERE id={str(uname)}")
      cred = c.fetchall()
      if cred != []:
       for i in range(len(cred)):
            if len(pwd) >= 8 and len(pwd) <= 16:
               passwd = bcrypt.hashpw(pwd, cred[i][3].encode()).decode()
               if compare_digest(passwd, cred[i][2]) is True:
                  log_admin(root,frame1,uname,cred[i][1])
               else:
                    for widget in frame1.winfo_children():
                       widget.destroy()
                    Label(frame1, text="Login failed", bg="red").grid(row=0, column=2, rowspan=1)
                    Label(frame1, text="           ",bg="steel blue").grid(row=2, column=2, rowspan=1)
                    Button(frame1,text="BACK",bg="blue",width=15,height=2,command= lambda: AdmLogin(root, frame1)).grid(row=4,column=2)
            else:
               Label(frame1, text='Invalid password length, try again',bg="black", fg="red").grid(row=3,column=4)
      else:
           show_message("Error","The admin user does not exist")
           
   except sqlite3.Error:
      for widget in frame1.winfo_children():
         widget.destroy()
      Label(frame1, text="User authentication error", bg="red").grid(row=0, column=2, rowspan=1)
      Label(frame1, text="           ",bg="steel blue").grid(row=2, column=2, rowspan=1)
      Button(frame1,text="BACK",bg="blue",width=15,height=2,command= lambda: AdmLogin(root, frame1)).grid(row=4,column=2)

def check_bill(root,frame1,var,txb,uname):
   try:
      conn = sqlite3.connect('waterbill.db')
      c = conn.cursor()
      try:
         c.execute("SELECT * FROM charges")
         tax = c.fetchall()
         for j in range(len(tax)):
            FixedCharge = int(tax[j][1])
            MeterCost = (int(tax[j][2])/10)
            VAT = int(tax[j][3])
      except sqlite3.Error:
         print('Charges details unretrievable')
      c.execute(f"SELECT * FROM bills WHERE id={str(var)}")
      det = c.fetchall()
      for i in range(len(det)):
         f=f'\nCurrent meter: {det[i][1]}\nConsumption: {det[i][3]}\nFixed charge: {FixedCharge}/-\nCost per unit: {MeterCost}/-\nVAT: {VAT}%\nTotall amount: {det[i][2]}/-\n'
      txb.insert(END,f)
   except sqlite3.Error as e:
      Label(frame1,text='Cannot retrieve your records, try again later',fg="red").grid(row=2,column=2)
      Label(frame1, text="           ",bg="steel blue").grid(row=3, column=2, rowspan=1)
      Button(frame1,text="BACK",bg="blue",width=15,height=2,command= lambda: log_user(root, frame1,uid,uname)).grid(row=4,column=2)

def register(root,frame1):
   for widget in frame1.winfo_children():
      widget.destroy()
   Label(frame1, text="User Registration",bg="steel blue", font=('Helvetica', 18, 'bold'),fg="yellow").grid(row = 0, column = 2, rowspan=1)
   Label(frame1, text="        ",bg="steel blue").grid(row = 1,column = 0)
   Label(frame1, text="User name:      ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 2,column = 0)
   Label(frame1, text="User ID:      ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 3,column = 0)
   Label(frame1, text="Password:       ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 4,column = 0)
   Label(frame1, text="           ",bg="steel blue").grid(row=5, column=2, rowspan=1)
   Button(frame1,text="SUBMIT",bg="blue",width=15,height=2,command= lambda: user_reg()).grid(row=6,column=2)

   uname = tk.StringVar()
   uid = tk.StringVar()
   pwd = tk.StringVar()

   e1 = Entry(frame1, textvariable = uid)
   e1.grid(row = 3,column = 2)
   e2 = Entry(frame1, textvariable = pwd, show = '*')
   e2.grid(row = 4,column = 2)
   e3 = Entry(frame1, textvariable = uname)
   e3.grid(row = 2,column = 2)
   passwd = pwd.get().encode()
   userID = uid.get()
   username = uname.get()
   def user_reg():
     if len(uid.get()) != 8:
      Label(frame1,text='Invalid ID number, check your ID number and try again',fg="red").grid(row=3,column=3,columnspan=4)
     else:
      if len(pwd.get().encode()) >= 8 and len(pwd.get().encode()) <= 16:
        try:
         _ = bcrypt.gensalt()
         th = _.decode()
         password = bcrypt.hashpw(pwd.get().encode(), _).decode()
         conn = sqlite3.connect('waterbill.db')
         c = conn.cursor()
         c.execute("INSERT INTO users (id, userName, password, slt) VALUES (?, ?, ?, ?)",(str(uid.get()), str(uname.get()), str(password), str(th)))
         conn.commit()
         try:
            temp = 0
            c.execute("INSERT INTO bills (id,prevMeter,totalBill, consumption) VALUES (?, ?, ?, ?)", (str(uid.get()), str(temp), str(temp), str(temp)))
            conn.commit()
         except sqlite3.Error as e:
            show_message("Database error","Cannot update bills table\n{e}")
         for widget in frame1.winfo_children():
            widget.destroy()
         Label(frame1,text=f'User with id {uid.get()} has been registered successfully, login to enjoy the services',fg="green").grid(row=2,column=1)
         Label(frame1, text="           ",bg="steel blue").grid(row=3, column=2, rowspan=1)
         Button(frame1,text="CONTINUE",bg="blue",width=15,height=2,command= lambda: userLogin(root, frame1)).grid(row=4,column=1)
        except sqlite3.Error as e:
          show_message(f"Database error",f"User with ID {uid.get()} already esists")

      else:
        show_message("Error","Password length should be at least 8 and not more than 16, try again")

def pay_bills(root,frame1,value,uname):
   for widget in frame1.winfo_children():
      widget.destroy()
   try:
      conn = sqlite3.connect('waterbill.db')
      c = conn.cursor()
      Label(frame1, text="Bills payment",bg="steel blue", font=('Helvetica', 18, 'bold'),fg="yellow").grid(row = 0, column = 1, rowspan=1)
      Label(frame1, text="         ",bg="steel blue").grid(row = 1,column = 0)
      Label(frame1, text="Current meter:      ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 2,column = 0)
      Label(frame1, text="       ",bg="steel blue").grid(row = 3,column = 0,rowspan=1)
      Button(frame1,text="CONTINUE",bg="blue",width=15,height=2,command= lambda: payB()).grid(row=4,column=1)
      Button(frame1,text="BACK",bg="blue",width=15,height=2,command= lambda: log_user(root, frame1,value,uname)).grid(row=4,column=3)
      meter = tk.StringVar()
      e1 = Entry(frame1, textvariable = meter)
      e1.grid(row = 2,column = 1)
      def payB():
       c.execute(f"SELECT * FROM bills WHERE id={str(value)}")
       det = c.fetchall() 
       for i in range(len(det)):
         prevMeter = int(det[i][1])
         try:
            c.execute("SELECT * FROM charges")
            charge = c.fetchall()
            for i in range(len(charge)):
              if meter.get() != '':
               try:
                if int(meter.get()) >= prevMeter:
                  consumption = int(meter.get()) - prevMeter
                  consumptionCost = (consumption * (int(charge[i][2])/10))
                  taxable = consumptionCost #+ int(charge[i][1])
                  tax = taxable * (int(charge[i][3])/100)
                  Total = taxable + tax + int(charge[i][1])
                else:
                   show_message("Entry Error",f"Meter value cannot be less than the previous readings\nPrevious meter reading is {prevMeter}!")
               except:
                   show_message("Entry Error",f"Meter value can only be an integer!")
              else:
                 show_message("Entry Error",f"Null meter value not allowed!")
         except sqlite3.Error:
            show_message("Database error",f"Data retrieval error")
       try:
        c.execute(f"UPDATE bills SET prevMeter=?, totalBill=?, consumption=? WHERE id={str(value)}", (str(meter.get()), str(Total), str(consumption)))
        conn.commit()
       except:
         return False
       for widget in frame1.winfo_children():
          widget.destroy()
       Label(frame1, text="",bg="steel blue").grid(row = 1,column = 0)
       Label(frame1,text="Thank you for paying your bills\n",fg="green").grid(row=2,column=2,columnspan=3)
       Label(frame1, text="",bg="steel blue").grid(row = 3,column = 0)
       Button(frame1,text="BACK",bg="blue",width=15,height=2,command= lambda: log_user(root, frame1,value,uname)).grid(row=4,column=2)

   except sqlite3.Error:
      show_message("Database error",f"Data retrieval error")

def p_users(root,frame1,txb):
   try:
      conn = sqlite3.connect('waterbill.db')
      c = conn.cursor()
      c.execute(f"SELECT * FROM users")
      users = c.fetchall()
      if len(users) == 0:
         txb.insert(END,"No registered users\n")
      else:
         for i in range (len(users)):
            p = f"{i+1}.[ID:{users[i][0]},USERNAME:{users[i][1]}]\n"
            txb.insert(END,p)
         
   except sqlite3.Error:
      txb.insert("An error occurred while processing")
def logout(root,frame1):
   def x(a,b):
      messagebox.showerror(a, b)
      userLogin(root,frame1)
   x("Logout", "Are you sure of logging out?")
   

def charges_update(root,frame1,uid,uname):
   for widget in frame1.winfo_children():
      widget.destroy()
   Label(frame1, text="Charges table update",fg="white",bg="black").grid(row=0,column=0,columnspan=3)
   Label(frame1, text="           ",bg="steel blue").grid(row=1, column=2, rowspan=1)
   Label(frame1, text="Fixed Charge:      ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 2,column = 0)
   Label(frame1, text="Meter Cost:      ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 3,column = 0)
   Label(frame1, text="VAT(%):       ",bg="steel blue", anchor="e", justify=LEFT).grid(row = 4,column = 0)
   Label(frame1, text="           ",bg="steel blue").grid(row=6, column=2, rowspan=1)
   Button(frame1,text="UPDATE",bg="blue",width=15,height=2,command= lambda: Update()).grid(row=7,column=2)
   Button(frame1,text="BACK",bg="blue",width=15,height=2,command= lambda: log_admin(root,frame1,uid,uname)).grid(row=7,column=4)

   fcharge = tk.StringVar()
   mcost = tk.StringVar()
   vat = tk.StringVar()

   ea = Entry(frame1, textvariable = fcharge)
   ea.grid(row = 2,column = 2)
   eb = Entry(frame1, textvariable = mcost)
   eb.grid(row = 3,column = 2)
   ec = Entry(frame1, textvariable = vat)
   ec.grid(row = 4,column = 2)
   def Update():
     if fcharge.get() != '':
       if mcost != '':
         if vat != '':
           try:
             conn = sqlite3.connect('waterbill.db')
             c = conn.cursor()
             c.execute(f"SELECT * FROM charges WHERE id=?",str(1))
             c.execute("UPDATE charges SET fixedCharge = ?, MeterCost=?, VAT=? WHERE id=?",(str(fcharge.get()), str(mcost.get()), str(vat.get()), str(1)))
             conn.commit()
             Label(frame1, text="Updated successfully!!!",fg="green").grid(row=5,column=2)
             lgs = f"{current_date} user with id {uid} made changes to charges"
             with open('waterbill.log','a') as l:
                l.write(f"\n{lgs}")
           except sqlite3.Error:
             Label(frame1, text="Update error",fg="green").grid(row=5,column=0)
         else:
           Label(frame1, text="* Required!",bg="black", fg="red").grid(row=2, column=4, columnspan=5)
       else:
         Label(frame1, text="* Required!",bg="black", fg="red").grid(row=3, column=4, columnspan=5)
     else:
        Label(frame1, text="* Required!",bg="black", fg="red").grid(row=4, column=4, columnspan=5)

def del_user(root,frame1,uid,uname):
   try:
      for widget in frame1.winfo_children():
         widget.destroy()
      Label(frame1, text="         ", bg="steel blue").grid(row=1,column=3)
      Label(frame1, text="Verification password:", bg="steel blue").grid(row=2, column=1)
      Label(frame1, text="         ", bg="steel blue").grid(row=2,column=3)
      Label(frame1, text="         ", bg="steel blue").grid(row=5,column=1)
      passwd = tk.StringVar()
      ent = Entry(frame1, textvariable = passwd, show="*")
      ent.grid(row=2, column=2)
      Button(frame1, text="CONFIRM", bg="blue",width=15,height=2,command= lambda: go_del()).grid(row=6, column=2)
      Label(frame1, text="           ", bg="steel blue").grid(row=4,column=3)
      Button(frame1,text="BACK",bg="blue",width=15,height=2,command= lambda: log_user(root,frame1,uid,uname)).grid(row=6,column=4)
      
      def go_del():
         conn = sqlite3.connect('waterbill.db')
         c = conn.cursor()
         c.execute(f"SELECT * FROM users WHERE id={str(uid)}")
         user = c.fetchall()
         for i in range(len(user)):
           pd = bcrypt.hashpw(((passwd.get()).encode()), user[i][3].encode()).decode()
           if compare_digest(pd, user[i][2]) == True:
               try:
                  c.execute(f"DELETE FROM users WHERE id={str(uid)}")
                  conn.commit()
                  c.execute(f"DELETE FROM bills WHERE id={str(uid)}")
                  conn.commit()
                  for widget in frame1.winfo_children():
                     widget.destroy()
                  Label(frame1, text='Account deleted successfully', fg="yellow", bg="steel blue").grid(row=1, column=1, columnspan=4)
                  Label(frame1, text="             ", bg="steel blue").grid(row=2,column=1)
                  Button(frame1,text="BACK",bg="blue",width=15,height=2,command= lambda: userLogin(root, frame1)).grid(row=3,column=2)
                  
               except sqlite3.Error:
                  show_message("Database error",f"Cannot remove the user from the register")
           else:
               Label(frame1, text='* Wrong password', fg="red", bg="black").grid(row=2, column=3)
   except:
      for widget in frame1.winfo_children():
         widget.destroy()
      Label(frame1, text="An error has occurred, try again!", fg="red", bg="black").grid(row=1, column=1)
      Label(frame1, text="             ", bg="steel blue").grid(row=3,column=1)
      Button(frame1,text="BACK",bg="blue",width=15,height=2,command= lambda: log_user(root,frame1,uid,uname)).grid(row=4,column=2)

def prog_quit(root,frame1,uid,uname):
   for widget in frame1.winfo_children():
      widget.destroy()
   Label(frame1, text="Are you sure you want to quit the program?", bg="steel blue").grid(row=3,column=1,columnspan=4)
   Button(frame1, text="Yes", bg="blue",width=7,height=2,command= lambda: root.destroy()).grid(row=6, column=2)
   Label(frame1, text="           ", bg="steel blue").grid(row=5,column=3)
   Button(frame1,text="No",bg="blue",width=7,height=2,command= lambda: log_admin(root,frame1,uid,uname)).grid(row=6,column=4)

def pCharges(root,frame1,tb):
   try:
      conn = sqlite3.connect('waterbill.db')
      c = conn.cursor()
      c.execute("SELECT * FROM charges")
      chg = c.fetchall()
      for i in range(len(chg)):
         pr = f"Fixed charge:{chg[i][1]}/-\nMeter cost:{int(chg[i][2])/10}/-\nVAT:{chg[i][3]}%\n"
         tb.insert(END,pr)
   except sqlite3.Error as e:
       tb.insert(END,f"Data retrieval error\n{e}")
       
def new_home():
    root = Tk()
    root.configure(bg='blue')
    root.geometry('1366x768')
    frame1 = Frame(root)
    frame2 = Frame(root)
    Home(root, frame1, frame2)


if __name__ == "__main__":
    new_home()


