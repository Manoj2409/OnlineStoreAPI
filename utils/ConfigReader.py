import os
import configparser

config = configparser.RawConfigParser()

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(project_root, "configurations", "config.ini")
config.read(path)

class ReadConfig():
    @staticmethod
    def get_property(key):
        return config.get("commonInfo",key)
