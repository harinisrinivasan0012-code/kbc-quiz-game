# 🎯 KBC Quiz Game

A fan-made, terminal version of the classic "Who Wants to Be a Millionaire"-style quiz show. Answer 15 questions, climb the prize ladder, use your lifelines wisely, and decide when to quit.

> Fan project for learning. Not affiliated with or endorsed by the TV show or its makers. All questions are original general-knowledge questions.

Built with **pure Python**, no libraries to install.

## Features

- 15 questions that get harder: 5 easy, 5 medium, 5 hard, picked randomly each game
- Prize ladder from Rs 1,000 up to Rs 1,00,00,000 (shown in Indian number format)
- Two **safe checkpoints** after question 5 (Rs 10,000) and question 10 (Rs 3,20,000)
- Two lifelines, one use each:
  - **50:50** removes two wrong options
  - **Audience Poll** shows how the audience voted (less sure on harder questions)
- **Quit** any time and keep what you have won
- Add your own questions by editing one JSON file

## How to play

```bash
git clone https://github.com/harinisrinivasan0012-code/kbc-quiz-game.git
cd kbc-quiz-game
python -m kbc
```

You need Python 3.8 or newer.

| Key | What it does |
|---|---|
| `A` `B` `C` `D` | Lock in your answer |
| `1` | Use the 50:50 lifeline |
| `2` | Use the Audience Poll lifeline |
| `Q` | Quit and take home your winnings |

## What you win

| Situation | You take home |
|---|---|
| Answer wrong before question 5 | Rs 0 |
| Answer wrong between questions 6 and 10 | Rs 10,000 |
| Answer wrong between questions 11 and 15 | Rs 3,20,000 |
| Quit | The prize of your last correct answer |
| Answer all 15 | Rs 1,00,00,000 |

## Sample game

```text

Question 1 for Rs 1,000
In which city is the Taj Mahal located?
   A) Jaipur
   B) Lucknow
   C) Delhi
   D) Agra
Your choice (A/B/C/D, 1=50:50, 2=Audience Poll, Q=quit): 2
Audience poll:
   A:   3%  
   B:   6%  #
   C:  14%  ###
   D:  77%  ###################
Your choice (A/B/C/D, 1=50:50, Q=quit): D

Correct! You have won Rs 1,000.

Question 2 for Rs 2,000
How many colours are there in a rainbow?
   A) 7
   B) 8
   C) 5
   D) 6
Your choice (A/B/C/D, 1=50:50, Q=quit): A

Correct! You have won Rs 2,000.

Question 3 for Rs 3,000
Who wrote the Indian national anthem?
   A) Mahatma Gandhi
   B) Sarojini Naidu
   C) Bankim Chandra Chatterjee
   D) Rabindranath Tagore
Your choice (A/B/C/D, 1=50:50, Q=quit): q

You quit and take home Rs 2,000.
```

## Add your own questions

Open `kbc/questions.json` and add an entry like this:

```json
{"level": "medium", "question": "Which language is this project written in?",
 "options": ["Java", "Python", "C", "Ruby"], "answer": 1}
```

- `level` is `easy`, `medium` or `hard`
- `options` must be 4 different answers
- `answer` is the position of the correct option, counting from 0 (so `1` means the second option)

The game checks every question when it starts and tells you if one is wrong.

## Project structure

```text
kbc/
    money.py       # prize ladder, checkpoints, Indian number format
    questions.py   # load and pick questions, shuffle options
    questions.json # the question bank (edit me!)
    lifelines.py   # 50:50 and Audience Poll
    game.py        # the game loop
    __main__.py    # start screen and play-again loop
tests/
    test_kbc.py    # 14 unit tests, including full scripted games
```

## Run the tests

```bash
python -m unittest discover -s tests -t . -v
```

## Ideas to extend it

- Add a **Phone a Friend** lifeline
- Add a countdown timer for each question
- Save a high-score table to a file
- Add question categories (cricket, movies, science)
- Build a window version with `tkinter`

## License

MIT
