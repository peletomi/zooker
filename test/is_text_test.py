
import unittest

from zooker.checkers import is_text

class IsTextTest(unittest.TestCase):

    def test_true(self):
        for test in ['foo.sql', 'bar.java', 'quux.xml', 'foobar.txt', 'some.properties', 'service.wsdl']:
            self.assertTrue(is_text(test), "failed [%s]" % test)

    def test_false(self):
        for test in ['foo.jpg', 'bar.exe']:
            self.assertFalse(is_text(test), "failed [%s]" % test)