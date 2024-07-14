import tkinter as tk
from tkinter import filedialog
root = tk.Tk()

def browse_button():

    # Allow user to select a directory and store it in global var
    # called folder_path
    filename = filedialog.askopenfilename()

    print(filename)

a = ""

label1 = tk.Label(text=a)
label1.pack()

open_button = tk.Button(root, text="Open File", command=browse_button)
open_button.pack()
root.mainloop()