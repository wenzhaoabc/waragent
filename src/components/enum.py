# -*-
from enum import StrEnum, Enum


class CountryRel(StrEnum):
    """Country relations"""

    W = "x"
    """war declarations"""
    M = "&"
    """military alliances"""
    T = "o"
    """non-intervention treaties"""
    P = "~"
    """peace agreements"""
    N = "-"
    """null (no relation)"""
