from .. import utils
from readme_generator import Readme



def flick():
    parselmouth = Parselmouth()
    parselmouth.write("README.md", 'head', 'overview', 'getting_started')
    parselmouth.write("DESCRIPTION.md", 'head')


class Parselmouth(Readme):
    sections = {
        name: section()()
        for name, section
        in utils.package_discovery('kaa.sections').items()
    }
    headers = {'head': 'Kaa'}
    header_lvl = 2
    locations = ['.']

    def write(self, filename, *words):
        self.order = words
        self.save(filename)
