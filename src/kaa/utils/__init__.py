from .meta import *
from .library import *


class entry_point:
    def __init__(self, obj, *, method=None, group='console_scripts'):
        self.obj = obj

    def __call__(self):
        print(self.obj.__module__)
