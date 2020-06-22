from . import utils
from . import viper
from . import snake
from .egg import entry_point
import setuptools

__version__ = "0.4.0"

import inspect


class Pythonidae(type):
    def __new__(meta, name, bases, attr):
        __origin__ = attr.pop("__origin__", f"{name.lower()}.wisdom")

        for knowledge, learning in utils.package_discovery(__origin__).items():
            attr[knowledge] = utils.fill_call(learning)

        return super(Pythonidae, meta).__new__(meta, name, bases, attr)


class Kaa(metaclass=Pythonidae):
    def setup(self, **kwargs):
        return setuptools.setup(**self.metadata(), **self.options(), **kwargs)

    def __repr__(self):
        attr = [
            name for name, _ in inspect.getmembers(self) if not name.startswith("_")
        ]

        return "Kaa({})".format(", ".join(attr))


def born():
    kaa = Kaa()
    kaa.setup()


@entry_point("console_scripts")
def egg():
    kaa = Kaa()
    print(kaa)
