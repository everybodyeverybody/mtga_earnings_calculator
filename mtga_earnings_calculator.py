#!/usr/bin/env python3.7
import random
from decimal import Decimal
from mtga_pricing_model import PricingModel
from mtga_event_structure import EventStructure
from mtga_event_prize_level import EventPrizeLevel

# i got tired so this is not done in the way i would typically do code
# see the other classes for more of what i do


def compare_entry_fees(gold, gems, pricing_model):
    if gold:
        gold_fee_in_currency = pricing_model.convert_gold_to_local_currency(gold)
    else:
        gold_fee_in_currency = None

    if gems:
        gems_fee_in_currency = pricing_model.convert_gems_to_local_currency(gems)
    else:
        gems_fee_in_currency = None

    if gems_fee_in_currency and gold_fee_in_currency:
        if gems_fee_in_currency < gold_fee_in_currency:
            print("Buying in with gems is cheaper: {} currency {} gems < {} currency {} gold".format(gems_fee_in_currency,gems,gold_fee_in_currency,gold))
            return gems_fee_in_currency
        elif gold_fee_in_currency < gems_fee_in_currency:
            print("Buying in with gold is cheaper: {} currency {} gold < {} currency {} gems".format(gold_fee_in_currency,gold,gems_fee_in_currency,gems))
            return gold_fee_in_currency
        else:
            print("No preference, defaulting to gems: {} currency {} gems".format(gems_fee_in_currency,gems))
            return gems_fee_in_currency

    if gems_fee_in_currency:
        return gems_fee_in_currency

    if gold_fee_in_currency:
        return gold_fee_in_currency
    raise RuntimeError("Something weird happened to get here")


def calculate_earnings(event, prizes):
    pricing_model = PricingModel(local_currency="usd")
    entry_fee_in_currency = compare_entry_fees(
        event.gold_entry_fee, event.gems_entry_fee, pricing_model
    )
    total_buyins = Decimal(0)
    total_winnings = Decimal(0)
    buyin_count = 0
    for entry in prizes:
        packs_in_currency = pricing_model.convert_packs_to_local_currency(entry.packs)
        gems_in_currency = pricing_model.convert_gems_to_local_currency(entry.gems)
        gold_in_currency = pricing_model.convert_gold_to_local_currency(entry.gold)
        total_winnings += packs_in_currency + gems_in_currency + gold_in_currency
        total_buyins += entry_fee_in_currency
        buyin_count += 1
    average_winnings_per_buyin = total_winnings / Decimal(buyin_count)
    total_earnings =  total_winnings - total_buyins
    ev = average_winnings_per_buyin - entry_fee_in_currency

    print("Single Buyin Costs: {}".format(entry_fee_in_currency)) 
    print("Total Buyins ({}): {}".format(buyin_count,total_buyins))
    print("Total Winnings: {}".format(total_winnings))
    print("Total Earnings: {}".format(total_earnings))
    print("Average Winnings Per Buyin: {}".format(average_winnings_per_buyin))
    print("EV: {}".format(ev))


def zero_match_loss_tracker(match_count, match_losses, event_matches, event_losses):
    return match_count < event_matches


def regular_match_loss_tracker(match_count, match_losses, event_matches, event_losses):
    return match_losses < event_losses and match_count < event_matches


def calculate_prizes(event, trials=10000, win_rate_percentage=50, print_records=False):
    if win_rate_percentage > 100 or win_rate_percentage < 1:
        print("defaulting win rate percentage to 50")
        win_rate_percentage = 50
    # floor division // provides the remainder
    prizes_won = []
    max_wins_or_losses = event.rounds_per_match // 2 + 1
    trial_count = 0
    if event.losses == 0:
        progress_tracker = zero_match_loss_tracker
    else:
        progress_tracker = regular_match_loss_tracker
    while trial_count < trials:
        trial_count += 1
        match_losses = 0
        match_wins = 0
        match_count = 0
        while progress_tracker(match_count, match_losses, event.matches, event.losses):
            match_count += 1
            round_losses = 0
            round_wins = 0
            while round_losses < max_wins_or_losses and round_wins < max_wins_or_losses:
                round_result = random.randint(1, 100)
                if round_result < win_rate_percentage:
                    round_wins += 1
                else:
                    round_losses += 1
            if print_records:
                print(
                    "Match {}: You went {}-{}".format(
                        match_count, round_wins, round_losses
                    )
                )
            if round_wins > round_losses:
                match_wins += 1
            else:
                match_losses += 1
        if print_records:
            print(
                "Event {}: You went {}-{}".format(trial_count, match_wins, match_losses)
            )
        prizes_won.append(event.prizes[match_wins])
    return prizes_won


def main():
    traditional_ikora_draft_prizes = [
        EventPrizeLevel(packs=1),
        EventPrizeLevel(packs=1),
        EventPrizeLevel(packs=4, gems=1000),
        EventPrizeLevel(packs=6, gems=3000),
    ]

    traditional_ikora_draft = EventStructure(
        name="Traditional Ikoria Draft",
        matches=3,
        rounds_per_match=3,
        losses=0,
        prizes=traditional_ikora_draft_prizes,
        gold_entry_fee=10000,
        gems_entry_fee=1500,
    )
    prizes = calculate_prizes(traditional_ikora_draft, trials=5)
    calculate_earnings(traditional_ikora_draft, prizes)


if __name__ == "__main__":
    main()
