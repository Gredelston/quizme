#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk

class QuizGUI:
    """Graphical user interface to the quiz."""
    def __init__(self, quiz_game):
        """Set up UI elements"""
        self._quiz_game = quiz_game
        self.mainloop_running = False

        self.root = tk.Tk()
        self.root.title('QuizMe!')
        self.root.geometry('640x480')

        self.top_text = tk.StringVar()
        self.top_label = tk.Label(self.root, textvariable=self.top_text)
        self.top_label.pack()

        self.prompt_text = tk.StringVar()
        self.prompt_label = tk.Label(self.root, textvariable=self.prompt_text)
        self.prompt_label.pack()

        self.answer_frame = tk.Frame(self.root)
        self.answer_frame.pack()

        self.answer_entry = tk.Entry(self.answer_frame)
        self.answer_entry.bind('<Return>', self.submit_answer)
        self.answer_entry.focus()
        self.answer_entry.pack(side=tk.LEFT)

        self.answer_button = tk.Button(self.answer_frame, text='Submit',
                command=self.submit_answer)
        self.answer_button.pack(side=tk.RIGHT)

        self.feedback_text = tk.StringVar()
        self.feedback_label = tk.Label(self.root,
                textvariable=self.feedback_text)
        self.feedback_label.pack()

        self.meta_buttons_frame = tk.Frame(self.root)
        self.meta_buttons_frame.pack()

        self.load_button = tk.Button(self.meta_buttons_frame,
                text='Load data set', command=self.open_data_loader)
        self.load_button.pack(side=tk.LEFT)

        self.close_button = tk.Button(self.meta_buttons_frame, text='Close',
                command=self.exit)
        self.close_button.pack(side=tk.RIGHT)

        if not self._quiz_game.quiz:
            self.end_quiz('')
            self.root.mainloop()

    def open_data_loader(self):
        pass
    
    def prompt_user(self):
        """Ask the user a quiz question"""
        self.prompt_text.set('(%d/%d) %s' % (
                self._quiz_game.score, self._quiz_game.questions_asked,
                self._quiz_game.active_entry.prompt))

    def provide_feedback(self, message):
        """Send a message to the user"""
        self.feedback_text.set(message)

    def submit_answer(self, event=None):
        """When the user presses Submit, send their input to the QuizGame"""
        answer = self.answer_entry.get()
        self.answer_entry.delete(0, 'end')
        self._quiz_game.process_input(answer)

    def start_quiz(self):
        """Start the quiz, and wait for user input"""
        self.top_text.set('Quizzing on %s' %
                self._quiz_game.quiz_name_with_categories())
        self.prompt_text.set(self._quiz_game.entries[0].prompt)
        self.mainloop_running = True
        self._quiz_game.next_question()
        self.root.mainloop()

    def end_quiz(self, message):
        """Wait patiently for the user to close the quiz"""
        self.prompt_text.set(message)
        self.answer_entry.config(state='disabled')
        self.answer_button.config(state='disabled')
        self.answer_entry.unbind('<Return>')

    def exit(self):
        """End the program immediately."""
        self.root.quit()