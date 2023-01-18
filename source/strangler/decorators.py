from lib import contract_check
from .contract_check_switch import *


def check_kind(kind):
    assert kind in ["create", "command", "query"]


def check_use(use):
    assert use in [OVERWRITE_ONLY, APPEND_TEST, OVERWRITE_MAIN, APPEND_MAIN, APPEND_ONLY]


def check_getter(getter):
    getter is None or check_use(getter)


def check_setter(setter):
    setter is None or check_use(setter)

# - - - - - - - - - - - - - - - -
# Code below contains sections for turning off
# contract checking when use/getter/setter is APPEND_ONLY
# It is commented out as it causes a single integration-test failure
# of test_1f213cc2 ??? To repeat this failure --random-order-seed=139390
# ...14th Jan 2023...
# This failure no longer occurs so the sections mentioned are now
# commented out.


def contract_checked_method(name, *, use, kind):
    check_use(use)
    check_kind(kind)

    if name == "__eq__":
        return _contract_checked_eq(use=use)
    elif name == "__iter__":
        return _contract_checked_iter(use=use)
    # elif use is APPEND_ONLY:
    #     def decorator(cls):
    #         def func(target, *args, **kwargs):
    #             result = getattr(target.append, name)(*args, **kwargs)
    #             if kind != "query":
    #                 target.append._reset(name)
    #             return result
    #         setattr(cls, name, func)
    #         return cls
    else:
        def decorator(cls):
            def func(target, *args, **kwargs):
                class Functor:
                    def __call__(self, obj):
                        self.args = args
                        self.kwargs = kwargs
                        return getattr(obj, name)(*args, **kwargs)

                return contract_check_f(cls, name, kind, use, target, Functor())

            setattr(cls, name, func)
            return cls

        return decorator


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def contract_checked_property(name, *, getter, setter):
    check_getter(getter)
    check_setter(setter)

    # if getter is APPEND_ONLY and (setter is None or setter is APPEND_ONLY):
    #     def decorator(cls):
    #         def get_value(target):
    #             return getattr(target.append, name)
    #
    #         def set_value(target, value):
    #             setattr(target.append, name, value)
    #             target.append._reset()
    #         setattr(cls, name, property(fget=get_value, fset=set_value if setter else None))
    #         return cls
    # else:

    def decorator(cls):
        def get_value(target):
            class Functor:
                def __call__(self, obj):
                    self.args = []
                    self.kwargs = {}
                    return getattr(obj, name)
            return contract_check_f(cls, name, "query", getter, target, Functor())

        def set_value(target, value):
            class Functor:
                def __call__(self, obj):
                    self.args = [value]
                    self.kwargs = {}
                    setattr(obj, name, value)
            return contract_check_f(cls, name, "command", setter, target, Functor())

        setattr(cls, name, property(fget=get_value, fset=set_value if setter else None))
        return cls

    return decorator


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _contract_checked_eq(*, use):

    # if use is APPEND_ONLY:
    #     def decorator(cls):
    #         def checked_eq(lhs, rhs):
    #             return lhs.append == rhs.append
    #         setattr(cls, '__eq__', checked_eq)
    #         return cls
    # else:

    def decorator(cls):
        def checked_eq(lhs, rhs):
            class OW:
                def __call__(self):
                    self.args = []
                    self.kwargs = {}
                    return lhs.overwrite == rhs.overwrite

                def _repr(self):
                    return repr(lhs.overwrite)

            class AO:
                def __call__(self):
                    self.args = []
                    self.kwargs = {}
                    return lhs.append == rhs.append

                def _repr(self):
                    return repr(lhs.append)

            return contract_check(cls, '__eq__', "query", use, OW(), AO())

        setattr(cls, '__eq__', checked_eq)
        return cls

    return decorator


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _contract_checked_iter(*, use):

    # if use is APPEND_ONLY:
    #     def decorator(cls):
    #         def unchecked_iter(target):
    #             return iter(target.append)
    #
    #         setattr(cls, '__iter__', unchecked_iter)
    #         return cls
    # else:

    def decorator(cls):
        def checked_iter(target):
            data = IterData(target, use)

            class OW:
                def __call__(self):
                    self.args = []
                    self.kwargs = {}
                    return iter(IterFor(data, "overwrite"))

                def _repr(self):
                    return repr(target.overwrite)

            class AO:
                def __call__(self):
                    self.args = []
                    self.kwargs = {}
                    return iter(IterFor(data, "append"))

                def _repr(self):
                    return repr(target.append)

            return contract_check(cls, '__iter__', "query", use, OW(), AO())

        setattr(cls, '__iter__', checked_iter)
        return cls

    return decorator


class IterFor:
    def __init__(self, data, oa):
        self.data = data
        self.oa = oa
        self.overwrite_index = 0
        self.append_index = 0

    def __eq__(self, other):
        return isinstance(other, IterFor) and \
            self.data.target is other.data.target and \
            sorted(self.data.overwrite_ids) == sorted(self.data.append_ids)

    def __iter__(self):
        return self

    def __str__(self):
        assert self.oa in ["overwrite", "append"]
        if self.oa == "overwrite":
            return f"{self.data.overwrite_ids}"
        else:
            return f"{self.data.append_ids}"

    def __next__(self):
        assert self.oa in ["overwrite", "append"]
        if self.oa == "overwrite":
            return self._next_overwrite()
        else:
            return self._next_append()

    def _next_overwrite(self):
        if self.overwrite_index < len(self.data.overwrite):
            result = self.data.overwrite[self.overwrite_index]
            self.overwrite_index += 1
            return result
        else:
            raise StopIteration

    def _next_append(self):
        if self.append_index < len(self.data.append):
            result = self.data.append[self.append_index]
            self.append_index += 1
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
        if overwrite_is_on(target, use):
            self.overwrite_ids = []
            self.overwrite = []
            for c in target.overwrite:
                self.overwrite.append(c)
                if hasattr(c, 'inner_id'):
                    self.overwrite_ids.append(c.inner_id)
                elif isinstance(target, EnvironmentEvents):
                    self.overwrite_ids.append("Fake")
                else:
                    self.overwrite_ids.append(c['inner_id'])  # allowlist

        if append_is_on(target, use):
            self.append_ids = []
            self.append = []
            for m in target.append:
                self.append.append(m)
                if hasattr(m, 'inner_id'):
                    self.append_ids.append(m.inner_id)
                elif isinstance(target, EnvironmentEvents):
                    self.append_ids.append("Fake")
                else:
                    self.append_ids.append(m['inner_id'])  # allowlist


def contract_check_f(cls, name, kind, use, obj, f):

    class OW:
        def __call__(self):
            result = f(obj.overwrite)
            self.args = f.args
            self.kwargs = f.kwargs
            return result

        @staticmethod
        def _reset():
            obj.overwrite._reset()

        def _repr(self):
            return repr(obj.overwrite)

    class AO:
        def __call__(self):
            result = f(obj.append)
            self.args = f.args
            self.kwargs = f.kwargs
            return result

        @staticmethod
        def _reset():
            obj.append._reset()

        def _repr(self):
            return repr(obj.append)

    return contract_check(cls, name, kind, use, OW(), AO())
