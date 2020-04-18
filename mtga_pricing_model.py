#!/usr/bin/env python3.7
from typing import Dict, Union
from decimal import Decimal
from convert_to_decimal import convert_to_decimal

# project imports
from pricing_constants import *


class PricingModel:
    local_currency: str
    pricing_reference: Dict[str, Dict[str, Decimal]]

    def __init__(self, local_currency: str = "usd"):
        self.local_currency = local_currency
        self.pricing_reference = self._pack_price_pegging()

    def _pack_price_pegging(self) -> Dict[str, Dict[str, Decimal]]:
        """We peg the economy in terms of per pack value derived from the maximum amount of purchaseable gems."""
        lookup_table = {
            "gold": {"cost": GOLD_PER_PACK, "quantity": GOLD_PACK_QUANTITY},
            "gems": {"cost": GEMS_PER_PACK, "quantity": GEMS_PACK_QUANTITY},
        }

        for price_type in lookup_table.keys():
            lookup_table[price_type]["per_pack"] = Decimal(
                lookup_table[price_type]["cost"] / lookup_table[price_type]["quantity"]
            )

        dollar_cost_per_pack = self._establish_baseline_conversion(
            lookup_table["gems"]["per_pack"]
        )

        lookup_table[self.local_currency] = {
            "cost": dollar_cost_per_pack,
            "quantity": Decimal(1),
            "per_pack": dollar_cost_per_pack,
        }
        return lookup_table

    def _establish_baseline_conversion(self, gems: Decimal = Decimal(0)) -> Decimal:
        """In the 2020 Spring MTGA Economy, the best deal for gems is buying
        20,000 gems for $100 USD. We assume this as the base rate for all
        gem transactions.
    
        We then derive the dollar costs from the gems per pack cost
        """
        gems_by_spend = MAXIMUM_BUYABLE_GEMS / local_currency_prices(
            self.local_currency
        )
        return gems / gems_by_spend

    def _generic_conversion(
        self,
        amount: Union[int, float, Decimal, str],
        from_currency: str,
        to_currency: str,
    ) -> Decimal:
        """Converts from one pricing table type to another"""
        decimal_amount = convert_to_decimal(amount)

        if (
            from_currency not in self.pricing_reference.keys()
            or to_currency not in self.pricing_reference.keys()
        ):
            raise RuntimeError(
                "Could not find currency mapping: from: {} , to: {}".format(
                    from_currency, to_currency
                )
            )

        normalized_value = Decimal(
            decimal_amount / self.pricing_reference[from_currency]["per_pack"]
        )
        converted_value = Decimal(
            normalized_value * self.pricing_reference[to_currency]["per_pack"]
        )
        return converted_value

    def convert_gems_to_local_currency(
        self, gems: Union[int, float, Decimal, str] = Decimal(0),
    ) -> Decimal:
        return self._generic_conversion(
            amount=gems, from_currency="gems", to_currency=self.local_currency
        )

    def convert_gems_to_gold(
        self, gems: Union[int, float, Decimal, str] = Decimal(0)
    ) -> Decimal:
        return self._generic_conversion(
            amount=gems, from_currency="gems", to_currency="gold"
        )

    def convert_gold_to_gems(
        self, gold: Union[int, float, Decimal, str] = Decimal(0)
    ) -> Decimal:
        return self._generic_conversion(
            amount=gold, from_currency="gold", to_currency="gems"
        )

    def convert_gold_to_local_currency(
        self, gold: Union[int, float, Decimal, str] = Decimal(0),
    ) -> Decimal:
        return self._generic_conversion(
            amount=gold, from_currency="gold", to_currency=self.local_currency
        )

    def convert_packs_to_gems(
        self, packs: Union[int, float, Decimal, str] = Decimal(0),
    ) -> Decimal:
        return convert_to_decimal(packs) * self.pricing_reference["gems"]["per_pack"]

    def convert_packs_to_local_currency(
        self, packs: Union[int, float, Decimal, str] = Decimal(0)
    ) -> Decimal:
        return (
            convert_to_decimal(packs)
            * self.pricing_reference[self.local_currency]["per_pack"]
        )

    def run_tests(self):
        """Probably should figure out a better way to test this, but that's later.
        USD is the default because our failed nation is still #1! USA! USA!"""
        print("1000 gold : ${}".format(self.convert_gold_to_local_currency(1000)))
        print("600 gems : ${}".format(self.convert_gems_to_local_currency(600)))
        print("3 packs: {} gems".format(self.convert_packs_to_gems(3)))


if __name__ == "__main__":
    test = PricingModel(local_currency="usd")
    test.run_tests()
