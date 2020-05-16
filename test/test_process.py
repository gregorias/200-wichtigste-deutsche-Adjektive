#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from tools import process

class FilenameToAdjectivesTestCase(unittest.TestCase):
    def test_filename_to_adjectives_rejects_malformed_filenames(self):
        with self.assertRaises(Exception):
            process.filename_to_adjectives("xyz.png")

    def test_filename_to_adjectives_rejects_missing_trunk(self):
        with self.assertRaises(Exception):
            process.filename_to_adjectives(
                "Adjektive-deutschlernerblog.png"),

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
