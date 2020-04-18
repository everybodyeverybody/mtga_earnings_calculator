#!/usr/bin/env python3.7
from decimal import Decimal
from collections import namedtuple

EventPrizeLevel = namedtuple(
    "EventPrizeLevel", ["packs", "gems", "gold"], defaults=[0, 0, 0],
)
