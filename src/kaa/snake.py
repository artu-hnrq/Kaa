import git
import setuptools
import os

HOME = os.environ['HOME']

def rattle():
	gitconfig = git.GitConfigParser(f"{HOME}/.gitconfig")

	name = gitconfig.get('user', 'name')
	email = gitconfig.get('user', 'email')

	return setuptools.setup(
		author = f"{name}",
		author_email = f'"{name}" <{email}>',

		entry_points={
	        'console_scripts': [
	            'kaa = kaa.snake:rattle'
	        ],
	    },
	)

rattle()
