#!/usr/bin/python3
import python_readme_generator
import shields

# TODO: Generalize github user, repository and branch
class License(shields.Abstract):
    __readme__ = []
    name = None
    path = "github/license/artu-hnrq/{name}.svg"
    link = "https://github.com/artu-hnrq/{name}/blob/jungle/LICENSE"

    def __init__(self, name, **kwargs):
        self.name = name
        self.update(kwargs)
