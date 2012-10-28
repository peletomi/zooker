
import unittest
import tempfile
import shutil
import os

from zooker.gitutil import Change
from zooker.checkers import WhiteSpaceChecker

class WhiteSpaceCheckerTest(unittest.TestCase):

    def setUp(self):
        self.checker = WhiteSpaceChecker()
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def create_file(self, filename, content):
        full_path = os.path.join(self.tempdir, filename)
        dir = os.path.dirname(full_path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(full_path, 'w') as f:
            f.write(content)
        return Change(filename, 'A', full_path)

    def test_ok(self):
        change = self.create_file('src/File.java', "foo bar")
        self.assertEquals([], self.checker.check(change))

    def test_tab(self):
        change = self.create_file('src/tab.txt', "\tfoobar")
        self.assertEquals(['[tab.txt:1] tabs'], self.checker.check(change))

    def test_empty_line(self):
        change = self.create_file('src/empty.txt', "   ")
        self.assertEquals(['[empty.txt:1] empty line with whitespace'], self.checker.check(change))

    def test_empty_line(self):
        change = self.create_file('src/trailing.txt', "foo   ")
        self.assertEquals(['[trailing.txt:1] trailing whitespace'], self.checker.check(change))

    def test_multiple(self):
        change = self.create_file('src/multiple.txt', "   \n" + """this is ok

\tbad
  and that too """)
        self.assertEquals(['[multiple.txt:1] empty line with whitespace',
                           '[multiple.txt:3] empty line with whitespace',
                           '[multiple.txt:4] tabs',
                           '[multiple.txt:5] trailing whitespace'], self.checker.check(change))