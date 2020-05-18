#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A collection of utilities for processing scraped images."""
from typing import Tuple


def filename_to_adjectives(filename: str) -> Tuple[str, str]:
    """
    >>> filename_to_adjectives("wild_zahm_Adjektive_Deutsch_deutschlernerblog.png")
    ("wild", "zahm")
    """
    adj_idx = filename.find("Adjektive")
    if adj_idx == -1:
        raise Exception(
            "Expected a filename with 'Adjektive' in it but got: " + filename)
    if adj_idx == 0:
        raise Exception("Expected a filename with a trunk in it but got: " +
                        filename)

    trunk = filename[:adj_idx - 1]
    if trunk.find('_') != -1:
        sep = '_'
    elif trunk.find('-') != -1:
        sep = '-'
    else:
        raise Exception(
            "Expected a filename with '_' or '-' as separator but got: " +
            trunk)

    words = trunk.split(sep)
    if len(words) == 2:
        return (words[0], words[1])

    if len(words) != 3:
        raise Exception("Expected two or three words but got: " + str(words))

    if words[1] == 'nicht':
        return (words[0], 'nicht ' + words[2])

    # Special cases of dirty input data
    if words == ['neugierig', 'gleichgültig', 'unehrlich']:
        return ('neugierig', 'gleichgültig')
    elif words[2] == '2':
        return (words[0], words[1])

    raise Exception("When given three words, expected the second of them to " +
                    "start with nicht, but got: " + str(words) +
                    ". Add a handler " + "to this function")
