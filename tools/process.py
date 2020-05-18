#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A collection of utilities for processing scraped images."""
import abc
from contextlib import closing
from os import path
import tempfile
from typing import Tuple, Union

from PIL import Image, ImageChops


def filename_to_adjectives(filename: str) -> Tuple[str, str]:
    """
    >>> filename_to_adjectives("wild_zahm_Adjektive_Deutsch_deutschlernerblog.png")
    ("wild", "zahm")
    """
    filename = path.basename(filename)
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


def get_picture_size(pic_filename: str) -> Tuple[int, int]:
    with Image.open(pic_filename) as im:
        return im.size


def remove_subs(pic: Image) -> Image:
    size = pic.size
    if size[1] == 402:
        return pic.crop((0, 0, size[0], 330))
    if size[1] == 803:
        return pic.crop((0, 0, size[0], 660))
    raise Exception("Not Implemented")


def split_double_adjective_img(
        pic: Image.Image) -> Tuple[Image.Image, Image.Image]:
    size = pic.size
    return (
        pic.crop((0, 0, pic.size[0] // 2, size[1])),
        pic.crop((pic.size[0] // 2, 0, pic.size[0], size[1])),
    )


class AdjectivePic(abc.ABC):
    @abc.abstractmethod
    def get_size(self) -> Tuple[int, int]:
        pass

    @abc.abstractmethod
    def get_filename(self) -> str:
        pass

    @abc.abstractmethod
    def remove_subs(self):
        pass

    def to_image(self) -> Image.Image:
        return Image.open(self.get_filename())

    __hash__ = None  # type: ignore


class SingleAdjectivePic(AdjectivePic):
    def __init__(self, filename: str, adjective: str, subs: bool):
        self.filename = filename
        self.adjective = adjective
        self.subs = subs

    @staticmethod
    def from_image(img: Image, adjective: str,
                   subs: bool) -> 'SingleAdjectivePic':
        with tempfile.NamedTemporaryFile(delete=False,
                                         prefix=adjective +
                                         ('_sub' if subs else '') + '_',
                                         suffix='.png') as tmp:
            img.save(tmp)
            filename = tmp.name
        return SingleAdjectivePic(filename, adjective, subs)

    def get_size(self) -> Tuple[int, int]:
        return get_picture_size(self.filename)

    def get_filename(self) -> str:
        return self.filename

    def remove_subs(self) -> AdjectivePic:
        if not self.subs:
            return self
        with self.to_image() as img:
            no_sub_img = remove_subs(img)
        return SingleAdjectivePic.from_image(no_sub_img,
                                             adjective=self.adjective,
                                             subs=False)

    def __eq__(self, other):
        with self.to_image() as img,\
                other.to_image() as other_img:
            diff = ImageChops.difference(img, other_img)
            if diff.getbbox():
                return True

        return (self.adjective == other.adjective
                and self.adjective == other.adjective
                and self.subs == other.subs)


class DoubleAdjectivePic(AdjectivePic):
    def __init__(self, filename: str, left_adjective: str,
                 right_adjective: str, subs: bool):
        self.filename = filename
        self.subs = subs
        self.left_adjective, self.right_adjective = (left_adjective,
                                                     right_adjective)

    @staticmethod
    def from_original(filename: str, subs: bool):
        left_adjective, right_adjective = (filename_to_adjectives(filename))
        return DoubleAdjectivePic(filename, left_adjective, right_adjective,
                                  subs)

    @staticmethod
    def from_image(img: Image, left_adjective: str, right_adjective: str,
                   subs: bool) -> 'DoubleAdjectivePic':
        with tempfile.NamedTemporaryFile(delete=False,
                                         prefix=left_adjective + '_' +
                                         right_adjective + '_' +
                                         ('_sub' if subs else '') + '_',
                                         suffix='.png') as tmp:
            img.save(tmp)
            filename = tmp.name
        return DoubleAdjectivePic(filename, left_adjective, right_adjective,
                                  subs)

    def get_size(self) -> Tuple[int, int]:
        return get_picture_size(self.filename)

    def get_filename(self) -> str:
        return self.filename

    def split(self) -> Tuple[SingleAdjectivePic, SingleAdjectivePic]:
        with Image.open(self.filename) as img:
            left, right = split_double_adjective_img(img)
            with closing(left) as left, closing(right) as right:
                return (SingleAdjectivePic.from_image(left,
                                                      self.left_adjective,
                                                      self.subs),
                        SingleAdjectivePic.from_image(right,
                                                      self.right_adjective,
                                                      self.subs))

    def remove_subs(self) -> 'DoubleAdjectivePic':
        if not self.subs:
            return self
        with self.to_image() as img:
            no_sub_img = remove_subs(img)
        return DoubleAdjectivePic.from_image(
            no_sub_img,
            left_adjective=self.left_adjective,
            right_adjective=self.right_adjective,
            subs=False)

    def __eq__(self, other):
        with self.to_image() as img,\
                other.to_image() as other_img:
            diff = ImageChops.difference(img, other_img)
            if diff.getbbox():
                return True

        return (self.left_adjective == other.left_adjective
                and self.right_adjective == other.right_adjective
                and self.subs == other.subs)
