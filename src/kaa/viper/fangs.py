from .. import utils
import commitizen as ctz
from commitizen import bump
from commitizen.defaults import bump_map, bump_pattern
import git
import sys
import os


class GitHook(metaclass=utils.Methodology):
    @classmethod
    def entry_name(cls):
        return cls.__name__.lower().replace("_", "-")

    @classmethod
    def call(cls):
        name = cls.__name__
        return f"{cls.entry_name()} = kaa.viper.fangs:{name}.run"


class Commit_Msg(GitHook):
    def bump_version_accordingly(self):
        commit_msg = open(sys.argv[1]).read()
        commit = ctz.git.GitCommit(rev="", title=commit_msg)
        increment = bump.find_increment([commit], bump_pattern, bump_map)

        if increment:
            os.system(f"kaa shed -b {increment}")
            open(".commit", "w")


class Post_Commit(GitHook):
    def add_remaining(self):
        if os.path.isfile(".commit"):
            os.remove(".commit")

            repo = git.Repo()
            unstaged = repo.index.diff(None)

            if unstaged:
                repo.git.add(*[diff.a_path for diff in unstaged])
                repo.git.commit("--amend", "-C", "HEAD", "--no-verify")
