#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import random
import sys

EXIT_STRINGS = ('q', 'exit')

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


def parse_args():
    """Parse command-line args."""
    parser = argparse.ArgumentParser()
    parser.add_argument('quiz', choices=['best-picture'])
    parser.add_argument('--category', default=None)
    parser.add_argument('--categories', action='store_true')
    parser.add_argument('--show-data', action='store_true')
    return parser.parse_args(sys.argv[1:])


def display_categories(quiz_name):
    """Given just the quiz name, display categories and quit."""
    quiz_entries = load_quiz_entries(quiz_name)
    categories = get_categories(quiz_entries)
    print("Valid categories for quiz '%s':" % quiz_name)
    print(', '.join(categories))
    sys.exit(0)


def display_entries(args):
    entries = load_quiz_entries(args.quiz)
    entries = filter_entries_by_category(entries, args.category)
    for e in entries:
        print(e)
    sys.exit(0)


def load_quiz_entries(quiz):
    """Load the quiz CSV into a list of QuizEntry objects."""
    quiz_entries = []
    with open('%s.csv' % quiz)as csvfile:
        quizreader = csv.DictReader(csvfile)
        for row in quizreader:
            prompt = row['prompt']
            answer = row['answer']
            categories = row['categories']
            other_answers = row['other_answers']
            entry = QuizEntry(prompt, answer, categories, other_answers)
            quiz_entries.append(entry)
    return quiz_entries


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


def filter_entries_by_category(entries, cat):
    """Return a list of entries that contain the given category."""
    all_categories = get_categories(entries)
    if cat not in all_categories:
        print('Invalid category: %s' % cat)
        print('Categories for this quiz: %s' % ', '.join(all_categories))
        sys.exit(1)
    return list(filter(lambda entry: cat in entry.categories, entries))


def run_quiz(args):
    """Main quiz-running function."""
    entries = load_quiz_entries(args.quiz)
    if args.category:
        entries = filter_entries_by_category(entries, args.category)
    print('Quizzing on %s%s' % (args.quiz,
            (' (%s)' % args.category) if args.category else ''))
    print('Respond with %s anytime to quit.' % '/'.join(EXIT_STRINGS))
    print('')
    questions_asked = 0
    score = 0
    while True:
        e = random.choice(entries)
        print('%d/%d # %s' % (score, questions_asked, e.prompt))
        response = raw_input('> ').strip()
        if response.lower() in EXIT_STRINGS:
            sys.exit(0)
        elif e.check_answer(response):
            print('Correct! 😊')
            score += 1
        else:
            print('Incorrect. Correct answer was: %s' % e.answer)
            incorrect_entry = get_entry_by_answer(entries, response)
            if incorrect_entry:
                print('You gave the right answer for %s.' %
                        incorrect_entry.prompt)
        questions_asked += 1
        print('')


def main():
    """Main program function."""
    args = parse_args()
    if args.categories:
        display_categories(args.quiz)
    elif args.show_data:
        display_entries(args)
    else:
        run_quiz(args)

if __name__ == '__main__':
    main()
