"""Start the game with:  python -m kbc"""

import random
import sys

from .game import play
from .money import CHECKPOINTS, LADDER, format_inr
from .questions import load_bank, pick_questions

BANNER = r"""
==============================================
        KBC  QUIZ  GAME  (fan-made)
==============================================
"""


def main():
    print(BANNER)
    name = input("What is your name? ").strip() or "Player"
    print(f"\nWelcome, {name}! 15 questions stand between you and {format_inr(LADDER[-1])}.")
    print(f"Safe checkpoints: {', '.join(format_inr(LADDER[c - 1]) for c in CHECKPOINTS)}")
    print("Lifelines: 50:50 and Audience Poll (one use each).")

    bank = load_bank()
    while True:
        input("\nPress Enter to start...")
        play(pick_questions(bank, random.Random()))
        if input("\nPlay again? (y/n) ").strip().lower() != "y":
            print(f"Thanks for playing, {name}!")
            return 0


if __name__ == "__main__":
    sys.exit(main())
