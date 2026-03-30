# World Explorer Quiz

A local Python command-line quiz app with account login, persistent score history, and per-question like/dislike feedback that influences future question selection.

## Run

1. Open a terminal in this project folder.
2. Run:

```bash
python3 quiz.py
```

## Files

- `quiz.py`: Main CLI application
- `questions.json`: Human-readable question bank
- `users.dat`: Local user account data (binary)
- `scores.dat`: Local score history data (binary)
- `preferences.dat`: Local feedback/preference data (binary)