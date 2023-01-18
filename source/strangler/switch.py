"""
The contract-checking decorators control overwrite/append at the
individual method/property level via keyword arguments:
      Method: (..., *, use)
  Properties: (..., *, getter, setter)

use/getter/setter are Tuples with 3 elements
  [0] controls if the overwrite call is made
  [1] controls if the append call is made
  [2] controls which is 'main' if overwrite and append calls are being made:
        - when overwrite is 'main', return/raise the overwrite result/exception.
        - when append is 'main', return/raise the append result/exception.
        - log any difference to a file.

However, when use/getter/setter=APPEND_TEST the behaviour of [2] is altered:
When a overwrite/append difference is detected:
  - Don't log the difference to a file
  - if running unit-tests
  -   raise ContractDifference() [*]
  - else
  -   return [@]

[*] Makes unit-testing the contract-checking code much easier.
[@] On staging and production, we want APPEND_TEST differences to be
    completely ignored; we don't want append work-in-progress differences
    mixed with genuine differences. Particularly when they relate to
    overwrite data that has not yet been migrated to append.
"""

# Steps in moving from overwrite to append...

OVERWRITE_ONLY = (True, None, "overwrite")  # 1st - overwrite call only, returns overwrite
APPEND_TEST = (True, 'test', "overwrite")   # 2nd - both called, returns overwrite (See above)
OVERWRITE_MAIN = (True, True, "overwrite")  # 3rd - both called, returns overwrite
APPEND_MAIN = (True, True, "append")        # 4th - both called, returns append
APPEND_ONLY = (None, True, "append")        # 5th - append call only, returns append


def overwrite_is_on(obj, use):
    """Returns True if Overwrite call is made."""
    return hasattr(obj, 'overwrite') and obj.overwrite is not None and use[0] is not None


def append_is_on(obj, use):
    """Returns True if Append call is made."""
    return obj.append is not None and use[1] is not None
