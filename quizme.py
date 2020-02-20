#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import random
import sys

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
        self.filter_entries_by_category(args.category)
        if args.show_categories:
            self.display_categories()
            sys.exit(0)
        if args.show_data:
            self.display_entries()
            sys.exit(0)

    def load_quiz_entries(self):
        """Load the quiz CSV into a list of QuizEntry objects."""
        quizme_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(quizme_dir, '%s.csv' % self.quiz)
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

    def filter_entries_by_category(self, cat):
        """Return a list of entries that contain the given category."""
        if not cat:
            return
        cat = cat.lower()
        all_categories = self.get_categories()
        if cat not in all_categories:
            print('Invalid category: %s' % cat)
            print('Categories for this quiz: %s' % ', '.join(all_categories))
            sys.exit(1)
        self.entries = list(filter(lambda e: cat in e.categories, self.entries))

    def get_categories(self):
        """Return a list of categories in this quiz."""
        categories = []
        for entry in self.entries:
            for category in entry.categories:
                if category.lower() not in categories:
                    categories.append(category.lower())
        return categories

    def display_categories(self):
        """Display all categories in this quiz."""
        categories = self.get_categories()
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
        """Main quiz-running function."""
        print('Quizzing on %s%s' % (self.quiz,
                (' (%s)' % self.args.category) if self.args.category else ''))
        print('Respond with %s anytime to quit.' % '/'.join(EXIT_STRINGS))
        print('')
        self.questions_asked = 0
        self.score = 0
        if self.args.forced_order:
            for e in self.entries:
                self.ask_question(e)
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
            incorrect_entry = self.get_entry_by_answer(response)
            if incorrect_entry:
                print('You gave the right answer for %s.' %
                        incorrect_entry.prompt)
        self.questions_asked += 1
        print('')

    def get_entry_by_answer(self, answer):
        """Find the quiz entry whose answer is `answer` (else None)."""
        for entry in self.entries:
            if entry.check_answer(answer):
                return entry
        return None


def all_quizzes():
    """Return a list of available quizzes."""
    quizme_dir = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(quizme_dir)
    files = filter(lambda f: os.path.isfile(os.path.join(quizme_dir, f)), files)
    csvs = filter(lambda f: os.path.splitext(f)[1] == '.csv', files)
    quizzes = map(lambda f: os.path.splitext(f)[0], csvs)
    return list(quizzes)


def parse_args():
    """Parse command-line args."""
    parser = argparse.ArgumentParser(
            description='Run a flashcard-style quiz on a chosen dataset.')
    parser.add_argument('quiz', choices=all_quizzes(),
            help='The name of the quiz to run')
    parser.add_argument('category', nargs='?', default=None,
            help='Filter the quiz down to a category')
    parser.add_argument('--show-categories', action='store_true',
            help='Display all categories for the selected quiz, and quit')
    parser.add_argument('--show-data', action='store_true',
            help='Display all data for the selected quiz/category, and quit')
    parser.add_argument('--forced-order', action='store_true',
            help='Ask each question once, in order')
    return parser.parse_args(sys.argv[1:])


def main():
    """Main program function."""
    args = parse_args()
    quiz_game = QuizGame(args)
    quiz_game.run_quiz()

if __name__ == '__main__':
    main()
