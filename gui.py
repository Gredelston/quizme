#!/usr/bin/env python3

import tkinter as tk

class GameUI:
    def __init__(self, quiz_game):
        self._quiz_game = quiz_game

        self.root = tk.Tk()
        self.root.title('QuizMe!')

        self.top_text = tk.StringVar()
        self.top_label = tk.Label(self.root, textvariable=self.top_text)
        self.top_label.pack()

        self.prompt_text = tk.StringVar()
        self.prompt_label = tk.Label(self.root, textvariable=self.prompt_text)
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

    def set_prompt(self, text):
        self.prompt_text.set(text)

    def set_top_text(self, text):
        self.top_text.set(text)

    def submit_answer(self, event=None):
        answer = self.answer_entry.get()
        print('Submitted answer: %s' % answer)
        if answer.lower() == 'gaborone':
            self.feedback_text.set('Correct!')
        else:
            self.feedback_text.set('Incorrect. The correct answer was: Gaborone')

    def greet(self):
        print('Greetings!')

    def start_quiz(self):
        self.set_top_text(self._quiz_game.quiz)
        self.set_prompt(self._quiz_game.entries[0].prompt)
        self.root.mainloop()
