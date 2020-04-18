#!/usr/bin/env python3.7
from decimal import Decimal

GOLD_PER_PACK = Decimal(1000)
GOLD_PACK_QUANTITY = Decimal(1)
GEMS_PER_PACK = Decimal(600)
GEMS_PACK_QUANTITY = Decimal(3)
MAXIMUM_BUYABLE_GEMS = Decimal(20000)
ROUND_TO_TWO_DIGITS = Decimal("1.00")
MAXIMUM_BUYABLE_GEMS_COST_BY_CURRENCY = {
    "usd": Decimal(100.00),
    "eur": None,
    "cad": None,
    "jpy": None,
    "brl": None,
    "gbp": None,
}


def local_currency_prices(local_currency: str = "usd") -> Decimal:
    """Although all the strings are in english, this at least allows for people to fill in
    with whatever their local market rates are. Need to find if there's ISO standards for currency
    names, or something similar that can be used."""
    lookup = local_currency.lower()
    if (
        lookup not in MAXIMUM_BUYABLE_GEMS_COST_BY_CURRENCY
        or not MAXIMUM_BUYABLE_GEMS_COST_BY_CURRENCY[lookup]
    ):
        raise RuntimeError("Currency {} not configured".format(lookup))
    return MAXIMUM_BUYABLE_GEMS_COST_BY_CURRENCY[lookup]
