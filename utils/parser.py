from configparser import ConfigParser, NoOptionError, NoSectionError


__config__ = 'config.ini'


class Config(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)
        self.load()

    def load(self):
        self.read(__config__)

    def __getitem__(self, item):
        try:
            if isinstance(item, tuple) and item[1] is not None:
                return self.get(item[1].__name__, item[0])
            else:
                return self.get('system', item)
        except NoOptionError or NoSectionError:
            return ''
