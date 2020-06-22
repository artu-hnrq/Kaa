import pkg_resources as pkg


def package_discovery(entry_point_group):
    "Return {name: func} for each entry point in the given group"

    return {
        entry_point.name: entry_point.load()
        for entry_point in pkg.iter_entry_points(entry_point_group)
    }


import inspect
import sys


def list_classes(module, *filters, _instance=None, _subclass=None, _excludes=None):
    filters = [
        lambda cls: inspect.isclass(cls),
        lambda cls: not cls.__name__.startswith("_"),
        lambda cls: not _instance or isinstance(cls, _instance),
        lambda cls: not _subclass or issubclass(cls, _subclass),
        lambda cls: not _excludes or cls not in _excludes,
    ] + list(filters)

    return inspect.getmembers(
        sys.modules[module], lambda cls: all(filter(cls) for filter in filters)
    )
