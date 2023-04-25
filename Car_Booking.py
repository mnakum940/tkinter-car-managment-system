from tkcalendar import Calendar
from tkinter import *
import sqlite3
from tkinter import messagebox

root = Tk()
root.title("Car Management System")
root.geometry("1000x500")
root.resizable(False, False)
global username
bg_image = PhotoImage(file="Car-Rental-Online-Booking.png")

background_label = Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
reg = sqlite3.connect('register.db')
reg_cursor = reg.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
table_exists = cursor.fetchone() is not None
reg_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='register'")
table_exists2 = reg_cursor.fetchone() is not None
if not table_exists:
    cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
if not table_exists2:
    reg_cursor.execute('''CREATE TABLE register (id INTEGER PRIMARY KEY,car TEXT, name TEXT, date TEXT, time TEXT)''')
def car_booking():
    global cal, drop, name, time, menu, time_str, booking_bg
    booking = Toplevel(root)
    booking.title("Car Booking")
    booking.geometry("1000x700")
    booking.resizable(False, False)

    booking_bg = PhotoImage(file="booking_bg.png")

    booking_background = Label(booking,image=booking_bg)
    booking_background.place(x=0,y=0,relwidth=1,relheight=1)

    success = Label(booking, width=130, text="Successfully Login !!!", font=("Helvetica",10),bg="Green")
    success.config(fg="White")
    success.place(x=0)

    Label(booking, text="Car Booking", font=("Helvetica", 30)).place(x=400,y=130)
    Label(booking, text="Select car:",font=("Helvetica",15)).place(x=400,y=220)

    menu = StringVar()
    menu.set("Click Here:")

    drop = OptionMenu(booking, menu, "Fortuner", "Alto", "Wagon r", "Swift", "Innova", "Scorpio")
    drop.place(x=550,y=220)


    name = Entry(booking, width=50, borderwidth=2)
    name.insert(10,"Your Name")
    name.place(x=370,y=270)

    Label(booking, text="Select Date: ").place(x=490, y=320)
    cal = Calendar(booking, selectmode='day', year=2023, month=4, day=21)
    cal.place(x=400, y=350)

    time_str = StringVar()
    time_str.set("Select Time:")
    time = OptionMenu(booking, time_str, "9:00am", "9:30am", "10:00am", "10:30am", "11:00am", "11:30am", "12:00pm",
                      "12:30pm", "1:00pm",
                      "1:30pm", "2:00pm", "2:30pm", "3:00pm", "3:30pm", "4:00pm", "4:30pm", "5:00pm", "5:30pm",
                      "6:00pm", "6:30pm",
                      "7:00pm", "7:30pm", "8:00pm", "8:30pm", "9:00pm")
    time.place(x=470, y=570)

    button = Button(booking, text="Submit", width=15, bg="Green",command=Register)
    button.config(fg="White")
    button.place(x=468, y=620)

def Register():
    car = menu.get()
    re_name = name.get()
    re_date = cal.get_date()
    re_time = time_str.get()
    if car=="" or re_name=="" or re_date =="" or re_time=="":
        messagebox.showerror("Missing Value","Please fill all the details...")
    else:
        reg_cursor.execute("INSERT INTO register (car, name, date, time) VALUES (?, ?, ?, ?)", (car, re_name, re_date, re_time))
        reg.commit()
        messagebox.showinfo("Success","Registered Successfully!!!")

def Admin():
    view = Toplevel(root)
    view.title("Admin")
    view.geometry("600x400")
    view.config(bg="light blue")
    view.resizable(False, False)

    Label(view, text="View DataBase Sir!!!", font=("Helvetica",20),width=37).place(x=0)
    reg_cursor.execute("SELECT * FROM register")
    rows = reg_cursor.fetchall()
    Label(view,text=" ").pack(pady=10)
    for row in rows:
            Label(view, text=row).pack()


