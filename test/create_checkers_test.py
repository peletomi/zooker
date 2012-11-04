
from zooker.checkers import create_checkers
from zooker.config import Config

import unittest

class CreateCheckersTest(unittest.TestCase):

    def test_create(self):
        config = Config.from_dict({'checkers': { 'WhiteSpaceChecker': '' }})
        checkers = create_checkers(config)