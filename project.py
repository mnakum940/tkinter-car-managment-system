from tkcalendar import Calendar
from tkinter import *
import sqlite3
from tkinter import messagebox

conn = sqlite3.connect('projectdemo1.db')
reg = sqlite3.connect('register.db')
cursor = conn.cursor()
reg_cursor = reg.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
table_exists = cursor.fetchone() is not None
reg_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='newuser'")
table_exists2 = cursor.fetchone() is not None
if not table_exists:
    cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')


# if not table_exists2:
#     reg_cursor.execute('''CREATE TABLE register (id INTEGER PRIMARY KEY,car TEXT, name TEXT, date TEXT, time TEXT)''')

root = Tk()
root.title("Car Management System")
root.geometry("1000x500")


def Register():
    car = menu.get()
    print(car)
    re_name = name.get()
    re_date = cal.get_date()
    print(re_date)
    re_time = time_str.get()
    print(re_time)
    reg_cursor.execute("INSERT INTO register (car, name, date, time) VALUES (?, ?, ?, ?)", (car, re_name,re_date,re_time))
    reg.commit()
    reg_cursor.execute("SELECT * FROM register WHERE name=?", (re_name,))
    row = reg_cursor.fetchone()
    messagebox.showinfo("Registered Successfully", "User {} booked {}".format(re_name,car))



def car_booking():
    global cal,drop, name, time, menu, time_str
    booking = Toplevel(root)
    booking.title("Car Booking")
    booking.geometry("1000x700")

    Label(booking, text="Car Booking", font=("Helvetica",40)).pack(pady=10)
    Label(booking, text="Select car:").pack(pady=20)

    menu = StringVar()
    menu.set("Select car:")

    drop = OptionMenu(booking, menu, "Fortuner", "Alto", "Wagon r", "Swift", "Innova", "Scorpio")
    drop.pack()

    name = Entry(booking, width=50, borderwidth=2)
    name.insert(0,"Name")
    name.pack(pady=10)

    Label(booking, text="Select Date: ").pack(pady=10)
    cal = Calendar(booking, selectmode='day',year=2023, month=3,day=21)
    cal.pack()

    time_str = StringVar()
    time_str.set("Select Time:")
    time = OptionMenu(booking, time_str, "9:00am","9:30am","10:00am","10:30am","11:00am","11:30am","12:00pm","12:30pm","1:00pm",
                      "1:30pm","2:00pm","2:30pm","3:00pm","3:30pm","4:00pm","4:30pm","5:00pm","5:30pm","6:00pm","6:30pm",
                      "7:00pm","7:30pm","8:00pm","8:30pm","9:00pm")
    time.pack(pady=5)

    button = Button(booking, text="Submit",command=Register)
    button.pack(pady=10)

def Admin():
    view = Toplevel(root)
    view.title("Admin")
    view.geometry("600x400")

    Label(view, text="View DataBase Sir!!!", font=("Helvetica",20)).pack(pady=10)
    reg_cursor.execute("SELECT * FROM register")

    rows = reg_cursor.fetchall()
    for row in rows:
        Label(view, text=row, font=("Helvetica",10)).pack()




def Login():
    wehave = username.get()
    pri = password.get()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (wehave, pri))
    row = cursor.fetchone()

    if wehave == "Meet" and pri == "1552":
        Admin()

    elif row is not None:
        car_booking()
    # Otherwise, show an error message
    else:
        messagebox.showerror("Login failed or Sign up", "Incorrect username or password")


def Signup():
    global newuser, newpass, conpass, newWindow
    newWindow = Toplevel(root)

    newWindow.title("Sign Up")
    newWindow.geometry("400x400")

    lb = Label(newWindow, text="Sign Up").pack(pady=20)

    newu = Label(newWindow, text="Enter Username:").pack(pady=20)
    newuser = Entry(newWindow, font=("Helvetica",10))
    newuser.pack(pady=5)

    newp = Label(newWindow, text="Create Password:").pack(pady=5)
    newpass = Entry(newWindow, font=("Helvetica",10),show="*")
    newpass.pack(pady=5)

    conp = Label(newWindow, text="Confirm Password:").pack(pady=5)
    conpass = Entry(newWindow, font=("Helvetica",10),show="*")
    conpass.pack(pady=5)

    button = Button(newWindow, text="Submit", command=Submit).pack(pady=10)

def Submit():
    user = newuser.get()
    new_pass = newpass.get()
    con_pass = conpass.get()

    if new_pass == con_pass:
        cursor.execute("SELECT * FROM users WHERE username=?", (user,))
        row = cursor.fetchone()

        if row is not None:
            messagebox.showerror("Sign-up failed", "Username already exists")
            # Otherwise, insert the new user into the database and show a success message
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",(user, new_pass))
            conn.commit()
            messagebox.showinfo("Sign-up successful", "User {} created".format(user))
    else:
        fail = Label(newWindow, text="Password could not match!!!").pack()

title = Label(root, text="Car Booking Management System", font=("Helvetica",40)).pack(pady=20)


login = Label(root, text="Log In to the system...", font=("Helvetica",10)).pack(pady=20)
user_label = Label(root, text="Username").pack()
username = Entry(root, font=("Helvetica",10))
username.pack(pady=5)

pass_label = Label(root, text="Password").pack()
password = Entry(root, font=("Helvetica",10),show="*")
password.pack(pady=5)

submit = Button(root, text="Log In", width=15, command=Login)
submit.pack(pady=5)
print(username.get())

signin = Button(root, text="Sign up",command=Signup,width=30)
signin.pack(pady=40)








root.mainloop()