from .check import strangled
from .switch import *


def check_use(use):
    assert use in [OLD_ONLY, NEW_TEST, OLD_MAIN, NEW_MAIN, NEW_ONLY]


def check_getter(getter):
    getter is None or check_use(getter)


def check_setter(setter):
    setter is None or check_use(setter)


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
                    def __call__(self, obj):
                        self.args = args
                        self.kwargs = kwargs
                        return getattr(obj, name)(*args, **kwargs)

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
                def __call__(self, obj):
                    self.args = []
                    self.kwargs = {}
                    return getattr(obj, name)
            return strangled_f(cls, name, getter, target, Functor())

        def set_value(target, value):
            class Functor:
                def __call__(self, obj):
                    self.args = [value]
                    self.kwargs = {}
                    setattr(obj, name, value)
            return strangled_f(cls, name, setter, target, Functor())

        setattr(cls, name, property(fget=get_value, fset=set_value if setter else None))
        return cls

    return decorator


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _strangled_eq(*, use):

    def decorator(cls):
        def checked_eq(lhs, rhs):
            class Old:
                def __call__(self):
                    self.args = []
                    self.kwargs = {}
                    return lhs.old == rhs.old

                def _repr(self):
                    return repr(lhs.old)

            class New:
                def __call__(self):
                    self.args = []
                    self.kwargs = {}
                    return lhs.new == rhs.new

                def _repr(self):
                    return repr(lhs.new)

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
                def __call__(self):
                    self.args = []
                    self.kwargs = {}
                    return iter(IterFor(data, "old"))

                def _repr(self):
                    return repr(target.old)

            class New:
                def __call__(self):
                    self.args = []
                    self.kwargs = {}
                    return iter(IterFor(data, "new"))

                def _repr(self):
                    return repr(target.new)

            return strangled(cls, '__iter__', use, Old(), New())

        setattr(cls, '__iter__', checked_iter)
        return cls

    return decorator


class IterFor:
    def __init__(self, data, oa):
        self.data = data
        self.oa = oa
        self.old_index = 0
        self.new_index = 0

    def __eq__(self, other):
        return isinstance(other, IterFor) and \
            self.data.target is other.data.target and \
            sorted(self.data.old_ids) == sorted(self.data.new_ids)

    def __iter__(self):
        return self

    def __str__(self):
        assert self.oa in ["old", "new"]
        if self.oa == "old":
            return f"{self.data.old_ids}"
        else:
            return f"{self.data.new_ids}"

    def __next__(self):
        assert self.oa in ["old", "new"]
        if self.oa == "old":
            return self._next_old()
        else:
            return self._next_new()

    def _next_old(self):
        if self.old_index < len(self.data.old):
            result = self.data.old[self.old_index]
            self.old_index += 1
            return result
        else:
            raise StopIteration

    def _next_new(self):
        if self.new_index < len(self.data.new):
            result = self.data.new[self.new_index]
            self.new_index += 1
            return result
        else:
            raise StopIteration


class IterData:
    """
    Relies on the target having an inner_id property.
    Probably not needed if the iterated objects have
    __eq__ but good enough, and all I could think of
    at the time.
    """

    def __init__(self, target, use):
        from model import EnvironmentEvents
        self.target = target
        if old_is_on(target, use):
            self.old_ids = []
            self.old = []
            for c in target.old:
                self.old.append(c)
                if hasattr(c, 'inner_id'):
                    self.old_ids.append(c.inner_id)
                elif isinstance(target, EnvironmentEvents):
                    self.old_ids.append("Fake")
                else:
                    self.old_ids.append(c['inner_id'])  # allowlist

        if new_is_on(target, use):
            self.new_ids = []
            self.new = []
            for m in target.new:
                self.new.append(m)
                if hasattr(m, 'inner_id'):
                    self.new_ids.append(m.inner_id)
                elif isinstance(target, EnvironmentEvents):
                    self.new_ids.append("Fake")
                else:
                    self.new_ids.append(m['inner_id'])  # allowlist


def strangled_f(cls, name, use, obj, f):

    class Old:
        def __call__(self):
            result = f(obj.old)
            self.args = f.args
            self.kwargs = f.kwargs
            return result

        def _repr(self):
            return repr(obj.old)

    class New:
        def __call__(self):
            result = f(obj.new)
            self.args = f.args
            self.kwargs = f.kwargs
            return result

        def _repr(self):
            return repr(obj.new)

    return strangled(cls, name, use, Old(), New())
