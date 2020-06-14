from .metadata import *
from .. import utils
import yaml


Metadata = utils.ContextLoader.fromModule('kaa.snake.metadata')


class Vocabulary(metaclass=utils.ContextLoader):
    def yml(self):
        data = {}
        try:
            with open(f".kaa") as file:
                data = yaml.load(file.read())["vocabulary"]
        except (FileNotFoundError, KeyError):
            return {}

        return data

    def metadata(self):
        return Metadata.load()
