def depurate(target, *restrictions):
    return {
        k: v for k, v
        in target.items()
        if all([
            restriction(k, v)
            for restriction
            in restrictions
        ])
    }

class Methodology(type):

    def __new__(meta, name, bases, attr, __func__='__call__'):
        "Overwrites a target method to behave calling all class declareted methods orderly"

        __stages__ =  meta.get_declareted_methods(attr)
        attr['__stages__'] = property(lambda self: __stages__)
        attr[__func__] = meta.__run__

        return super(Methodology, meta).__new__(meta, name, bases, attr)

    def __run__(self, *args, **kwargs):
        for stage, procedure in self.__stages__.items():
            procedure(self, *args, **kwargs)

    @classmethod
    def get_declareted_methods(meta, attr):
        return depurate(attr,
            lambda k, v: not k.startswith('_'),
            lambda k, v: callable(v),
        )
