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
    gitconfig = cls.repository.config_reader("global")

    def author(cls):
        return cls.gitconfig.get("user", "name")

    def author_email(cls):
        email = cls.gitconfig.get("user", "email")
        return f"{cls.author(cls)} <{email}>"


class RepositoryInfo(_GitInfo):
    repository = git.Repo()

    def name(cls):
        return cls.url(cls).split("/")[1][:-4]

    def url(cls):
        return cls.repository.remote().url


class Source(metaclass=utils.ContextBuilder):
    def packages(cls):
        return setuptools.find_packages(where="src")

    def package_dir(cls):
        return {"": "src"}


class DeclaredLicense(metaclass=utils.ContextBuilder):
    def license(cls):
        return open("LICENSE").read().splitlines()[0]


class LibVersion(metaclass=utils.ContextBuilder):
    # TODO generalize it
    def version(cls):
        import kaa

        return kaa.__version__


class DescriptionFile(metaclass=utils.ContextBuilder):
    def long_description(cls):
        return open("DESCRIPTION.md").read()

    def long_description_content_type(cls):
        return "markdown"


class Envirionment(metaclass=utils.ContextBuilder):
    def platforms(cls):
        return "ANY"

    def python_requires(cls):
        return f">={platform.python_version()}"
