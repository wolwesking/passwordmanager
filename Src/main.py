import tkinter as tk
import mysql.connector
from dotenv import load_dotenv
import os
from tkinter import messagebox

# Global variables
isLogin = False


# Initialize window
window = tk.Tk()
window.geometry("800x600")
window.title("Password manager")


def main():
    # Connecting to database
    database = connectSql()
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

        db = mysql.connector.connect(
            host=host, database=database, user=user, passwd=passwd)
        return db.cursor()
    except:
        messagebox.showerror(message="Coudn't connect to database")
        return None





def searchButton():
    if isLogin:
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

    interactButton = tk.Button(page, text="Login", command=login)
    interactButton.grid(column=1)

    tk.Label(page, text="Note: (If you don't have an account, we will automaticly create one for you)").grid(pady=50)




def login():
    return

# Calling Main
main()
