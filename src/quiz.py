#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import random
import sys
import time

import cli
import gui
import fs_utils


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
        if self.quiz:
            self.load_quiz_entries()
            self.filter_entries_by_categories(args.categories)
            if args.show_categories:
                self.display_categories()
                sys.exit(0)
            if args.show_data:
                self.display_entries()
                sys.exit(0)
        if self.args.cli:
            self._interface = cli.QuizCLI(self)
        else:
            self._interface = gui.QuizGUI(self)

    def load_quiz_entries(self):
        """Load the quiz CSV into a list of QuizEntry objects."""
        csv_basename = '%s.csv' % self.quiz
        if os.path.isfile(fs_utils.data_filepath(csv_basename, True)):
            csv_path = fs_utils.data_filepath(csv_basename, True)
        else:
            csv_path = fs_utils.data_filepath(csv_basename)
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

    def start_quiz(self):
        """Start running the quiz, either through CLI or GUI."""
        self.questions_asked = 0
        self.score = 0
        self.ask_each_question_once = bool(
                self.args.forced_order or self.args.challenge)
        if not self.args.forced_order:
            random.shuffle(self.entries)
        self._start_time = time.time()
        self._interface.start_quiz()

    def next_question(self):
        """
        Ask the next question.

        After we call self._interface.prompt_user(), we expect that
        control should eventually be passed to self.process_input(),
        once the user has provided input.

        """
        if self.ask_each_question_once:
            self.active_entry = self.entries.pop(0)
        else:
            self.active_entry = random.choice(self.entries)
        self._interface.prompt_user()
    
    def process_input(self, user_input):
        """
        Provide feedback on the user's input.

        If more questions remain, ask more questions.
        Otherwise, end the quiz.

        """
        assert self.active_entry is not None
        if self.active_entry.check_answer(user_input):
            self._correct()
        else:
            self._incorrect(user_input)
        self.questions_asked += 1
        if len(self.entries):
            self.next_question()
        else:
            self.end_quiz()

    def _correct(self):
        """Process a correct answer, and trickle down to the interface."""
        self.score += 1
        self._interface.provide_feedback('Correct!')

    def _incorrect(self, user_input):
        """Process an incorrect answer, and trickle down to the interface."""
        quiz_entry = self.active_entry
        feedback = 'Incorrect.'
        feedback += '\nThe correct answer was: %s' % quiz_entry.answer
        for other_answer in quiz_entry.other_answers:
            feedback += '\nWe also would have accepted: %s' % other_answer
        other_prompts = self.get_prompts_by_answer(user_input)
        if other_prompts:
            feedback += '\nYou gave the right answer for: %s.' % other_prompts
        self._interface.provide_feedback(feedback)

    def end_quiz(self):
        elapsed_time = time.time() - self._start_time
        pct_score = 100 * round(float(self.score) / self.questions_asked, 2)
        self._interface.end_quiz(
                "It's over!\nYou scored %d%% in %d seconds." %
                (pct_score, elapsed_time))

    def get_prompts_by_answer(self, answer):
        """Build a '; '-delimited string of prompts whose answer is `answer`."""
        prompts = []
        for entry in self.entries:
            if entry.check_answer(answer):
                prompts.append(entry.prompt)
        return '; '.join(prompts)
    
    def quiz_name_with_categories(self):
        if self.args.categories:
            return '%s (%s)' % (self.quiz, ', '.join(self.args.categories))
        else:
            return self.quiz


def all_quizzes():
    """Return a list of available quizzes."""
    data_dirs = [fs_utils.data_dir()]
    private_dir = fs_utils.data_dir(True)
    if os.path.isdir(private_dir):
        data_dirs.append(private_dir)
    quizzes = []
    for data_dir in data_dirs:
        files = os.listdir(data_dir)
        files = filter(lambda f: os.path.isfile(os.path.join(data_dir, f)),
                files)
        csvs = filter(lambda f: os.path.splitext(f)[1] == '.csv', files)
        quizzes += map(lambda f: os.path.splitext(f)[0], csvs)
    return list(set(quizzes))
