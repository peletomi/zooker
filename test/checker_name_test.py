__author__ = 'pele'

import unittest

from zooker.checkers import Checker

class TestChecker(Checker):
    pass

class CheckerNameTest(unittest.TestCase):

    def test_name(self):
        checker = TestChecker()
        self.assertEqual('TestChecker', checker.get_name())