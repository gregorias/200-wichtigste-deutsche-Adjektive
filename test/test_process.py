#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from os import path
from typing import Union
import unittest

from tools import process

from PIL import Image, ImageChops

PROJECT_DIR = path.dirname(path.dirname(path.realpath(__file__)))
TESTDATA_DIR = path.join(PROJECT_DIR, 'testdata')
# A 640x402 double picture with subs
LEFT_RIGHT_IMG = path.join(
    TESTDATA_DIR, "left_right_Adjektive_Deutsch_deutschlernerblog.png")
LEFT_IMG = path.join(TESTDATA_DIR, "left.png")
LEFT_NO_SUBS_IMG = path.join(TESTDATA_DIR, "left_no_subs.png")
RIGHT_IMG = path.join(TESTDATA_DIR, "right.png")


def assertTwoImagesEqual(self, a: Image, b: Image, msg=None):
    diff = ImageChops.difference(a, b)
    if diff.getbbox():
        raise self.failureException(
            "The picture images differ.\n{}".format(msg))


class FilenameToAdjectivesTestCase(unittest.TestCase):
    def test_filename_to_adjectives_rejects_malformed_filenames(self):
        with self.assertRaises(Exception):
            process.filename_to_adjectives("xyz.png")

    def test_filename_to_adjectives_rejects_missing_trunk(self):
        with self.assertRaises(Exception):
            process.filename_to_adjectives("Adjektive-deutschlernerblog.png"),

    def test_filename_to_adjectives_rejects_missing_separators(self):
        with self.assertRaises(Exception):
            process.filename_to_adjectives(
                "wildzahmAdjektiveDeutschdeutschlernerblog.png"),

    def test_filename_to_adjectives_parses_a_basic_case(self):
        self.assertEqual(
            process.filename_to_adjectives(
                "wild_zahm_Adjektive_Deutsch_deutschlernerblog.png"),
            ("wild", "zahm"))

    def test_filename_to_adjectives_parses_a_pair_with_nicht(self):
        self.assertEqual(
            process.filename_to_adjectives(
                "nett_nicht_nett_Adjektive_Deutsch_deutschlernerblog.png"),
            ("nett", "nicht nett"))

    def test_filename_to_adjectives_parses_a_hyphen(self):
        self.assertEqual(
            process.filename_to_adjectives(
                "wertvoll-wertlos-Adjektive-Bilder-Gegensatzpaare-deutschlernerblog.png"
            ), ("wertvoll", "wertlos"))

    def test_filename_to_adjectives_parses_with_dirname(self):
        self.assertEqual(
            process.filename_to_adjectives(
                "/a/full/path/wertvoll-wertlos-Adjektive-Bilder-Gegensatzpaare-deutschlernerblog.png"
            ), ("wertvoll", "wertlos"))


class PictureSizeTestCase(unittest.TestCase):
    def test_get_picture_size_returns_correct_size(self):
        self.assertEqual(process.get_picture_size(LEFT_RIGHT_IMG), (640, 402))


class SubtitleRemovalTestCase(unittest.TestCase):
    def test_remove_subs(self):
        with Image.open(LEFT_IMG) as left_img, \
                Image.open(LEFT_NO_SUBS_IMG) as left_no_subs_img:
            assertTwoImagesEqual(self, process.remove_subs(left_img),
                                 left_no_subs_img)


class SplitTestCase(unittest.TestCase):
    def test_split_double_adjective_img(self):
        with Image.open(LEFT_IMG) as left_img, \
              Image.open(RIGHT_IMG) as right_img, \
              Image.open(LEFT_RIGHT_IMG) as left_right_img:
            l, r = process.split_double_adjective_img(left_right_img)
            assertTwoImagesEqual(self, l, left_img)
            assertTwoImagesEqual(self, r, right_img)

    def test_split_double_adjective_pic(self):
        dap = process.DoubleAdjectivePic.from_original(LEFT_RIGHT_IMG)
        expected_left_pic = process.SingleAdjectivePic(LEFT_IMG,
                                                       adjective='left',
                                                       subs=True)
        expected_right_pic = process.SingleAdjectivePic(RIGHT_IMG,
                                                        adjective='right',
                                                        subs=True)
        self.assertEqual(dap.split(), (expected_left_pic, expected_right_pic))
