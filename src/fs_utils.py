#!/usr/bin/env python3

import os

"""Utility functions for interacting with the filesystem."""

def quizme_dir():
    return os.path.dirname(os.path.abspath(__file__))

def data_dir(private=False):
    if private:
        return os.path.join(data_dir(), 'private')
    return os.path.join(quizme_dir(), 'data')

def data_filepath(file_basename, private=False):
    return os.path.join(data_dir(private), file_basename)

def find_csv(quizname):
    csv_basename = '%s.csv' % quizname
    if os.path.isfile(data_filepath(csv_basename, True)):
        return data_filepath(csv_basename, True)
    elif os.path.isfile(data_filepath(csv_basename)):
        return data_filepath(csv_basename)
    raise ValueError('Could not find CSV %s' % csv_basename)
