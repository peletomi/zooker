import json
import os

class Config:

    def __init__(self, **kwargs):
        self.config = dict()
        self.config.update(kwargs)

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
            self.config.update(data)
        return self

    def add_from_json(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                from_json = json.load(f)
                self.config = dict(self.config.items() + from_json.items())
        return self

    def add_from_args(self, args):
        if args:
            self.config.update(vars(args))
        return self

    def get(self, key, default=None):
        return self.config.get(key, self.config.get(key.replace('_', '-'), default))

    def __getattr__(self, item):
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

    def __contains__(self, item):
        return item in self.config

    def __len__(self):
        return len(self.config)
