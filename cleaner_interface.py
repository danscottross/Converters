from tkinter import *
from cleaner_fcn import cleaner

root = Tk()
root.title("HANA Export Cleaner")
#root.wm_iconbitmap('logo_2.ico')
root.geometry("600x200")

def clean():
    clean_button.pack_forget()
    target_file = input_field.get()
    status_text.set('Status = Cleaning ' + target_file)
    input_field.delete(0, 'end')
    reset_button.pack(pady=10)

    try:
        cleaner(target_file)
        status_text.set('Status = Complete')
        instruction_text.set('Click Reset to clean another file')
    except FileNotFoundError:
        status_text.set('Status = Error! No such file or directory')
    except:
        status_text.set('Status = Error! Not a value file')

    input_field.pack_forget()

def reset():
    instruction_text.set("Enter the file path of the text file you would like to clean and then click 'Clean'")
    status_text.set('Status = Awaiting File')

    reset_button.pack_forget()
    input_field.delete(0, 'end')
    input_field.pack(pady=10)
    clean_button.pack(pady=10)

# Instructions
instruction_text = StringVar()
instruction_text.set("Enter the file path of the text file you would like to clean and then click 'Clean'")
instruction_label = Label(root, textvariable=instruction_text)
instruction_label.pack(pady=10)

# Status
status_text = StringVar()
status_text.set('Status = Awaiting File')
status_label = Label(root, textvariable=status_text)
status_label.pack(pady=10)

# Input
input_field = Entry(root, width=70)
input_field.pack(pady=10)

# Clean Button
clean_button = Button(root, text="Clean", command=clean)
clean_button.pack(pady=10)

# Reset Button
reset_button = Button(root, text="Reset", command=reset)

root.mainloop()
