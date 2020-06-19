from .venom import *
from .fangs import GitHook
from .. import utils
import setuptools.command.build_py
from distutils import cmd


class Build_Py(setuptools.command.build_py.build_py):
    def run(self):
        for name, command in utils.list_classes(
            "kaa.viper.venom", _subclass=cmd.Command
        ):
            self.run_command(name.lower())
        setuptools.command.build_py.build_py.run(self)
