#!/usr/bin/env python3

import tkinter as tk

class GameUI:
    def __init__(self, master):
        self.master = master
        master.title('QuizMe')

        self.prompt_label = tk.Label(master, text='Prompt will go here.')
        self.prompt_label.pack()

        self.answer_entry = tk.Entry(master)
        self.answer_entry.pack()

        self.answer_button = tk.Button(master, text='Submit',
                command=self.submit_answer)
        self.answer_button.pack()

        self.close_button = tk.Button(master, text='Close', command=master.quit)
        self.close_button.pack()

    def submit_answer(self):
        print('Answer: %s' % self.answer_entry.get())

    def greet(self):
        print('Greetings!')

root = tk.Tk()
my_gui = GameUI(root)
root.mainloop()
