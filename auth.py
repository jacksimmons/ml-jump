from tkinter import *
import csv

auth_file = "data/auth.csv"

def check_username(username):
    with open(auth_file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if username == row[0]:
                return True
        return False

def submit_username():
    username = username_entry['text']
    if username == 0: #Check if it is blank
        username_output['text'] = 'Please enter a valid username.'
    else:
        valid = check_username(username)
        if valid == False:
            username_output['text'] = 'Invalid username.'

auth = Tk()
auth.geometry("200x200")
auth.title("Authorisation")

username_prompt = Label(text="Username:")
username_prompt.place(x=20,y=20)

username_entry = Entry(text=0)
username_entry.place(x=20,y=40,w=150)

username_output = Label()
username_output.place(x=20,y=60)

username_submit = Button(text="Submit", command=submit_username)
username_submit.place(x=20,y=80)

auth.mainloop()
