import git
import setuptools
import os

HOME = os.environ['HOME']

def rattle():
	# Project
	repository = git.Repo()

	name = repository.description

	for line in open(f"src/kaa/__init__.py").read().splitlines():
		if line.startswith('__version__'):
			version = line.split('=')[1][1:].strip("'")

	# Author
	gitconfig = git.GitConfigParser(f"{HOME}/.gitconfig")

	author = gitconfig.get('user', 'name')
	author_email = f'"{author}" <{gitconfig.get("user", "email")}>'

	# Description
	summary = None
	long_description = open('DESCRIPTION.md').read()

	# License
	license = open('LICENSE').read().splitlines()[0]

	# Code
	packages = setuptools.find_packages(where = 'src')

	# Python version
	import platform



	return setuptools.setup(
		name = name,
		version = version,

		author = f"{author}",
		author_email = f'"{author}" <{author_email}>',

		long_description = long_description,
		long_description_content_type = 'text/markdown',

		license = license,
		# license_file = 'LICENSE',

		packages = packages,
		package_dir = {'': 'src'},

		python_requires = f">={platform.python_version()}",

		platforms = 'ANY',

		entry_points={
	        'console_scripts': [
	            'kaa = kaa.snake:rattle'
	        ],
	    },
	)

rattle()
