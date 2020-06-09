import setuptools

setuptools.setup(
    name = 'kaa',
    version = '0.0.0',

    install_requires = [
        'pip >= 20.1.1',
        'setuptools >= 47.1.1',
        'wheel >= 0.34.2',
        'twine >= 3.1.1',

        'GitPython >= 3.1.3',
    ],

    python_requires = '>=3.8.2',

    packages = setuptools.find_packages(where = 'src'),
    package_dir = {'': 'src'},

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
        ],
    },
)
