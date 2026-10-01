"""Loading the question bank and choosing questions for one game."""

import json
import os
from dataclasses import dataclass
from typing import List

BANK_FILE = os.path.join(os.path.dirname(__file__), "questions.json")
LEVELS = ("easy", "medium", "hard")


@dataclass
class Question:
    text: str
    options: List[str]
    answer: int  # index (0-3) of the correct option
    level: str


def load_bank(path=BANK_FILE):
    """Read questions.json and check every question is valid."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    bank = []
    for item in raw:
        q = Question(item["question"], item["options"], item["answer"], item["level"])
        if len(q.options) != 4 or len(set(q.options)) != 4:
            raise ValueError(f"Need 4 different options: {q.text}")
        if not 0 <= q.answer <= 3:
            raise ValueError(f"'answer' must be 0-3: {q.text}")
        if q.level not in LEVELS:
            raise ValueError(f"'level' must be one of {LEVELS}: {q.text}")
        bank.append(q)
    return bank


def pick_questions(bank, rng, per_level=5):
    """Pick `per_level` questions of each level, easiest first.

    Options are shuffled so the right answer is not always in the same place.
    """
    chosen = []
    for level in LEVELS:
        pool = [q for q in bank if q.level == level]
        if len(pool) < per_level:
            raise ValueError(f"Need at least {per_level} '{level}' questions.")
        for q in rng.sample(pool, per_level):
            right_text = q.options[q.answer]
            options = q.options[:]
            rng.shuffle(options)
            chosen.append(Question(q.text, options, options.index(right_text), q.level))
    return chosen
