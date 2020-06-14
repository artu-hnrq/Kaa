from . import scales
from .. import Kaa
from readme_generator import Readme
import shields
import setupcfg


class Parseltongue(type):
    vocabulary = Kaa().vocabulary()

    def __new__(meta, name, bases, attr):

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
        attr['vocabulary'] = meta.vocabulary
        return super(Parseltongue, meta).__new__(meta, name, bases, attr)


class Section(Readme, metaclass=Parseltongue):
    def __call__(self):
        return self.render()

    def get_section(self, name):
       return super(Section, self).get_section(name).format(**self.vocabulary)


class Head(Section):
    def badges(self):
        return '\n'.join([
            shields.pypi.Pyversions('Kaa').md,
            scales.License('Kaa').md,
            shields.pypi.V("Kaa", color='blue').md,
        ])

    def introduction(self):
        return "{reference}. {description} \n\n {introduction}"

class Overview(Section):
    def purpose(self):
        return "{overview} Check [package description](DESCRIPTION.md#{name}) for more information and [examples](DESCRIPTION.md#Example)."


class Getting_Started(Section):
    def python_version(self):
        return """
        Make sure you have the corrected interpreter available:

        $ python3 --version
        python {python_requires}

        """

    def pipy(self):
        return """
        Since, from this version, [pip](https://pip.pypa.io/en/stable/installing/) already comes together with Python, you'll be able to download package [latest release]({pypi}) available in PyPI:

        pip3 install {name}
        """
