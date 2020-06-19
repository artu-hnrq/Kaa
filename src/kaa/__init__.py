from . import utils
from . import viper
from distutils.cmd import Command
import setuptools
import setupcfg

__version__ = "0.2.0"


class Pythonidae(type):
    def __new__(meta, name, bases, attr):
        __origin__ = attr.pop("__origin__", f"{name.lower()}.wisdom")

        for knowledge, learning in utils.package_discovery(__origin__).items():
            attr[knowledge] = utils.fill_call(learning)

        return super(Pythonidae, meta).__new__(meta, name, bases, attr)


class Kaa(metaclass=Pythonidae):
    def setup(self, **kwargs):
        return setuptools.setup(**self.metadata(), **kwargs,)


def born():
    kaa = Kaa()

    cmdclass = {
        name.lower(): command
        for name, command in utils.list_classes("kaa.viper", _subclass=Command)
    }

    entry_points = {
        group: [f"{name} = {path}" for name, path in entries.items()]
        for group, entries in setupcfg.load()["options.entry_points"].items()
    }
    entry_points["kaa.hooks"] = [
        hook.call()
        for name, hook in utils.list_classes(
            "kaa.viper.fangs", _subclass=viper.GitHook, _excludes=[viper.GitHook]
        )
    ]

    kaa.setup(cmdclass=cmdclass, entry_points=entry_points)
