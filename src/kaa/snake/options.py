from .. import utils
from .. import viper
from distutils.cmd import Command
import setupcfg
import yaml
import os

"All ContextLoaders defined in this module are passed as keyword arguments to Kaa.setup"


class _Nest(metaclass=utils.CascadeLoader):
    __precedence__ = ["./", os.environ["HOME"]]

    def cfg(path):
        return {
            group: [f"{name} = {path}" for name, path in entries.items()]
            for group, entries in setupcfg.load(f"{path}/setup.cfg")[
                "options.entry_points"
            ].items()
        }

    def yml(path):
        data = {}
        try:
            with open(f"{path}/.kaa") as yml:
                data = yaml.safe_load(yml.read())["options"]["entry_points"]
        except (FileNotFoundError, KeyError):
            return {}

        return data


class Entry_Points(metaclass=utils.ContextLoader):
    def nest(self):
        return _Nest.load()

    def hooks(self):
        return {
            "kaa.hooks": [
                hook.call()
                for name, hook in utils.list_classes(
                    "kaa.viper.fangs",
                    _subclass=viper.GitHook,
                    _excludes=[viper.GitHook],
                )
            ]
        }

    # TODO Automatize declared kaa.wisdom entry_points from kaa.snake module
    def wisdom(self):
        return {
            "kaa.wisdom": [
                # hook.call()
                # for name, hook in utils.list_classes(
                #     "kaa.snake",
                #     _subclass=viper.GitHook,
                #     _excludes=[viper.GitHook]
                # )
            ]
        }


class CmdClass(metaclass=utils.ContextLoader):
    def declared(self):
        return {
            name.lower(): command
            for name, command in utils.list_classes("kaa.viper", _subclass=Command)
        }
