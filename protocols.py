"""Custom protocols for use in static type annotations."""

__all__ = ['HashableSortable']

from collections.abc import Hashable
from typing import Protocol

from useful_types import SupportsDunderLT


class HashableSortable[T](Hashable, SupportsDunderLT[T], Protocol):
    """Protocol representing support for ``<`` and ``hash``."""

    __slots__ = ()
