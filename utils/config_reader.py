import configparser
import os

class ConfigReader:
    @staticmethod
    def get_config(section, key):
        config = configparser.ConfigParser()
        # Get the path to the root config.ini
        path=os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        config.read(path)
        return config.get(section, key)
