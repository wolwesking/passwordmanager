import tkinter as tk
import mysql.connector as sql
from dotenv import load_dotenv
import os
from tkinter import messagebox
from werkzeug.security import check_password_hash, generate_password_hash


# Global variables
usrData = None
names = None
domain = None
password = None
usrID = None

# Initialize window
window = tk.Tk()
window.geometry("800x600")
window.title("Password manager")


def connectSql():
    try:
        load_dotenv()
    except:
        messagebox.showerror(message="Couldn't load env variable")

    try:
        host = os.getenv("HOST")
        database = os.getenv("DATABASE")
        user = os.getenv("USERNAME")
        passwd = os.getenv("PASSWORD")

        db = sql.connect(
            host=host, database=database, user=user, passwd=passwd)
        return db
    except:
        messagebox.showerror(message="Coudn't connect to database")
        return None


database = connectSql()


def main():
    # Connecting to database
    if not database:
        return

    if not usrData:
        loginPage()

    # Creating layout
    frameInput = tk.Frame(window)
    frameInput.pack(side="left")

    frameOutput = tk.Frame(window)
    frameOutput.pack(side="right", padx=5)

    nav = tk.Frame(frameOutput)
    nav.pack(side="bottom")

    # Creating input side
    tk.Label(frameInput, text="Domain: ", font=(
        "default", 22)).grid(column=0, row=0)

    global domain
    domain = tk.Entry(frameInput, font=("default", 22))
    domain.grid(column=1, row=0)

    tk.Label(frameInput, text="Password: ", font=(
        "default", 22)).grid(column=0, row=1)

    global password
    password = tk.Entry(frameInput, font=("default", 22))
    password.grid(column=1, row=1)

    SearchButton = tk.Button(frameInput, text="Search",
                             command=lambda: search())
    SearchButton.grid(column=1, row=2)

    # Creating output side

    addButton = tk.Button(nav, text="+", command=addBt)# TODO command=addBt
    addButton.grid(column=0, row=0)

    deleteButton = tk.Button(nav, text="-", command=deleteBt)
    deleteButton.grid(column=1, row=0)
    newHeight = window.winfo_height() - nav.winfo_height()
    global names
    # List functions
    names = tk.Listbox(frameOutput, width=int(
        window.winfo_width()/2), height=newHeight,)
    names.pack()
    names.bind('<Button-1>', showTextOnClick)
    window.mainloop()

def addBt():
    global names
    global domain
    global password
    global usrID
    
    if len(domain.get()) and len(password.get()):
        for i in usrData:
            if domain.get() == i[2]:
                messagebox.showwarning(message="The domain is already exist")
                return
        db = database.cursor()
        db.execute("INSERT INTO Passwords (UserId, Password, Domain) VALUES (%(id)s, %(pass)s, %(dom)s)", {
            'id': usrID,
            'pass': password.get(),
            'dom': domain.get()
        })
        database.commit()
        messagebox.showinfo(message="Password added")
        names.insert(0, domain.get())
    else:
        messagebox.showinfo(message="Please fill out both of the forms")

def deleteBt():
    global names

    id = names.curselection()
    if len(id):
        q = messagebox.askyesno(message="Do you want to delete this password?")
        user = names.get(id, last=None)
        if q: # TODO TEST
            db = database.cursor()
            db.execute("DELETE FROM Passwords WHERE Domain = %(domain)s;", {
                'domain':user
            })
            database.commit()
            messagebox.showinfo(message="You successfully deleted the password")
            names.delete(id, id)


def search():
    global names
    global domain
    global password

    searchName = domain.get()
    searchPass = password.get()
    names.delete(0, tk.END)
    if searchName:
        for i in usrData:
            if searchName == i[2]:
                names.insert(0, i[2])
    elif searchPass:
        for i in usrData:
            if searchPass == i[1]:
                names.insert(0, i[2])
    else:
        listInit()


def showTextOnClick(a):
    global names
    global password
    global domain
    if len(names.curselection()):
        for i in usrData:
            if names.get(names.curselection(), last=None) == i[2]:
                password.delete(0, tk.END)
                domain.delete(0, tk.END)
                password.insert(0, i[1])
                domain.insert(0, i[2])


def listInit():
    # Update list by user
    global names
    if usrData:
        for i in usrData:
            names.insert(0, i[2])


def loginPage():
    loginPage = tk.Toplevel(window)
    loginPage.geometry("800x600")
    loginPage.title("Login page")

    page = tk.Frame(loginPage, width=500)
    page.pack(pady=5)

    tk.Label(page, text="Username: ", font=(
        "default", 22)).grid(column=0, row=0)

    username = tk.Entry(page, font=("default", 22))
    username.grid(column=1, row=0)

    tk.Label(page, text="Password: ", font=(
        "default", 22)).grid(column=0, row=1)

    password = tk.Entry(page, font=("default", 22))
    password.grid(column=1, row=1)

    interactButton = tk.Button(
        page, text="Login", command=lambda: login(username, password, loginPage))
    interactButton.grid(column=1)

    tk.Label(page, text="Note: (If you don't have an account, we will automaticly create one for you)").grid(pady=50)


def login(usr, psw, window):
    usr = usr.get()
    psw = psw.get()

    # Check if the forms are not empty
    if len(usr) == 0 or len(psw) == 0:
        messagebox.showwarning(message="Please fill out the forms")
        return

    # Check if the user exist
    db = database.cursor()
    db.execute("SELECT * FROM Users WHERE Username = %(user)s AND Password = %(pass)s;", {
        'user': usr,
        'pass': psw
    })
    result = db.fetchone()

    # User doesn't exist
    if result == None:
        question = messagebox.askquestion(
            message="This user isn't registered, do you want to register?")
        if question == 'yes':
            db = database.cursor()
            db.execute(
                "INSERT INTO Users (Username, Password) VALUES (%(user)s, %(pass)s);", {
                    'user': usr,
                    'pass': psw
                })
            database.commit()
            messagebox.showinfo(message="Registered")
    else:
        # User exist
        global usrID
        usrID = result[0]
        db = database.cursor()
        db.execute("SELECT * FROM Passwords WHERE UserID = %(id)s;", {
            'id': result[0]
        })
        user = db.fetchall()
        global usrData
        usrData = user
        window.destroy()
        listInit()


# TODO +, - Buttons


# Calling Main
main()
