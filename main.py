#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

import quiz


def parse_args():
    """Parse command-line args."""
    parser = argparse.ArgumentParser(
            description='Run a flashcard-style quiz on a chosen dataset.')
    parser.add_argument('quiz', choices=quiz.all_quizzes(),
            help='The name of the quiz to run')
    parser.add_argument('categories', nargs='*', default=None,
            help='Filter the quiz down by category/ies')
    parser.add_argument('--show-categories', action='store_true',
            help='Display all categories for the selected quiz, and quit')
    parser.add_argument('--show-data', action='store_true',
            help='Display all data for the selected quiz/category, and quit')
    parser.add_argument('--challenge', action='store_true',
            help='Ask each question once, randomly shuffled')
    parser.add_argument('--forced-order', action='store_true',
            help='Ask each question once, in order')
    return parser.parse_args(sys.argv[1:])

def main():
    """Main program function."""
    args = parse_args()
    quiz_game = quiz.QuizGame(args)
    quiz_game.run_quiz()

if __name__ == '__main__':
    main()
