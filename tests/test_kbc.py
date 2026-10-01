import random
import unittest

from kbc.game import LETTERS, play
from kbc.lifelines import audience_poll, fifty_fifty
from kbc.money import LADDER, format_inr, quit_amount, safe_amount
from kbc.questions import load_bank, pick_questions


def scripted(replies):
    """An `ask` function that returns pre-planned replies one by one."""
    it = iter(replies)
    return lambda prompt: next(it)


def right(questions, count):
    return [LETTERS[q.answer] for q in questions[:count]]


class TestMoney(unittest.TestCase):
    def test_format_inr(self):
        self.assertEqual(format_inr(0), "Rs 0")
        self.assertEqual(format_inr(1000), "Rs 1,000")
        self.assertEqual(format_inr(160000), "Rs 1,60,000")
        self.assertEqual(format_inr(1250000), "Rs 12,50,000")
        self.assertEqual(format_inr(10000000), "Rs 1,00,00,000")

    def test_ladder_increases(self):
        self.assertEqual(len(LADDER), 15)
        self.assertEqual(LADDER, sorted(LADDER))

    def test_safe_and_quit_amounts(self):
        self.assertEqual(safe_amount(0), 0)
        self.assertEqual(safe_amount(4), 0)
        self.assertEqual(safe_amount(5), 10_000)
        self.assertEqual(safe_amount(9), 10_000)
        self.assertEqual(safe_amount(11), 3_20_000)
        self.assertEqual(quit_amount(0), 0)
        self.assertEqual(quit_amount(3), 3_000)


class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.bank = load_bank()

    def test_bank_is_valid(self):
        self.assertGreaterEqual(len(self.bank), 15)

    def test_pick_questions(self):
        qs = pick_questions(self.bank, random.Random(1))
        self.assertEqual([q.level for q in qs], ["easy"] * 5 + ["medium"] * 5 + ["hard"] * 5)

    def test_shuffle_keeps_right_answer(self):
        by_text = {q.text: q.options[q.answer] for q in self.bank}
        for seed in range(20):
            for q in pick_questions(self.bank, random.Random(seed)):
                self.assertEqual(q.options[q.answer], by_text[q.text])


class TestLifelines(unittest.TestCase):
    def test_fifty_fifty(self):
        for seed in range(30):
            kept = fifty_fifty(2, random.Random(seed))
            self.assertEqual(len(kept), 2)
            self.assertIn(2, kept)

    def test_poll_adds_to_100(self):
        for seed in range(50):
            for visible in ({0, 1, 2, 3}, {1, 3}):
                poll = audience_poll(1, visible, "hard", random.Random(seed))
                self.assertEqual(sum(poll.values()), 100)
                self.assertEqual(set(poll), visible)


class TestGame(unittest.TestCase):
    def setUp(self):
        self.qs = pick_questions(load_bank(), random.Random(3))
        self.out = []
        self.say = self.out.append

    def run_game(self, replies):
        return play(self.qs, scripted(replies), self.say, random.Random(0))

    def test_win_everything(self):
        result = self.run_game(right(self.qs, 15))
        self.assertEqual(result["outcome"], "won")
        self.assertEqual(result["winnings"], 1_00_00_000)

    def test_wrong_answer_falls_to_checkpoint(self):
        wrong = LETTERS[(self.qs[6].answer + 1) % 4]
        result = self.run_game(right(self.qs, 6) + [wrong])
        self.assertEqual(result["outcome"], "lost")
        self.assertEqual(result["winnings"], 10_000)

    def test_wrong_on_first_question(self):
        wrong = LETTERS[(self.qs[0].answer + 1) % 4]
        self.assertEqual(self.run_game([wrong])["winnings"], 0)

    def test_quit_keeps_current_winnings(self):
        result = self.run_game(right(self.qs, 3) + ["q"])
        self.assertEqual(result["outcome"], "quit")
        self.assertEqual(result["winnings"], 3_000)

    def test_lifelines_work_once(self):
        a = LETTERS[self.qs[0].answer]
        replies = ["1", "1", "2", "2", a] + right(self.qs[1:], 14)
        result = self.run_game(replies)
        self.assertEqual(result["outcome"], "won")
        text = "\n".join(self.out)
        self.assertIn("already used 50:50", text)
        self.assertIn("already used Audience Poll", text)

    def test_bad_input_is_ignored(self):
        a = LETTERS[self.qs[0].answer]
        result = self.run_game(["hello", "", "9", a, "q"])
        self.assertEqual(result["outcome"], "quit")
        self.assertEqual(result["winnings"], 1_000)


if __name__ == "__main__":
    unittest.main()
