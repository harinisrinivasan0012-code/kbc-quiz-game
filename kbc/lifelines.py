"""The two lifelines: 50:50 and Audience Poll."""

# How sure the audience is of the right answer, by question level (percent).
POLL_RANGE = {"easy": (70, 90), "medium": (50, 70), "hard": (30, 55)}


def fifty_fifty(correct, rng):
    """Keep the correct option and ONE random wrong option. Returns a set of indices."""
    wrong = [i for i in range(4) if i != correct]
    return {correct, rng.choice(wrong)}


def audience_poll(correct, visible, level, rng):
    """Return {option_index: percent} for the options still visible.

    The audience favours the right answer, but not always strongly on hard questions.
    """
    low, high = POLL_RANGE[level]
    top = rng.randint(low, high)
    others = [i for i in sorted(visible) if i != correct]
    remaining = 100 - top
    cuts = sorted(rng.randint(0, remaining) for _ in range(len(others) - 1))
    parts = [b - a for a, b in zip([0] + cuts, cuts + [remaining])]
    result = {correct: top}
    result.update(zip(others, parts))
    return result
