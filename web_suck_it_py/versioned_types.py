import sys

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, Required, TypedDict, Unpack
else:
    from typing import NotRequired, Required, TypedDict, Unpack  # noqa: F401
