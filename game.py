"""The game loop. `ask` and `say` can be replaced, which makes testing easy."""

import random

from .lifelines import audience_poll, fifty_fifty
from .money import CHECKPOINTS, LADDER, format_inr, quit_amount, safe_amount

LETTERS = "ABCD"


def show_question(q, number, visible, say):
    say("")
    say(f"Question {number} for {format_inr(LADDER[number - 1])}")
    say(q.text)
    for i, option in enumerate(q.options):
        if i in visible:
            say(f"   {LETTERS[i]}) {option}")


def make_prompt(lifelines):
    parts = ["A/B/C/D"]
    if lifelines["1"]:
        parts.append("1=50:50")
    if lifelines["2"]:
        parts.append("2=Audience Poll")
    parts.append("Q=quit")
    return "Your choice (" + ", ".join(parts) + "): "


def show_poll(poll, say):
    say("Audience poll:")
    for i in sorted(poll):
        say(f"   {LETTERS[i]}: {poll[i]:>3}%  {'#' * (poll[i] // 4)}")


def play(questions, ask=input, say=print, rng=None):
    """Play one game. Returns {'outcome': 'won'|'lost'|'quit', 'correct': n, 'winnings': rupees}."""
    rng = rng or random.Random()
    lifelines = {"1": True, "2": True}  # True = still available
    correct = 0

    for number, q in enumerate(questions, start=1):
        visible = {0, 1, 2, 3}
        show_question(q, number, visible, say)

        while True:
            choice = ask(make_prompt(lifelines)).strip().upper()

            if choice in LETTERS and len(choice) == 1:
                index = LETTERS.index(choice)
                if index not in visible:
                    say("That option was removed. Choose again.")
                    continue
                break

            if choice == "Q":
                amount = quit_amount(correct)
                say(f"\nYou quit and take home {format_inr(amount)}.")
                return {"outcome": "quit", "correct": correct, "winnings": amount}

            if choice == "1":
                if not lifelines["1"]:
                    say("You have already used 50:50.")
                    continue
                lifelines["1"] = False
                visible = fifty_fifty(q.answer, rng)
                show_question(q, number, visible, say)
                continue

            if choice == "2":
                if not lifelines["2"]:
                    say("You have already used Audience Poll.")
                    continue
                lifelines["2"] = False
                show_poll(audience_poll(q.answer, visible, q.level, rng), say)
                continue

            say("Please type A, B, C, D, 1, 2 or Q.")

        if index == q.answer:
            correct += 1
            say(f"\nCorrect! You have won {format_inr(LADDER[correct - 1])}.")
            if correct in CHECKPOINTS and correct < len(questions):
                say(f"*** Checkpoint! {format_inr(LADDER[correct - 1])} is now safe. ***")
        else:
            amount = safe_amount(correct)
            say(f"\nWrong! The correct answer was "
                f"{LETTERS[q.answer]}) {q.options[q.answer]}.")
            say(f"You go home with {format_inr(amount)}.")
            return {"outcome": "lost", "correct": correct, "winnings": amount}

    amount = LADDER[len(questions) - 1]
    say(f"\nINCREDIBLE! You answered every question and won {format_inr(amount)}!")
    return {"outcome": "won", "correct": correct, "winnings": amount}
