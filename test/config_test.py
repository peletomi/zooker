
from zooker.config import Config

import unittest
import argparse
import os

class ConfigTest(unittest.TestCase):

    def test_default(self):
        config = Config.from_dict({'foo': 'bar'})
        self.assertEqual('bar', config['foo'])

    def test_attribute_access(self):
        config = Config.from_dict({'foo': 'bar'})
        self.assertEqual('bar', config.foo)

    def test_attribute_with_dash(self):
        config = Config.from_dict({'foo-bar': 'quux'})
        self.assertEqual('quux', config.foo_bar)

    def test_default_chaining(self):
        config = Config.from_dict({'foo': 'bar'}).add_from_dict({'baz': 'quux'})
        self.assertEqual('quux', config['baz'])

    def test_from_file(self):
        path = os.path.dirname(os.path.abspath(__file__))
        config = Config.from_json(os.path.join(path, 'someconfig.json'))
        self.assertEqual('bar', config['foo'])

    def test_add_argparse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--foo')
        args = parser.parse_args(['--foo', 'bar'])
        config = Config()
        config.add_from_args(args)
        self.assertEqual('bar', config['foo'])