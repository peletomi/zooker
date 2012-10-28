import unittest
import tempfile
import os
import shutil

from zooker.gitutil import copy_files_to, retrieve_changed_files

class TestRepo:
    def get_changed_files(self, base, commit, **kw):
        return {
            'M': ['java/FooBar.java', 'database/foo_bar.sql'],
            'A': ['java/test/QuuxTest.java', 'database/quux.sql'],
            'D': ['no_more']
        }

    def get_file_contents(self, commit, filename):
        return filename


class CopyTest(unittest.TestCase):

    def setUp(self):
        self.repo = TestRepo()
        self.basedir = tempfile.mkdtemp()

    def tearDown(self):
       shutil.rmtree(self.basedir)

    def test_copy(self):
        copy_files_to(self.basedir, self.repo, '2123', ['java/FooBar.java', 'database/foo_bar.sql'])

    def test_retrieve(self):
        changed_files = retrieve_changed_files(self.basedir, self.repo, '', '')
        self.assertEqual(5, len(changed_files)) # as there are that much changes in the test repo
        for file in changed_files:
            if file.temp_path:
                self.assertTrue(os.path.exists(file.temp_path), "file [%s] does not exists" % file.temp_path)
