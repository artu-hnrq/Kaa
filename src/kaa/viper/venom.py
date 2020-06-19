from .. import utils
from distutils import cmd
import os


class Attack(cmd.Command):
    description = "Run all functions declared in the kaa.attack entry point group"
    user_options = []

    def initialize_options(self):
        self.fang = utils.package_discovery("kaa.attack")

    def finalize_options(self):
        pass

    def run(self):
        for key, func in self.fang.items():
            print("kaa attack:", key)
            func()


class Shed(cmd.Command):
    description = "Bump up package version"
    user_options = [
        ("bump=", "b", "version bump group"),
    ]

    def initialize_options(self):
        self.bump = "BUILD"

    def finalize_options(self):
        assert self.bump in [
            "MAJOR",
            "MINOR",
            "PATCH",
            "BUILD",
        ]

    def run(self):
        os.system(" ".join(["bumpversion", "--allow-dirty", self.bump,]))


import textwrap
import pkg_resources as pkg


class Init(cmd.Command):
    description = "Setup Kaa's packing repository"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for name, module, attrs in [
            (hook.name, hook.module_name, hook.attrs)
            for hook in pkg.iter_entry_points("kaa.hooks")
        ]:
            filename = f".git/hooks/{name}"
            with open(filename, "w") as hook:
                attrs = ".".join(attrs)
                hook.write(
                    textwrap.dedent(
                        f"""\
                    #!/usr/bin/python3
                    # EASY-INSTALL-ENTRY-SCRIPT: 'kaa','kaa.hooks','kaa'
                    __requires__ = 'kaa'
                    import re
                    import sys
                    from pkg_resources import load_entry_point

                    if __name__ == '__main__':
                        sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
                        sys.exit(
                            load_entry_point('kaa', 'kaa.hooks', '{name}')()
                        )

                    """
                    )
                )
            os.system(f"chmod +x {filename}")
