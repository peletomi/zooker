__author__ = 'pele'

import unittest

from zooker.common import get_changes

from zooker.common import get_changed_files

class UtilTest(unittest.TestCase):

    def test_get_changed_files_empty(self):
        self.assertDictEqual({}, get_changes(""))

    def test_get_changed_files_none(self):
        self.assertDictEqual({}, get_changes(None))

    def test_get_changed_files_with_changes(self):
        changes = """
        M       foo
        A       bar
        A       quux
        """
        expected = {
            'M': ['foo'],
            'A': ['bar', 'quux']
        }
        self.assertDictEqual(expected, get_changes(changes))