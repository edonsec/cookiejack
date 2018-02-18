import json


class Cookie(object):
    def __init__(self, name, value, domain, url=None, path="/", expiry=None):
        self.name = name
        self.value = value
        self.domain = domain
        self.path = path
        self.url = url
        self.expiry = expiry

    def to_json(self):
        return json.dumps(self.__dict__)
