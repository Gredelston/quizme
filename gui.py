#!/usr/bin/env python3

import tkinter as tk

class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('QuizMe!')

        self.top_label = tk.Label(self.root, text='Sample quiz, yo.')
        self.top_label.pack()

        self.prompt_label = tk.Label(self.root, text='> Capital of Botswana')
        self.prompt_label.pack()

        self.answer_entry = tk.Entry(self.root)
        self.answer_entry.bind('<Return>', self.submit_answer)
        self.answer_entry.pack()

        self.answer_button = tk.Button(self.root, text='Submit',
                command=self.submit_answer)
        self.answer_button.pack()

        self.feedback_text = tk.StringVar()
        self.feedback_label = tk.Label(self.root,
                textvariable=self.feedback_text)
        self.feedback_label.pack()

        self.close_button = tk.Button(self.root, text='Close',
                command=self.root.quit)
        self.close_button.pack()

    def submit_answer(self, event=None):
        answer = self.answer_entry.get()
        print('Submitted answer: %s' % answer)
        if answer.lower() == 'gaborone':
            self.feedback_text.set('Correct!')
        else:
            self.feedback_text.set('Incorrect. The correct answer was: Gaborone')

    def greet(self):
        print('Greetings!')

    def mainloop(self):
        self.root.mainloop()
