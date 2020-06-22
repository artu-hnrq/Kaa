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
        __arrangement__ = attr.pop("__arrangement__", [])

        for name, loader in __arrangement__:
            assert isinstance(loader, ContextLoader) or issubclass(
                loader, ContextLoader
            )
            attr[loader.__name__.lower()] = fill_call(loader)

        return super(ContextLoader, meta).__new__(meta, name, bases, attr)

    def __run__(cls):
        load = {}
        for stage, procedure in cls.__stages__:
            try:
                for k, v in procedure(cls).items():
                    load.setdefault(k, v)
            except AttributeError:
                warnings.warn(
                    f"{cls.__name__} ContextLoader {stage} stage isn't returning a dictionary",
                    category=UserWarning,
                )
        return load

    @classmethod
    def fromModule(meta, module):
        class ModuleContext(metaclass=meta):
            __arrangement__ = library.list_classes(module, _instance=ContextLoader)

        return ModuleContext


class ContextComposer(ContextLoader):
    def __run__(cls):
        load = {}
        for stage, procedure in cls.__stages__:
            try:
                for k, v in procedure(cls).items():
                    load.setdefault(k, [])
                    load[k].append(v)
            except AttributeError:
                warnings.warn(
                    f"{cls.__name__} ContextLoader {stage} stage isn't returning a dictionary",
                    category=UserWarning,
                )
        return load


class ContextBuilder(ContextLoader):
    def __run__(cls):
        return {key: value(cls) for key, value in cls.__stages__}


class EntryPointContext(ContextBuilder):
    def __new__(meta, name, bases, attr):
        "Declares a method for each entry_points available for given group"

        try:
            group = attr.pop("group")
        except AttributeError:
            warnings.warn(
                f"__precedence__ is required to defining {self.__class__.__name__} CascadeLoader",
                category=UserWarning,
            )
            group = []

        for name, func in library.package_discovery(group).items():
            attr[name] = func

        return super(EntryPointContext, meta).__new__(meta, name, bases, attr)

    @classmethod
    def fromGroup(meta, group):
        return EntryPointContext.__new__(
            EntryPointContext, "Group", (), {"group": group}
        )


class CascadeLoader(ContextLoader):
    def __new__(meta, name, bases, attr):
        try:
            __precedence__ = attr.pop("__precedence__")
        except AttributeError:
            warnings.warn(
                f"__precedence__ is required to defining {self.__class__.__name__} CascadeLoader",
                category=UserWarning,
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
    def get_declareted_methods(meta, attr):
        def depurate(target, *restrictions):
            return {
                k: v
                for k, v in target.items()
                if all([restriction(k, v) for restriction in restrictions])
            }

        return depurate(
            attr, lambda k, v: not k.startswith("_"), lambda k, v: callable(v),
        )
