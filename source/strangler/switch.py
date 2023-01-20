"""
The strangler decorators control Old/New at the
individual method/property level via keyword arguments:
      Method: (..., *, use)
  Properties: (..., *, getter, setter)

use/getter/setter are Tuples with 3 elements
  [0] controls if the New call is made
  [1] controls if the Old call is made
  [2] controls which is 'main' if Old and New calls are being made:
      if Old/New calls exhibit different behaviour
          if use is NEW_TEST:
              if running-unit-tests:
                  raise StrangledDifference(...) # [*]
              else:
                  return # [@]
          else:
              log difference to a file.

[*] Makes unit-testing the strangler-checking code much easier.
[@] On staging and production, we want NEW_TEST differences to be
    completely ignored; we don't want New work-in-progress differences
    mixed with genuine differences. Particularly when they relate to
    Old data that has not yet been migrated to New.
"""

# Steps in moving from Old to New...

OLD_ONLY = (True, None, "old")  # 1st - Old call only, returns Old
NEW_TEST = (True, 'nt', "old")  # 2nd - both called, returns Old (See above)
OLD_MAIN = (True, True, "old")  # 3rd - both called, returns Old
NEW_MAIN = (True, True, "new")  # 4th - both called, returns New
NEW_ONLY = (None, True, "new")  # 5th - New call only, returns New


def old_is_on(obj, use):
    """Returns True if Old call is made."""
    return obj.old is not None and use[0] is not None


def new_is_on(obj, use):
    """Returns True if New call is made."""
    return obj.new is not None and use[1] is not None
