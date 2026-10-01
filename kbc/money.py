"""The prize ladder and the rules about what you take home."""

# Prize for each of the 15 questions, in rupees.
LADDER = [
    1_000, 2_000, 3_000, 5_000, 10_000,
    20_000, 40_000, 80_000, 1_60_000, 3_20_000,
    6_40_000, 12_50_000, 25_00_000, 50_00_000, 1_00_00_000,
]

# After answering this many questions correctly, the prize is guaranteed.
CHECKPOINTS = (5, 10)


def format_inr(amount):
    """Format with Indian digit grouping: 1250000 -> 'Rs 12,50,000'."""
    digits = str(amount)
    if len(digits) <= 3:
        return f"Rs {digits}"
    head, tail = digits[:-3], digits[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    if head:
        groups.insert(0, head)
    return "Rs " + ",".join(groups + [tail])


def quit_amount(correct):
    """Money you take home if you QUIT after `correct` right answers."""
    return LADDER[correct - 1] if correct > 0 else 0


def safe_amount(correct):
    """Money you take home if you answer WRONG after `correct` right answers.

    You fall back to the last checkpoint you passed (or zero).
    """
    passed = [c for c in CHECKPOINTS if c <= correct]
    return LADDER[max(passed) - 1] if passed else 0
