import json
import os

class Config:

    def __init__(self):
        self.config = dict()

    @classmethod
    def from_dict(cls, defaults):
        config = Config()
        config.add_from_dict(defaults)
        return config

    @classmethod
    def from_json(cls, path):
        config = Config()
        config.add_from_json(path)
        return config

    def add_from_default_locations(self):
        self.add_from_json('/etc/zookerrc')
        self.add_from_json(os.path.join(os.path.expanduser('~'), '.zookerrc'))
        return self

    def add_from_dict(self, data):
        if data and type(data) == dict:
            self.config = dict(self.config.items() + data.items())
        self.__setattr()
        return self

    def add_from_json(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                from_json = json.load(f)
                self.config = dict(self.config.items() + from_json.items())
        self.__setattr()
        return self

    def add_from_args(self, args):
        if args:
            self.config = dict(self.config.items() + vars(args).items())
        self.__setattr()
        return self

    def __setattr(self):
        for k, v in self.config.iteritems():
            k = k.replace('-', '_')
            setattr(self, k, v)

    def __getitem__(self, item):
        return self.config[item]

    def __contains__(self, item):
        return item in self.config

    def __len__(self):
        return len(self.config)