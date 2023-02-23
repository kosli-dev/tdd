from .strangled import strangled
from .switch import *


def strangled_method(name, *, use):
    check_use(use)

    if name == "__eq__":
        return strangled_eq(use=use)
    elif name == "__iter__":
        return strangled_iter(use=use)
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
    check_prop(getter)
    check_prop(setter)

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

    class Call:
        def __init__(self, age):
            self.age = age
            self.args = f.args
            self.kwargs = f.kwargs

        def __repr__(self):
            return repr(self._target())

        def __call__(self):
            return f(self._target())

        def _target(self):
            return getattr(obj, self.age)

    return strangled(cls, name, use, Call('old'), Call('new'))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def strangled_eq(*, use):

    def decorator(cls):
        def checked_eq(lhs, rhs):

            class Call:
                def __init__(self, age):
                    self.age = age
                    self.args = []
                    self.kwargs = {}

                def __repr__(self):
                    return repr(self._target(lhs))

                def __call__(self):
                    return self._target(lhs) == self._target(rhs)

                def _target(self, side):
                    return getattr(side, self.age)

            return strangled(cls, '__eq__', use, Call('old'), Call('new'))

        setattr(cls, '__eq__', checked_eq)
        return cls

    return decorator


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def strangled_iter(*, use):

    def decorator(cls):
        def checked_iter(target):
            data = IterData(target, use)

            class Call:
                def __init__(self, age):
                    self.age = age
                    self.args = []
                    self.kwargs = {}

                def __repr__(self):
                    return repr(getattr(target, self.age))

                def __call__(self):
                    return IterFor(data, getattr(data, self.age))

            return strangled(cls, '__iter__', use, Call('old'), Call('new'))

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
        if call_old(use):
            self.old = [obj for obj in target.old]
        if call_new(use):
            self.new = [obj for obj in target.new]


def check_use(use):
    assert use in switches()


def check_prop(prop):
    prop is None or check_use(prop)
