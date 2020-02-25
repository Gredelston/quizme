#!/usr/bin/env python3

import tkinter as tk

class GameUI:
    def __init__(self, master):
        self.master = master
        master.title('QuizMe')

        self.label = tk.Label(master, text='This is my first GUI!')
        self.label.pack()

        self.greet_button = tk.Button(master, text='Greet', command=self.greet)
        self.greet_button.pack()

        self.close_button = tk.Button(master, text='Close', command=master.quit)
        self.close_button.pack()

    def greet(self):
        print('Greetings!')

root = tk.Tk()
my_gui = GameUI(root)
root.mainloop()
