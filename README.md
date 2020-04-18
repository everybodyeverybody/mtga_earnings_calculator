# MTGA Earnings Calculator
I wanted to write something to calculate my EV/Earnings in Magic without using Excel, so I threw this together in an afternoon.

I am a losing player in limited formats, so I wanted to see what generally would be my expected return on firing them off, and also compare what my ROI would be depending on the event. The things you do when you're pinching pennies.

## Requirements
python3.7 and the black formatting library

## Setup

You need to provide the calculator an event configuration which is specified in `mtga_event_structure.py`. You can then modify `mtga_earnings_calculator.py` with the amount of trials you want to attempt and what your expected win percentage is.

## Logic

Runs a trial (default: 10000) matches and checks whether you would win the match round-by-round, assuming your win rate is tied to rounds, not matches. I can probably refactor that in the calculation logic, but I left it as rounds for now.

## TODO

- Incorporating a random play/draw and incorporating that into match rate calculations would be fun, but likely refactoring the math to do this based on rounds would be better.
