import tkinter as tk
import subprocess
from threading import Thread

class App:
    def __init__(self, master):
        self.master = master
        master.title("Run Python Scripts")

        self.label = tk.Label(master, text="Click a button to run the corresponding Python script:")
        self.label.pack()

        self.buttons = [
            tk.Button(master, text="<Script Name>", command=lambda: self.run_script("/path/to/script")),
            tk.Button(master, text="<Script Name>", command=lambda: self.run_script("/path/to/script")),
            tk.Button(master, text="<Script Name>", command=lambda: self.run_script("/path/to/script")),
            tk.Button(master, text="<Script Name>", command=lambda: self.run_script("/path/to/script")),
        ]

        for button in self.buttons:
            button.pack()

    def run_script(self, script):
        Thread(target=subprocess.call, args=(["python", script],)).start()

root = tk.Tk()
app = App(root)
root.mainloop()

