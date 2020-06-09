import setuptools
import setuptools.command.build_py
import distutils
import git
import os
from . import utils


setup = {
    attr: func()
    for attr, func
    in utils.package_discovery('kaa.defaults').items()
}

def rattle():
	return setuptools.setup(
		**setup,

		cmdclass={
            'build_py': BuildPyCommand,
            'venom': VenomCommand,
        }

	)

class BuildPyCommand(setuptools.command.build_py.build_py):
    def run(self):
        self.run_command('venom')
        setuptools.command.build_py.build_py.run(self)


class VenomCommand(distutils.cmd.Command):
    # description = 'run Pylint on Python source files'
    user_options = [
      # The format is (long option, short option, description).
    ]

    def initialize_options(self):
        self.venom = utils.package_discovery('kaa.venom')

    def finalize_options(self):
        pass

    def run(self):
        for key, func  in self.venom.items():
            print('running venom:', key)
            func()
