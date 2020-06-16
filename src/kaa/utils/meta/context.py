from .methodology import Methodology
from .. import library
import itertools
import warnings

import inspect
import sys

def fill_call(func, *args, **kwargs):
    return lambda self: func(*args, **kwargs)

class ContextLoader(Methodology):
    def __new__(meta, name, bases, attr):
        __arrangement__ = attr.pop('__arrangement__', [])

        attr['load'] = classmethod(meta.load)

        for name, loader in __arrangement__:
            assert isinstance(loader, ContextLoader) \
                or issubclass(loader, ContextLoader)
            attr[loader.__name__] = fill_call(loader.load)

        return super(ContextLoader, meta).__new__(meta, name, bases, attr)

    def __run__(self):
        load = {}
        for stage, procedure in self.__stages__.items():
            try:
                for k, v in procedure(self).items():
                    load.setdefault(k, v)
            except AttributeError:
                warnings.warn(
                    f"{self.__class__.__name__} ContextLoader {stage} stage isn't returning a dictionary",
                    category = UserWarning
                )

        return load

    def load(cls):
        return cls()()

    @classmethod
    def fromModule(meta, module):
        class ModuleContext(metaclass=ContextLoader):
            __arrangement__ = library.list_classes(
                module, _instance = ContextLoader
            )

        return ModuleContext


class ContextBuilder(ContextLoader):
    def __run__(self):
        return {
            key: value(self)
            for key, value
            in self.__stages__.items()
        }

class EntryPointContext(ContextBuilder):
    def __new__(meta, name, bases, attr):
        "Declares a method for each entry_points available for given group"

        try:
            group = attr.pop('group')
        except AttributeError:
            warnings.warn(
                f"__precedence__ is required to defining {self.__class__.__name__} CascadeLoader",
                category = UserWarning
            )
            group = []

        for name, func in library.package_discovery(group).items():
            attr[name] = func

        return super(EntryPointContext, meta).__new__(meta, name, bases, attr)

    @classmethod
    def fromGroup(meta, group):
        return EntryPointContext.__new__(
            EntryPointContext, 'Group', (), {'group': 'kaa.defaults'}
        )

class CascadeLoader(ContextLoader):
    def __new__(meta, name, bases, attr):
        "Overwrites a target method to behave calling all class declareted methods orderly"

        try:
            __precedence__ = attr.pop('__precedence__')
        except AttributeError:
            warnings.warn(
                f"__precedence__ is required to defining {self.__class__.__name__} CascadeLoader",
                category = UserWarning
            )
            __precedence__ = []

        methods = meta.get_declareted_methods(attr)
        for i, [path, (stage, procedure)] in enumerate(
            itertools.product(__precedence__, methods.items())
        ):
            attr[f"{stage}{i}"] = fill_call(procedure, path)
            attr.pop(stage, None)

        return super(CascadeLoader, meta).__new__(meta, name, bases, attr)

    @classmethod
    def loader(*precedence, _load):
        class Loader(metaclass=CascadeLoader):
            __precedence__ = precedence
            load = _load

        return Loader
