from . import utils
from . import viper
import setuptools
from distutils.cmd import Command

__version__ = '0.1.0'

class Pythonidae(type):
    def __new__(meta, name, bases, attr):
        __origin__ = attr.pop('__origin__', f"{name.lower()}.wisdom")

        for knowledge, learning in utils.package_discovery(__origin__).items():
            attr[knowledge] = utils.fill_call(learning)

        return super(Pythonidae, meta).__new__(meta, name, bases, attr)


class Kaa(metaclass=Pythonidae):

    def setup(self, **kwargs):
        return setuptools.setup(
            **self.metadata(),
            **kwargs,
        )

def born():
    kaa = Kaa()

    cmdclass = {
        name.lower(): command
        for name, command
        in utils.list_classes(
            'kaa.viper',
            _subclass = Command
        )
    }

    kaa.setup(
        cmdclass = cmdclass
    )
