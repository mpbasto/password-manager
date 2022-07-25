import os
import pyperclip
import pandas as pd
from dotenv import load_dotenv
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle


# LOAD DATA FROM .env FILE
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
DB_PATH = os.getenv('DB_PATH')

# LOAD DB
db = pd.read_csv(DB_PATH)


# PASSWORD GENERATOR
def generate_password():
    """
    Shuffles letters, numbers and symbols to generate a password. It also copies the password into the clipboard for instante use.
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    random_letters = [choice(letters) for char in range(randint(8, 10))]
    random_symbols = [choice(symbols) for char in range(randint(2, 4))]
    random_numbers = [choice(numbers) for char in range(randint(2, 4))]

    password_list = random_letters + random_symbols + random_numbers
    shuffle(password_list)
    password = ''.join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# SAVE PASSWORD

def save_data():
    """
    Function will first verify that no fields are empty. Then, it will confirm the details with user. Only after confirmation it will save input data to the database file, clear all fields except "Email/Username" which is reset to default email address, and generate a pop-up message upon saving data.
    """
    global db
    website = website_input.get()
    username = user_input.get()
    password = password_input.get()

    if len(website) == 0 or len(password):
        messagebox.showwarning(title='Oh no!', message='Please make sure you haven\'t left any fields empty.')
    else:
        confirm = messagebox.askokcancel(title=website, message=f'These are the details to be saved for {website}: \nEmail/Username: {username} \nPassword: {password} \nIs this correct?')

        if confirm:
            new_data = pd.DataFrame({
                'Website': [website],
                'Email/Username': [username],
                'Password': [password]
            })
            db = pd.concat([db, new_data], ignore_index=True, axis=0)
            db.to_csv(DB_PATH, index=False)

            website_input.delete(0, END)
            user_input.delete(0, END)
            user_input.insert(0, EMAIL_ADDRESS)
            password_input.delete(0, END)

            messagebox.showinfo(title='Hooray!', message=f'Password saved for {website}!')
    

# UI SETUP

root = Tk()
root.title('Password Manager')
root.config(padx=50, pady=50)
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='logo.png'))

# Logo
canvas = Canvas(width=200, height=200)
padlock_img = PhotoImage(file='./logo.png')
canvas.create_image(100, 100, image=padlock_img)
canvas.grid(column=1, row=0)

# Website label & input
website_lbl = Label(text='Website:').grid(row=1, column=0)
website_input = Entry()
website_input.grid(row=1, column=1, columnspan=2, sticky='EW')
website_input.focus()

# Email/Username label & input
user_lbl = Label(text='Email/Username:').grid(row=2, column=0)
user_input = Entry()
user_input.grid(row=2, column=1, columnspan=2, sticky='EW')
user_input.insert(0, EMAIL_ADDRESS)

# Password label & input
password_lbl = Label(text='Password:').grid(row=3, column=0)
password_input = Entry()
password_input.grid(row=3, column=1, sticky='EW')

# Generate Password button
generate_btn = Button(text='Generate Password', command=generate_password) 
generate_btn.grid(row=3, column=2, padx=2)

# Add button
add_btn = Button(text='Add', command=save_data) 
add_btn.grid(row=4, column=1, columnspan=2, sticky='EW')



root.mainloop()
