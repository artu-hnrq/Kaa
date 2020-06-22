import inspect


class Methodology(type):
    def __new__(meta, name, bases, attr, __func__="__call__"):
        "Overwrites a target method to behave calling all class declareted methods orderly"

        attr[__func__] = meta.__run__
        return super(Methodology, meta).__new__(meta, name, bases, attr)

    @property
    def __stages__(cls):
        __stages__ = inspect.getmembers(
            cls,
            lambda member: inspect.isfunction(member)
            and not member.__name__.startswith("_"),
        )
        __stages__.reverse()
        return __stages__

    def __run__(self, *args, **kwargs):
        for stage, procedure in self.__stages__:
            procedure(self, *args, **kwargs)

    def __call__(cls):
        return cls.__run__()
