"""
The strangler decorators control Old/New at the
individual method/property level via keyword arguments:
      Method: (..., *, use)
  Properties: (..., *, getter, setter)

use/getter/setter are Tuples with 3 elements
  [0] controls which is 'main' if Old _and_ New calls are being made:
  [1] controls if the Old call is made
  [2] controls if the New call is made

if Old/New calls exhibit _different_ behaviour
  if running-unit-tests:
      raise StrangledDifference(...)
  else:
      log difference to a file - never leak an exception
"""

OLD_ONLY = ("old", True, False)  # mainline=old, Call old only
OLD_MAIN = ("old", True, True)   # mainline=old, Call both
NEW_MAIN = ("new", True, True)   # mainline=new, Call both
NEW_ONLY = ("new", False, True)  # mainline=new, Call new only


def switches():
    return [OLD_ONLY, OLD_MAIN, NEW_ONLY, NEW_MAIN]


def old_is_main(use):
    return use[0] == 'old'


def new_is_main(use):
    return use[0] == 'new'


def call_old(use):
    return use[1]


def call_new(use):
    return use[2]
