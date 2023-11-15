import sys
# You may also pick one without version check, of course
if sys.version_info < (3, 11):
    from typing_extensions import TypedDict, Required, NotRequired, Unpack
else:
    from typing import TypedDict, Required, NotRequired, Unpack