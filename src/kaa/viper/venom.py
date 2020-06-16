from .. import utils
from distutils import cmd
import os

class Attack(cmd.Command):
    description = 'Run all functions declared in the kaa.attack entry point group'
    user_options = []

    def initialize_options(self):
        self.fang = utils.package_discovery('kaa.attack')

    def finalize_options(self):
        pass

    def run(self):
        for key, func  in self.fang.items():
            print('kaa attack:', key)
            func()


class Shed(cmd.Command):
    description = 'Bump up package version'
    user_options = [
        ('bump=', 'b', 'version bump group'),
    ]

    def initialize_options(self):
        self.bump = 'build'

    def finalize_options(self):
        assert self.bump in [
            'major', 'minor', 'patch', 'build'
        ]

    def run(self):
        os.system(' '.join([
            "bumpversion",
            "--allow-dirty",
            self.bump,
        ]))
