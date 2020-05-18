#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from tools import anki


class ShyRemovalTestCase(unittest.TestCase):
    def test_removes_shys(self):
        self.assertEqual(anki.remove_silent_hyphens('he\u00adllo'), 'hello')
