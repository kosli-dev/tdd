"""
The strangler decorators control Old/New at the
individual method/property level via keyword arguments:
      Method: (..., *, use)
  Properties: (..., *, getter, setter)

use/getter/setter are Tuples with 3 elements
  [0] controls if the Old call is made
  [1] controls if the New call is made
  [2] controls which is 'main' if Old _and_ New calls are being made:

if Old/New calls exhibit _different_ behaviour
  if running-unit-tests:
      raise StrangledDifference(...)
  else:
      log difference to a file

On staging and production, while strangling is in progress
differences are logged to a file, they do NOT raise an exception.
However, inside unit-tests, differences do raise an exception.
"""

# Steps in moving from Old to New...

OLD_ONLY = (True, False, "old")  # 1st - Old call only, returns Old
OLD_MAIN = (True, True, "old")   # 2nd - both called, returns Old
NEW_MAIN = (True, True, "new")   # 3rd - both called, returns New
NEW_ONLY = (False, True, "new")  # 4th - New call only, returns New


def switches():
    return [OLD_ONLY, OLD_MAIN, NEW_ONLY, NEW_MAIN]


def call_old(use):
    return use[0]


def call_new(use):
    return use[1]


def call_both(use):
    return call_old(use) and call_new(use)


def old_is_primary(use):
    return _primary_is(use, 'old')


def new_is_primary(use):
    return _primary_is(use, 'new')


def _primary_is(use, age):
    return use[2] == age
