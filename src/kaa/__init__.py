from . import utils
from . import viper
from . import snake
import setuptools

__version__ = "0.2.1"


class Pythonidae(type):
    def __new__(meta, name, bases, attr):
        __origin__ = attr.pop("__origin__", f"{name.lower()}.wisdom")

        for knowledge, learning in utils.package_discovery(__origin__).items():
            attr[knowledge] = utils.fill_call(learning)

        return super(Pythonidae, meta).__new__(meta, name, bases, attr)


class Kaa(metaclass=Pythonidae):
    def setup(self, **kwargs):
        return setuptools.setup(**self.metadata(), **self.options(), **kwargs)


def born():
    kaa = Kaa()
    kaa.setup()
