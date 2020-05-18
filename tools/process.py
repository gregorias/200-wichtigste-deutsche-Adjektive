#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A collection of utilities for processing scraped images."""
from typing import Tuple

from PIL import Image


def get_picture_size(pic_filename: str) -> Tuple[int, int]:
    with Image.open(pic_filename) as im:
        return im.size


class AdjectivePic:
    def __init__(self, filename: str, adjective: str, subtitle: bool):
        self.filename = filename
        self.adjective = adjective
        self.subtitle = subtitle

    def get_size(self) -> Tuple[int, int]:
        return get_picture_size(self.filename)


def remove_subtitle_from_adjective_pic(pic: AdjectivePic) -> AdjectivePic:
    if not pic.subtitle:
        return pic
    raise Exception("Not Implemented")


class DoubleAdjectivePic:
    def __init__(self, filename: str, subtitles: bool):
        self.filename = filename
        self.subtitles = subtitles
        self.left_adjective, self.right_adjective = (
            filename_to_adjectives(filename))

    def get_size(self) -> Tuple[int, int]:
        return get_picture_size(self.filename)


def remove_subtitles_from_double_adjective_pic(
        pic: DoubleAdjectivePic) -> DoubleAdjectivePic:
    if not pic.subtitles:
        return pic

    size = pic.get_size()
    if size == (640, 402):
        pass
    raise Exception("Not Implemented")


def split_double_adjective_pic(
        pic: DoubleAdjectivePic) -> Tuple[AdjectivePic, AdjectivePic]:
    raise Exception("Not Implemented")


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
