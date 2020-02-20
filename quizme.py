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
    parser.add_argument('--category', default=None,
            help='Filter the quiz down to a category')
    parser.add_argument('--show-categories', action='store_true',
            help='Display all categories for the selected quiz, and quit')
    parser.add_argument('--show-data', action='store_true',
            help='Display all data for the selected quiz/category, and quit')
    return parser.parse_args(sys.argv[1:])


def display_categories(args, quiz_entries):
    """Given a list of quiz_entries, display all categories."""
    categories = get_categories(quiz_entries)
    print("Valid categories for quiz '%s':" % args.quiz)
    print(', '.join(categories))


def display_entries(quiz_entries):
    """Given a list of quiz_entries, display them all."""
    for e in quiz_entries:
        print(e)


def load_quiz_entries(quiz):
    """Load the quiz CSV into a list of QuizEntry objects."""
    quizme_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(quizme_dir, '%s.csv' % quiz)
    with open(csv_path)as csvfile:
        quizreader = csv.DictReader(csvfile)
        entries = []
        for row in quizreader:
            prompt = row['prompt']
            answer = row['answer']
            categories = row['categories']
            other_answers = row['other_answers']
            if not prompt or not answer:
                print('Invalid CSV row (must contain prompt and answer):')
                print(row)
                sys.exit(1)
            entry = QuizEntry(prompt, answer, categories, other_answers)
            entries.append(entry)
    return entries


def filter_entries_by_category(entries, cat):
    """Return a list of entries that contain the given category."""
    if not cat:
        return entries
    all_categories = get_categories(entries)
    if cat not in all_categories:
        print('Invalid category: %s' % cat)
        print('Categories for this quiz: %s' % ', '.join(all_categories))
        sys.exit(1)
    return list(filter(lambda entry: cat in entry.categories, entries))


def get_entry_by_answer(entries, answer):
    """Find the quiz entry whose answer is `answer` (else None)."""
    for entry in entries:
        if entry.check_answer(answer):
            return entry
    return None


def get_categories(quiz_entries):
    """From a list of quiz entries, return a list of unique categories."""
    categories = []
    for entry in quiz_entries:
        for category in entry.categories:
            if category not in categories:
                categories.append(category)
    return categories


def run_quiz(args, quiz_entries):
    """Main quiz-running function."""
    print('Quizzing on %s%s' % (args.quiz,
            (' (%s)' % args.category) if args.category else ''))
    print('Respond with %s anytime to quit.' % '/'.join(EXIT_STRINGS))
    print('')
    questions_asked = 0
    score = 0
    while True:
        e = random.choice(quiz_entries)
        print('%d/%d # %s' % (score, questions_asked, e.prompt))
        response = input('> ').strip()
        if response.lower() in EXIT_STRINGS:
            sys.exit(0)
        elif e.check_answer(response):
            print('Correct! 😊')
            score += 1
        else:
            print('Incorrect. Correct answer was: %s' % e.answer)
            incorrect_entry = get_entry_by_answer(quiz_entries, response)
            if incorrect_entry:
                print('You gave the right answer for %s.' %
                        incorrect_entry.prompt)
        questions_asked += 1
        print('')


def main():
    """Main program function."""
    args = parse_args()
    quiz_entries = load_quiz_entries(args.quiz)
    if args.show_categories:
        display_categories(args, quiz_entries)
        sys.exit(0)
    quiz_entries = filter_entries_by_category(quiz_entries, args.category)
    if args.show_data:
        display_entries(quiz_entries)
        sys.exit(0)
    run_quiz(args, quiz_entries)

if __name__ == '__main__':
    main()
