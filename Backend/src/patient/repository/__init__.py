"""Modul für den DB-Zugriff."""

from patient.repository.pageable import MAX_PAGE_SIZE, Pageable
from patient.repository.slice import Slice

# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    "MAX_PAGE_SIZE",
    "Pageable",
    "Slice"
]
