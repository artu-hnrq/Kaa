# from pkg_resources import EntryPoint
import inspect


class entry_point(type):
    declared = {}

    def __new__(meta, name, bases=(), attr={}):
        attr["__init__"] = lambda s, o: None
        return super(entry_point, meta).__new__(meta, name, bases, attr)

    def __call__(cls, obj):
        cls.declare(
            "{} = {}:{}".format(obj.__name__.lower(), obj.__module__, obj.__qualname__,)
        )
        return super(entry_point, cls).__call__(obj)

    def declare(cls, entry):
        entry_point.declared.setdefault(cls.__name__, []).append(entry)
