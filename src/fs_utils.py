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
