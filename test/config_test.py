
from zooker.config import Config

import unittest
import argparse

class ConfigTest(unittest.TestCase):

    def test_default(self):
        config = Config.from_dict({'foo': 'bar'})
        self.assertEqual('bar', config['foo'])

    def test_default_chaining(self):
        config = Config.from_dict({'foo': 'bar'}).add_from_dict({'baz': 'quux'})
        self.assertEqual('quux', config['baz'])

    def test_from_file(self):
        config = Config.from_json('./someconfig.json')
        self.assertEqual('bar', config['foo'])

    def test_add_argparse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--foo')
        args = parser.parse_args(['--foo', 'bar'])
        config = Config()
        config.add_from_args(args)
        self.assertEqual('bar', config['foo'])