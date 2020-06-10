from readme_generator import Readme
import shields
import setupcfg
from kaa import viper
from . import scales


class Parseltongue(type):
    def __new__(meta, name, bases, attr):
        """Meta description of class definition"""
        attr['order'] = [
            method
            for method in attr
            if not method.startswith('__')
            and method not in [
                'disabled', 'header_lvl', 'headers',
                'locations', 'order', 'sections'
            ]
        ]
        attr['headers'] = {strech: '' for strech in attr['order']}
        return super(Parseltongue, meta).__new__(meta, name, bases, attr)


class Section(Readme, metaclass=Parseltongue):
    def __call__(self):
        return self.render()


class Head(Section):
    def badges(self):
        return '\n'.join([
            shields.pypi.Pyversions('Kaa').md,
            scales.License('Kaa').md,
            shields.pypi.V("Kaa", color='blue').md,
        ])

    def introduction(self):
        return '\n'.join([
            setupcfg.get('metadata', 'reference'),
            viper.summary() + '\n',
            setupcfg.get('metadata', 'introduction'),
        ])

class Overview(Section):
    def purpose(self):
        return f"{setupcfg.get('metadata', 'overview')} Check [package description](DESCRIPTION.md#kaa) for more information and [examples](DESCRIPTION.md#Example)."


class Getting_Started(Section):
    def python_version(self):
        return f"""
        Make sure you have the corrected interpreter available:

        $ python3 --version
        python {viper.python_version()}

        """

    def pipy(self):
        return f"""
        Since, from this version, [pip](https://pip.pypa.io/en/stable/installing/) already comes together with Python, you'll be able to download package [latest release]({viper.pypi()}) available in PyPI:

        pip3 install {viper.name()}
        """
