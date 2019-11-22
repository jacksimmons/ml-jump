from tkinter import *
import csv

auth_file = "data/auth.csv"

def check_username(username):
    with open(auth_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if username == row[0]:
                return True
        return False

def check_password(password):
    pass

def submit_input():
    input_type = input_prompt['text']
    if input_type == 'Username:':
        username = input_box.get()
        if username == '': #Check if it is blank
            output_label['text'] = 'Please enter a username.'
        else:
            valid = check_username(username)
            if valid:
                input_prompt['text'] = 'Password:'
                input_box.lower()
                output_label['text'] = ''

                input_box_pass.delete(0, END)
                input_box_pass.place(x=20,y=40,w=150)

            if valid == False:
                output_label['text'] = 'Invalid username.'

    elif input_type == 'Password:':
        password = input_box_pass.get()
        if password == '':
            output_label['text'] = 'Please enter a password.'
        else:
            valid = check_password(password)
            if valid:
                pass


auth = Tk()
auth.geometry("200x200")
auth.title("Authorisation")

input_prompt = Label(text="Username:")
input_prompt.place(x=20,y=20)

input_box = Entry(text=0)
input_box.place(x=20,y=40,w=150)

input_box_pass = Entry(text=0, show="*")

output_label = Label()
output_label.place(x=20,y=60)

continue_button = Button(text="Continue", command=submit_input)
continue_button.place(x=20,y=80)

auth.mainloop()
