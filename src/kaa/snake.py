import git
import setuptools
import os
import pkg_resources as pkg



setup = {
    entry_point.name: entry_point.load()()
    for entry_point
    in pkg.iter_entry_points('kaa.defaults')
}

print(setup)

def rattle():

	return setuptools.setup(
		**setup,

		entry_points={
	        'console_scripts': [
	            'kaa = kaa.snake:rattle'
	        ],

			'kaa.defaults': [
				'name = kaa.viper:name',
				'version = kaa.viper:version',
				'description = kaa.viper:summary',
				'long_description = kaa.viper:description',
				'long_description_content_type = kaa.viper:description_type',
				'license = kaa.viper:license',
				'platforms = kaa.viper:any_platform',
				'author = kaa.viper:author',
				'author_email = kaa.viper:email',
				'url = kaa.viper:repository_url',
				'python_requires = kaa.viper:python_version',
				'packages = kaa.viper:packages',
				'package_dir = kaa.viper:package_dir',
			]
	    }

	)

rattle()
