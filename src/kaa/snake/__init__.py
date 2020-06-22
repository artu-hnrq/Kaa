from .metadata import *
from .options import *
from .. import utils
from ..egg import entry_point
import yaml

Metadata = utils.ContextLoader.fromModule("kaa.snake.metadata")
Options = utils.ContextBuilder.fromModule("kaa.snake.options")


@entry_point("kaa.wisdom")
class Vocabulary(metaclass=utils.ContextLoader):
    def yml(self):
        data = {}
        try:
            with open(f".kaa") as file:
                data = yaml.safe_load(file.read())["vocabulary"]
        except (FileNotFoundError, KeyError):
            return {}

        return data

    def metadata(self):
        return Metadata.load()
