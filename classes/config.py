from configparser import ConfigParser
import os

class config:

    @staticmethod
    def get(section, key):
        # Get the current working path
        basedir = os.path.abspath(os.path.dirname(__file__))
        # Open the config
        configuration = ConfigParser()
        configuration.read(basedir + '/../config.ini')
        return configuration.get(section, key)