#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


EXIT_STRINGS = ('q', 'exit')

# Bind raw_input to input, in case of Python 2
try:
    input = raw_input
except NameError:
    pass

class QuizCLI(object):
    """Command-line user interface to the quiz."""
    def __init__(self, quiz_game):
        self._quiz_game = quiz_game

    def start_quiz(self):
        """Show the user that the quiz has started."""
        print('Quizzing on %s' % self._quiz_game.quiz_name_with_categories())
        print('Respond with %s anytime to quit.' % '/'.join(EXIT_STRINGS))
        if self._quiz_game.ask_each_question_once:
            print('You will be asked %d questions.' %
                    len(self._quiz_game.entries))
            print('Time starts now.')
        self._quiz_game.next_question()

    def prompt_user(self):
        """Collect user input, and pass control back to the QuizGame."""
        print('')
        print('%d/%d # %s' % (
                self._quiz_game.score, self._quiz_game.questions_asked,
                self._quiz_game.active_entry.prompt))
        response = input('> ').strip()
        if response.lower() in EXIT_STRINGS:
            self.exit()
        self._quiz_game.process_input(response)

    def provide_feedback(self, message):
        """Provide feedback to the user."""
        print(message)

    def end_quiz(self):
        """Process the end of the quiz."""
        pass

    def exit(self, return_code=0):
        """Quit the program immediately."""
        sys.exit(return_code)
