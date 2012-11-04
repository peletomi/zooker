import unittest

from zooker.gitutil import GitRepo

class UtilTest(unittest.TestCase):

    def setUp(self):
        self.repo = GitRepo()

    def test_parse_changes_empty(self):
        self.assertDictEqual({}, self.repo.parse_changes(""))

    def test_parse_changes_none(self):
        self.assertDictEqual({}, self.repo.parse_changes(None))

    def test_parse_changes_with_changes(self):
        changes = """
        M       foo
        A       bar
        A       quux
        """
        expected = {
            'M': ['foo'],
            'A': ['bar', 'quux']
        }
        self.assertDictEqual(expected, self.repo.parse_changes(changes))