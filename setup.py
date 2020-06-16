#!/user/bin/python3
import setuptools

setuptools.setup(
    name = 'kaa',
    version = '0.0.0',

    python_requires = '>=3.8.2',

    packages = setuptools.find_packages(where = 'src'),
    package_dir = {'': 'src'},
)
