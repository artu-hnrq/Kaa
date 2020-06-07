import setuptools

setuptools.setup(
    name = 'kaa',
    version = '0.0.1',

    install_requires = [
        'pip >= 20.1.1',
        'setuptools >= 47.1.1',
        'wheel >= 0.34.2',
        'twine >= 3.1.1'
    ],

    python_requires = '>=3.8.2',

    entry_points={
        'console_scripts': [
            'kaa = kaa.snake:rattle'
        ],
    },

    packages = setuptools.find_packages(where = 'src'),
    package_dir = {'': 'src'},
)
