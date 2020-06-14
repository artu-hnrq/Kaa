from .. import utils
import setuptools.command.build_py
from distutils.cmd import Command


class BuildPyCommand(setuptools.command.build_py.build_py):
    def run(self):
        self.run_command('attack')
        setuptools.command.build_py.build_py.run(self)


class Attack(Command):
    # description = 'run Pylint on Python source files'
    user_options = [
      # The format is (long option, short option, description).
    ]

    def initialize_options(self):
        self.fang = utils.package_discovery('kaa.attack')

    def finalize_options(self):
        pass

    def run(self):
        for key, func  in self.fang.items():
            print('kaa attack:', key)
            func()
