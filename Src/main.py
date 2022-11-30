import tkinter as tk
import mysql.connector as sql
from dotenv import load_dotenv
import os
from tkinter import messagebox
from werkzeug.security import check_password_hash, generate_password_hash


# Global variables
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
    domain = tk.Entry(frameInput, font=("default", 22))
    domain.grid(column=1, row=0)

    tk.Label(frameInput, text="Password: ", font=(
        "default", 22)).grid(column=0, row=1)
    password = tk.Entry(frameInput, font=("default", 22))
    password.grid(column=1, row=1)

    # TODO Check if logged in
    SearchButton = tk.Button(frameInput, text="Search", command=searchButton)
    SearchButton.grid(column=1, row=2)

    # Creating output side

    addButton = tk.Button(nav, text="+")
    addButton.grid(column=0, row=0)

    deleteButton = tk.Button(nav, text="-")
    deleteButton.grid(column=1, row=0)

    newHeight = window.winfo_height() - nav.winfo_height()
    names = tk.Listbox(frameOutput, width=int(
        window.winfo_width()/2), height=newHeight)
    names.pack()

    window.mainloop()


def searchButton():
    if usrID:
        search()
        return
    else:
        loginPage()


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
        window.destroy()


# TODO Import everything from the user
# TODO +, - Buttons
# TODO Search in database        


# Calling Main
main()
