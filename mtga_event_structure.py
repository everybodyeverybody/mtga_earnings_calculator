#!/usr/bin/env python3.7
from decimal import Decimal
from collections import namedtuple
from typing import List, Union, Optional

# local imports
from convert_to_decimal import convert_to_decimal
from mtga_event_prize_level import EventPrizeLevel


class EventStructure:
    name: str
    matches: Decimal
    losses: Decimal
    rounds_per_match: Decimal
    prizes: List[EventPrizeLevel]
    gold_entry_fee: Optional[int]
    gems_entry_fee: Optional[int]

    def __init__(
        self,
        name: str = "New Event",
        matches: Union[int, float, Decimal, str] = 1,
        losses: Union[int, float, Decimal, str] = 0,
        rounds_per_match: Union[int, float, Decimal, str] = 1,
        prizes: List[EventPrizeLevel] = None,
        gold_entry_fee: Optional[int] = None,
        gems_entry_fee: Optional[int] = None,
    ):
        # gotta account for events with prizes for 0th place
        if matches + 1 != len(prizes):
            raise RuntimeError(
                "Amount of matches does not equal amount of prize levels"
            )

        if matches < 1 or rounds_per_match < 1:
            raise RuntimeError(
                "Must have at least 1 round and 1 match. Rounds: {}, Matches {}".format(
                    rounds, matches
                )
            )

        if rounds_per_match % 2 == 0:
            raise RuntimeError("Rounds per match must be odd")

        if losses < 0:
            raise RuntimeError(
                "Must have at least 0 losses as the maximum amount of losses acceptable"
            )

        if not prizes:
            raise RuntimeError("Must provide a prize structure")

        if not gold_entry_fee and not gems_entry_fee:
            raise RuntimeError(
                "Cannot have an event with no valid fee. If the event is free set gold_entry_fee or gems_entry_fee to 0"
            )

        self.name = name
        self.matches = convert_to_decimal(matches)
        self.losses = convert_to_decimal(losses)
        self.rounds_per_match = convert_to_decimal(rounds_per_match)
        self.prizes = prizes
        if gold_entry_fee:
            self.gold_entry_fee = convert_to_decimal(gold_entry_fee)
        if gems_entry_fee:
            self.gems_entry_fee = convert_to_decimal(gems_entry_fee)


if __name__ == "__main__":
    prizes = [
        EventPrizeLevel(packs=1, gold=0, gems=100),
        EventPrizeLevel(packs=2, gold=0, gems=200),
        EventPrizeLevel(packs=3, gold=0, gems=300),
        EventPrizeLevel(packs=4, gold=0, gems=400),
    ]
    fake_event = EventStructure(
        name="Magical Xmas Land",
        matches=4,
        rounds_per_match=4,
        prizes=prizes,
        gold_entry_fee=1000,
    )
    print(fake_event.name)
