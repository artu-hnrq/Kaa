from .. import utils
import setuptools
import setupcfg
import platform
import yaml
import git
import os

"All ContextLoaders defined in this module are scaled to populate Kaa.metadata"


class Nest(metaclass=utils.CascadeLoader):
    __precedence__ = [".", os.environ["HOME"]]

    def cfg(path):
        return setupcfg.load(f"{path}/setup.cfg")["metadata"]

    def yml(path):
        data = {}
        try:
            with open(f"{path}/.kaa") as yml:
                data = yaml.safe_load(yml.read())["metadata"]
        except (FileNotFoundError, KeyError):
            return {}

        return data


class _GitInfo(metaclass=utils.ContextBuilder):
    repository = git.Repo()


class GitUserAuthor(_GitInfo):
    def __init__(self):
        self.gitconfig = self.repository.config_reader("global")

    def author(self):
        return self.gitconfig.get("user", "name")

    def author_email(self):
        email = self.gitconfig.get("user", "email")
        return f"{self.author()} <{email}>"


class RepositoryInfo(_GitInfo):
    def __init__(self):
        self.repository = git.Repo()

    def name(self):
        return self.url().split("/")[1][:-4]

    def url(self):
        return self.repository.remote().url


class Source(metaclass=utils.ContextBuilder):
    def packages(self):
        return setuptools.find_packages(where="src")

    def package_dir(self):
        return {"": "src"}


class DeclaredLicense(metaclass=utils.ContextBuilder):
    def license(self):
        return open("LICENSE").read().splitlines()[0]


class LibVersion(metaclass=utils.ContextBuilder):
    # TODO generalize it
    def version(self):
        import kaa

        return kaa.__version__


class DescriptionFile(metaclass=utils.ContextBuilder):
    def long_description(self):
        return open("DESCRIPTION.md").read()

    def long_description_content_type(self):
        return "markdown"


class Envirionment(metaclass=utils.ContextBuilder):
    def platforms(self):
        return "ANY"

    def python_requires(self):
        return f">={platform.python_version()}"
