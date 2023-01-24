from .strangled import strangled
from .switch import *


def strangled_method(name, *, use):
    check_use(use)

    if name == "__eq__":
        return _strangled_eq(use=use)
    elif name == "__iter__":
        return _strangled_iter(use=use)
    else:
        def decorator(cls):
            def func(target, *args, **kwargs):
                class Functor:
                    def __init__(self):
                        self.args = args
                        self.kwargs = kwargs

                    def __call__(self, obj):
                        f = getattr(obj, name)
                        return f(*args, **kwargs)

                return strangled_f(cls, name, use, target, Functor())

            setattr(cls, name, func)
            return cls

        return decorator


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def strangled_property(name, *, getter, setter):
    check_getter(getter)
    check_setter(setter)

    def decorator(cls):
        def get_value(target):
            class Functor:
                def __init__(self):
                    self.args = []
                    self.kwargs = {}

                def __call__(self, obj):
                    return getattr(obj, name)
            return strangled_f(cls, name, getter, target, Functor())

        def set_value(target, value):
            class Functor:
                def __init__(self):
                    self.args = [value]
                    self.kwargs = {}

                def __call__(self, obj):
                    setattr(obj, name, value)
            return strangled_f(cls, name, setter, target, Functor())

        setattr(cls, name, property(fget=get_value, fset=set_value if setter else None))
        return cls

    return decorator

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def strangled_f(cls, name, use, obj, f):

    class Old:
        def __init__(self):
            self.args = f.args
            self.kwargs = f.kwargs

        def __repr__(self):
            return repr(obj.old)

        def __call__(self):
            return f(obj.old)

    class New:
        def __init__(self):
            self.args = f.args
            self.kwargs = f.kwargs

        def __repr__(self):
            return repr(obj.new)

        def __call__(self):
            return f(obj.new)

    return strangled(cls, name, use, Old(), New())

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def _strangled_eq(*, use):

    def decorator(cls):
        def checked_eq(lhs, rhs):
            class Old:
                def __init__(self):
                    self.args = []
                    self.kwargs = {}

                def __repr__(self):
                    return repr(lhs.old)

                def __call__(self):
                    return lhs.old == rhs.old

            class New:
                def __init__(self):
                    self.args = []
                    self.kwargs = {}

                def __repr__(self):
                    return repr(lhs.new)

                def __call__(self):
                    return lhs.new == rhs.new

            return strangled(cls, '__eq__', use, Old(), New())

        setattr(cls, '__eq__', checked_eq)
        return cls

    return decorator


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _strangled_iter(*, use):

    def decorator(cls):
        def checked_iter(target):
            data = IterData(target, use)

            class Old:
                def __init__(self):
                    self.args = []
                    self.kwargs = {}

                def __repr__(self):
                    return repr(target.old)

                def __call__(self):
                    return IterFor(data, data.old)

            class New:
                def __init__(self):
                    self.args = []
                    self.kwargs = {}

                def __repr__(self):
                    return repr(target.new)

                def __call__(self):
                    return IterFor(data, data.new)

            return strangled(cls, '__iter__', use, Old(), New())

        setattr(cls, '__iter__', checked_iter)
        return cls

    return decorator


class IterFor:
    def __init__(self, data, seq):
        self.data = data
        self.index = -1
        self.seq = seq

    def __eq__(self, other):
        return isinstance(other, IterFor) \
               and self.data.old == self.data.new

    def __repr__(self):
        return f"{self.seq}"

    def __next__(self):
        self.index += 1
        if self.index < len(self.seq):
            return self.seq[self.index]
        else:
            raise StopIteration


class IterData:

    def __init__(self, target, use):
        if old_is_on(target, use):
            self.old = [obj for obj in target.old]
        if new_is_on(target, use):
            self.new = [obj for obj in target.new]


def check_use(use):
    assert use in [OLD_ONLY, OLD_MAIN, NEW_MAIN, NEW_ONLY]


def check_getter(getter):
    getter is None or check_use(getter)


def check_setter(setter):
    setter is None or check_use(setter)
