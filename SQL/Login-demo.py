#%% Import
from tkinter import *
from tkinter import ttk
import DatabaseManager
from tkinter import messagebox
from tkinter import ttk

#%% Connect to SQLite3
db = DatabaseManager.DatabaseManager()
db.create_table()

#%% Main GUI window configuration
root = Tk()
root.title("Login Demo") 
root.geometry("500x160+350+300")
root.resizable(False, False)
style = ttk.Style()
#Available themes: ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
style.theme_use("vista")

#%% Variables
var_user_name = StringVar() # user name
var_user_name.set('Not defined ...') 
var_user_familyname = StringVar() # user familyname
var_user_familyname.set('Not defined...')
var_user_age = StringVar() # user age
var_user_age.set('Not defined...')

#%% Commands
# button for signin in
def btn_sign_in_command():
    try:
        exists = db.item_exists(var_user_name.get(), var_user_familyname.get(), var_user_age.get())
        if exists == True:
            messagebox.showinfo('Status','User already exists!')
        else:
            db.add_item(var_user_name.get(), var_user_familyname.get(), var_user_age.get())
            messagebox.showinfo('Status','User added!')
    except Exception as e:
        print(e)
    
# button for loging in
def btn_log_in_command():
    exists = db.item_exists(var_user_name.get(), var_user_familyname.get(), var_user_age.get())
    if exists == True:
        messagebox.showinfo('Status','Loged in!')
    else:
        messagebox.showinfo('Status','User not found!')

# button for deleting
def btn_delete_command():
    exists = db.item_exists(var_user_name.get(), var_user_familyname.get(), var_user_age.get())
    if exists == True:
        db.delete_item(var_user_name.get(), var_user_familyname.get(), var_user_age.get())
        messagebox.showinfo('Status','User deleted!')
    else:
        messagebox.showinfo('Status','User not found!')

# button for clossing the GUI
def btn_close():
    root.destroy()

#%% GUI
frame1 = LabelFrame(root, text = 'Input parameters')
frame1.config(relief=SUNKEN, bd=2)
frame1.place(x=5, y=5, width=490, height=100)

label1 = Label(frame1, text='First name:').place(x=5,y=5)
entry1 = Entry(frame1, textvariable = var_user_name).place(x=90, y=5, width=390)

label2 = Label(frame1, text='Family name:').place(x=5,y=30)
entry2 = Entry(frame1, textvariable = var_user_familyname).place(x=90,y=30, width=390)

label3 = Label(frame1, text='Age:').place(x=5, y=55)
entry3 = Entry(frame1, textvariable = var_user_age).place(x=90,y=55, width=80)


frame2 = LabelFrame(root, text = 'Actions')
frame2.config(relief=SUNKEN, bd=0)
frame2.place(x=5,y=105, width=490,height=50)

btn_sign_in = Button(frame2, text = "Sign in", command = btn_sign_in_command).place(x=5, y=5, width=80)
btn_log_in = Button(frame2, text = "Log in", command = btn_log_in_command).place(x=90, y=5, width=80)
btn_delete = Button(frame2, text = "Delete user", command = btn_delete_command).place(x=180, y=5, width=80)
btn_close = Button(frame2, text = "Close", command = btn_close).place(x=270, y=5, width=80)

# close the GUI
root.mainloop()

# Close the connection when done
db.close_connection()

