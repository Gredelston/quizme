#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import random
import sys
import time

import gui

EXIT_STRINGS = ('q', 'exit')

# Bind raw_input to input, in case of Python 2
try:
    input = raw_input
except NameError:
    pass


class QuizEntry(object):
    """Data from a single row of the source CSV."""
    def __init__(self, prompt, answer, categories=None, other_answers=None):
        """
        @param prompt: The string shown to a user.
        @param answer: The string answer a user should provide.
        @param categories: A ';'-delimited string, where each substring
                           is a category to which this entry belongs.
        @param other_answers: A ';'-delimited string, where each
                              substring is also an acceptable response.

        """
        assert prompt
        assert answer
        self.prompt = prompt
        self.answer = answer
        self.categories = categories.split(';') if categories else []
        self.other_answers = other_answers.split(';') if other_answers else []

    def check_answer(self, answer):
        """Check whether a user's answer is correct."""
        answer = answer.lower()
        if answer == self.answer.lower():
            return True
        elif answer in [a.lower() for a in self.other_answers]:
            return True
        return False

    def __str__(self):
        """Pretty-print the QuizEntry."""
        all_answers = ' ~OR~ ' .join([self.answer] + self.other_answers)
        s = '%s: %s' % (self.prompt, all_answers)
        if self.categories:
            s += ' (%s)' % ', '.join(self.categories)
        return s


class QuizGame(object):
    """Class to run the actual quiz-game."""
    def __init__(self, args):
        """
        @param args: hashable object of command-line args

        """
        self.args = args
        self.quiz = args.quiz
        self.load_quiz_entries()
        self.filter_entries_by_categories(args.categories)
        if args.show_categories:
            self.display_categories()
            sys.exit(0)
        if args.show_data:
            self.display_entries()
            sys.exit(0)

    def load_quiz_entries(self):
        """Load the quiz CSV into a list of QuizEntry objects."""
        quizme_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(quizme_dir, 'data')
        csv_path = os.path.join(data_dir, '%s.csv' % self.quiz)
        with open(csv_path)as csvfile:
            quizreader = csv.DictReader(csvfile)
            self.entries = []
            for row in quizreader:
                prompt = row['prompt']
                answer = row['answer']
                categories = row.get('categories', '').lower().replace(' ', '-')
                other_answers = row.get('other_answers', None)
                if not prompt or not answer:
                    print('Invalid CSV row (must contain prompt and answer):')
                    print(row)
                    sys.exit(1)
                entry = QuizEntry(prompt, answer, categories, other_answers)
                self.entries.append(entry)

    def filter_entries_by_categories(self, cats):
        """Return a list of entries that contain the given categories."""
        if not cats:
            return
        cats = [cat.lower() for cat in cats]
        all_cats = self.all_categories()
        for cat in cats:
            if cat not in all_cats:
                print('Invalid category: %s' % cat)
                print('Categories for this quiz: %s' % ', '.join(all_cats))
                sys.exit(1)
        self.entries = list(filter(lambda e:
                any([c in cats for c in e.categories]),
                self.entries))

    def all_categories(self):
        """Return a list of categories in this quiz."""
        categories = []
        for entry in self.entries:
            for category in entry.categories:
                if category.lower() not in categories:
                    categories.append(category.lower())
        return categories

    def display_categories(self):
        """Display all categories in this quiz."""
        categories = self.all_categories()
        if categories:
            print("Valid categories for quiz '%s':" % self.quiz)
            print(', '.join(categories))
        else:
            print("There are no categories for quiz '%s'." % self.quiz)

    def display_entries(self):
        """Display all the entries in this quiz."""
        for e in self.entries:
            print(e)

    def run_quiz(self):
        """Start running the quiz, either through CLI or GUI."""
        if self.args.gui:
            self.run_gui_quiz()
        else:
            self.run_cli_quiz()

    def run_gui_quiz(self):
        """Main loop for a graphical user interface quiz."""
        self.gui = gui.GameUI()
        self.gui.mainloop()

    def run_cli_quiz(self):
        """Main loop for a command-line quiz.""" 
        print('Quizzing on %s' % self.quiz)
        if len(self.args.categories) > 1:
            print('Categories: %s' % ', '.join(self.args.categories))
        elif len(self.args.categories) == 1:
            print('Category: %s' % self.args.categories[0])
        print('Respond with %s anytime to quit.' % '/'.join(EXIT_STRINGS))
        print('')
        self.questions_asked = 0
        self.score = 0
        if self.args.forced_order or self.args.challenge:
            if self.args.challenge:
                random.shuffle(self.entries)
            print('You will be asked %d questions.' % len(self.entries))
            print('Time starts now.')
            print()
            start_time = time.time()
            for e in self.entries:
                self.ask_question(e)
            elapsed_time = time.time() - start_time
            pct_score = round(float(self.score) / self.questions_asked, 2) * 100
            print('You scored %d%% in %d seconds.' % (pct_score, elapsed_time))
        else:
            while True:
                self.ask_question(random.choice(self.entries))

    def ask_question(self, entry):
        """Prompt the user, score their answer, and display feedback."""
        print('%d/%d # %s' % (self.score, self.questions_asked, entry.prompt))
        response = input('> ').strip()
        if response.lower() in EXIT_STRINGS:
            sys.exit(0)
        elif entry.check_answer(response):
            print('Correct! 😊')
            self.score += 1
        else:
            print('Incorrect. Correct answer was: %s' % entry.answer)
            for other_answer in entry.other_answers:
                print('We also would have accepted: %s' % other_answer)
            incorrect_prompts = self.get_prompts_by_answer(response)
            if incorrect_prompts:
                print('You gave the right answer for: %s.' % incorrect_prompts)
        self.questions_asked += 1
        print('')

    def get_prompts_by_answer(self, answer):
        """Build a '; '-delimited string of prompts whose answer is `answer`."""
        prompts = []
        for entry in self.entries:
            if entry.check_answer(answer):
                prompts.append(entry.prompt)
        return '; '.join(prompts)


def all_quizzes():
    """Return a list of available quizzes."""
    quizme_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(quizme_dir, 'data')
    files = os.listdir(data_dir)
    files = filter(lambda f: os.path.isfile(os.path.join(data_dir, f)), files)
    csvs = filter(lambda f: os.path.splitext(f)[1] == '.csv', files)
    quizzes = map(lambda f: os.path.splitext(f)[0], csvs)
    return list(quizzes)
