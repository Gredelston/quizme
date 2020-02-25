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
        print('Quizzing on %s' % self._quiz_game.quiz)
        if len(self._quiz_game.args.categories) > 1:
            print('Categories: %s' % ', '.join(self._quiz_game.args.categories))
        elif len(self._quiz_game.args.categories) == 1:
            print('Category: %s' % self._quiz_game.args.categories[0])
        print('Respond with %s anytime to quit.' % '/'.join(EXIT_STRINGS))
        if self._quiz_game.ask_each_question_once:
            print('You will be asked %d questions.' %
                    len(self._quiz_game.entries))
            print('Time starts now.')
        self._quiz_game.next_question()

    def wait_for_input(self):
        """Collect user input, and pass control back to the QuizGame."""
        print('')
        print('%d/%d # %s' % (
                self._quiz_game.score, self._quiz_game.questions_asked,
                self._quiz_game.active_entry.prompt))
        response = input('> ').strip()
        if response.lower() in EXIT_STRINGS:
            self.exit()
        self._quiz_game.process_input(response)

    def correct(self):
        """Provide feedback for a correct answer."""
        print('Correct! 😊')

    def incorrect(self, quiz_entry, user_input):
        """Provide feedback for an incorrect answer."""
        print('Incorrect. Correct answer was: %s' % quiz_entry.answer)
        for other_answer in quiz_entry.other_answers:
            print('We also would have accepted: %s' % other_answer)
        incorrect_prompts = self._quiz_game.get_prompts_by_answer(user_input)
        if incorrect_prompts:
            print('You gave the right answer for: %s.' % incorrect_prompts)

    def end_quiz(self):
        """Report to the user that their quiz has ended."""
        pct_score = 100 * round(float(
                self._quiz_game.score) / self._quiz_game.questions_asked, 2)
        print('\nYou scored %d%% in %d seconds.' % (
                pct_score, self._quiz_game.elapsed_time))

    def exit(self, return_code=0):
        """Quit the program immediately."""
        sys.exit(return_code)
