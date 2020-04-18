#!/usr/bin/env python3.7
from typing import Union
from decimal import Decimal, ROUND_DOWN


def convert_to_decimal(number: Union[int, float, Decimal, str]) -> Decimal:
    ROUND_TO_TWO_DIGITS = Decimal("1.00")
    """Input validation, attempting to cover my ass and ensure my math logic is consistent"""
    if isinstance(number, Decimal) and number > Decimal(0):
        return number
    decimal_number = Decimal(number).quantize(ROUND_TO_TWO_DIGITS, rounding=ROUND_DOWN)
    if decimal_number < Decimal(0):
        raise RuntimeError("Not taking negative values here")
    return decimal_number
