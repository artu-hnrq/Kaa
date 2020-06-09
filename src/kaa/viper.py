import setuptools
import platform
import git

repository = git.Repo()

# Name
def name():
	return repository_url().split('/')[1][:-4]

# Version
def version():
    for line in open(f"src/kaa/__init__.py").read().splitlines():
        if line.startswith('__version__'):
            version = line.split('=')[1][1:].strip("'")
            return version


# Description
def summary():
    return None

def description():
    return open('DESCRIPTION.md').read()

def description_type():
	return 'markdown'

# License
def license():
	return open("LICENSE").read().splitlines()[0]

# Platform
def any_platform():
    return 'ANY'

# Author
gitconfig = repository.config_reader('global')

def author():
    return gitconfig.get('user', 'name')

def email():
    return f'"{author()}" <{gitconfig.get("user", "email")}>'

# URL
def repository_url():
    return repository.remote().url

# Requires
def python_version():
    return f">={platform.python_version()}"

# Packages
def packages():
    return setuptools.find_packages(where = 'src')

def package_dir():
    return {'': 'src'}