def Login_page():
    global Login_view
    Login_view = Toplevel(root)
    Login_view.title("Login First")
    Login_view.geometry("400x500")
    Login_view.resizable(False, False)

    global Login_bg
    Login_bg = PhotoImage(file="login_bg.png")

    Login_Background = Label(Login_view, image=Login_bg)
    Login_Background.place(x=0,y=0,relwidth=1,relheight=1)

    first_label = Label(Login_view,text="Login First!!!",width=25,font=("Helvatica",20),bg="blue")
    first_label.config(fg="white")
    first_label.place(x=0,y=0)

    username_label = Label(Login_view, text="Username : ",font=("Helvetica",10))
    username_label.place(x=60,y=80)
    username_entry = Entry(Login_view,font=("Helvetica",12))
    username_entry.place(x=150,y=80)

    password_label = Label(Login_view, text="Password : ",font=("Helvetica",10))
    password_label.place(x=60,y=130)
    password_entry = Entry(Login_view, show='*',font=("Helvetica",12))
    password_entry.place(x=150,y=130)

    login_button = Button(Login_view,width=10, text="Login",command=lambda: validate_login(username_entry.get(), password_entry.get()))
    login_button.place(x=220,y=190)

    signup_button = Button(Login_view,width=10, text="Sign Up",command=Signup)
    signup_button.place(x=80, y=190)

    def validate_login(username, password):
        if username == "admin" and password == "admin":
            Login_view.destroy()
            Admin()
        else:
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            result = cursor.fetchone()
            if result is not None:
                # Show a message box with the successful login message
                messagebox.showinfo("Success", "Login successful!")
                # Close the login window
                Login_view.destroy()
                car_booking()
            else:
                # Show a message box with the failed login message
                messagebox.showerror("Error", "Invalid login credentials!")
def Signup():
    global signup_bg, newuser, newpass, conpass,newWindow
    Login_view.destroy()
    newWindow = Toplevel(root)
    newWindow.title("Sign Up")
    newWindow.geometry("400x400")
    newWindow.resizable(False, False)

    signup_bg = PhotoImage(file="signup.png")

    signup_background = Label(newWindow,image=signup_bg)
    signup_background.place(x=0,y=0,relwidth=1,relheight=1)

    first_label = Label(newWindow, text="Create Account", width=25, font=("Helvatica", 20), bg="black")
    first_label.config(fg="white")
    first_label.place(x=0, y=0)

    Label(newWindow, text="Enter Username : ",font=("Helvetica",10)).place(x=55,y=80)
    newuser = Entry(newWindow, font=("Helvetica", 12))
    newuser.place(x=180,y=80)

    Label(newWindow, text="Create Password : ", font=("Helvetica", 10)).place(x=50, y=130)
    newpass = Entry(newWindow, font=("Helvetica", 12),show="*")
    newpass.place(x=180, y=130)

    Label(newWindow, text="Confirm Password : ",font=("Helvetica",10)).place(x=50,y=180)
    conpass = Entry(newWindow, font=("Helvetica", 12),show="*")
    conpass.place(x=180,y=180)

    button = Button(newWindow, text="Submit", command=Submit,width=10).place(x=230,y=230)

def Submit():
    user = newuser.get()
    new_pass = newpass.get()
    con_pass = conpass.get()

    if user=="" or new_pass=="" or con_pass=="":
        messagebox.showerror("Missing Value", "Fill all the details!!!")
    elif new_pass == con_pass:
        cursor.execute("SELECT * FROM users WHERE username=?", (user,))
        row = cursor.fetchone()

        if row is not None:
            messagebox.showerror("Sign-up failed", "Username already exists")
            # Otherwise, insert the new user into the database and show a success message
            newWindow.destroy()
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, new_pass))
            conn.commit()
            messagebox.showinfo("Sign-up successful", "User {} created".format(user))
            newWindow.destroy()
    else:
        Label(newWindow, text="Password could not match!!!").place(x=100,y=280)



Button(root, text="Book Car",width=15,font=("Helvatica",10),command=Login_page).place(x=850,y=450)

root.mainloop()