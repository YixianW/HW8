# REVIEW.md

## Scope
This review checks the implementation in `quiz.py` against `SPEC.MD`, including required features, extension feature behavior, logic correctness, input validation, file handling, score/preference handling, local storage readability, and error handling.

## Executive Summary
The project is close to spec-complete and implements the main flow correctly (account creation/login, category or mixed quiz, per-question feedback, score history persistence, and weighted selection based on feedback). However, there are important robustness gaps around malformed saved data structures that can still crash the app, which means the full error-handling requirement is **not fully satisfied**.

## Acceptance Criteria Check

1. Program starts successfully via Python CLI: **PASS**
- `quiz.py` compiles and is runnable from command line.

2. New user can create account and later log in: **PASS**
- Account creation and hashed password verification are implemented.

3. Questions loaded from separate human-readable JSON: **PASS**
- Questions are read from `questions.json` and validated for required fields.

4. User can choose category quiz or mixed quiz: **PASS**
- Both quiz types are implemented.

5. One multiple-choice question at a time with validated answer input: **PASS**
- Questions are shown one-by-one; answer input loops until 1-4.

6. Program reports correct/incorrect per answer: **PASS**
- Correctness feedback is shown immediately after each answer.

7. Score history saved across runs: **PASS (with caveat)**
- Scores are persisted to `scores.dat`.
- Caveat: malformed internal data can still break score append/display paths.

8. Like/dislike/skip feedback after each question and save feedback: **PASS (with caveat)**
- Feedback prompt is implemented and stored.
- Caveat: malformed preference internals can still crash update logic.

9. Saved feedback affects future question selection: **PASS**
- Weighted question selection uses liked/disliked category counters.

10. Handles invalid input and common file errors without crashing: **PARTIAL / FAIL**
- Missing/invalid `questions.json`, invalid menu choices, invalid answer choice, duplicate usernames, failed login are handled.
- But malformed nested content inside saved `.dat` dicts can still raise runtime exceptions.

## Required Features Check

1. Local account creation/login: **Implemented**
2. Separate human-readable JSON question file: **Implemented**
3. Persistent score history: **Implemented**
4. User data stored in not easily human-readable form: **Implemented (basic)**
5. Like/dislike feedback system: **Implemented**
6. Preferences affecting future selection: **Implemented**
7. Local Python CLI: **Implemented**

## Extension Feature Check (Category vs Mixed)
**Implemented correctly.**
- Before quiz start, user chooses category or mixed mode.
- Category mode filters by chosen category.
- Mixed mode uses full question set.
- If category has no questions, app shows message and returns safely.

## Findings (Ordered by Severity)

### High
1. Malformed preference internals can crash weighted selection
- Location: `quiz.py`, `get_weighted_questions` and caller path from `start_quiz`.
- Risk: If `preferences.dat` loads as a dict but `preferences[username]` is non-dict (or contains non-dict `liked`/`disliked`), calls like `.get(...)` on wrong types can throw `AttributeError`.
- Impact: Violates SPEC requirement to handle malformed local data safely.

2. Malformed score internals can crash score save/history paths
- Location: `quiz.py` at score append and history display.
- Risk A: `scores.setdefault(username, []).append(result)` fails if existing value for user is not a list.
- Risk B: `show_history` assumes each history item is a dict and calls `item.get(...)`; non-dict entries cause crash.
- Impact: Violates malformed saved-data handling requirement.

### Medium
3. Preference update path trusts nested types too much
- Location: `quiz.py`, `apply_feedback`.
- Risk: `user_pref.setdefault("liked", {})` and `setdefault("disliked", {})` do not repair bad existing values; if these fields exist but are not dicts, later `.get(...)` calls can fail.
- Impact: Runtime errors on corrupted/legacy data.

4. Weak persistence error handling may report success after failed write
- Location: `quiz.py`, `safe_save_pickle` and callers.
- Risk: `safe_save_pickle` only prints an error and does not return status. Callers (e.g., account creation) still print success, even if write failed.
- Impact: Misleading UX; data loss not clearly surfaced.

### Low
5. Question validation does not ensure `answer` is in `options`
- Location: `quiz.py`, `load_questions` validation.
- Risk: Malformed question entries could become unwinnable while still being treated as valid.
- Impact: Logic correctness/quality issue (not immediate crash).

## Input Validation Review
- Good:
  - Main menu choice validation.
  - Logged-in menu choice validation.
  - Quiz answer validation (1-4 loop).
  - Feedback choice validation.
  - Empty username blocked.
  - Duplicate username blocked.
  - Minimum password length enforced.
- Gaps:
  - No handling for EOF/interrupt (`EOFError`, `KeyboardInterrupt`) around `input()` calls.
  - No normalization for username case collisions (e.g., `Alice` vs `alice`) if desired.

## File Handling Review
- Good:
  - Missing `questions.json` handled with safe exit.
  - Invalid JSON in `questions.json` handled with safe exit.
  - Missing/empty/unpickling errors on `.dat` top-level are handled.
- Gaps:
  - Nested malformed data inside otherwise valid top-level dict is not sanitized consistently.
  - Save failures are not propagated to caller decisions.

## Score History & Preferences Review
- Strengths:
  - Persistent score history exists.
  - Preference feedback is captured each question.
  - Preferences influence selection by category weighting.
- Issues:
  - Corrupted per-user score/preference structures can crash append/display/weighting logic.
  - No schema migration or cleanup for bad historical records.

## Local Storage Human-Readability Check
- `users.dat`, `scores.dat`, and `preferences.dat` are stored via pickle (binary), which is not immediately human-readable in plain text editors.
- Passwords are not stored in plain text; PBKDF2-HMAC with salt is used.
- Conclusion: Meets the assignment's baseline “not easily human-readable” requirement.
- Note: This is obscurity/basic protection, not secure-at-rest encryption.

## Recommended Fixes (Priority)
1. Add normalization/sanitization helpers for loaded `scores` and `preferences` nested structures before use.
2. Harden `apply_feedback`, `start_quiz`, and `show_history` with `isinstance` checks and safe fallbacks.
3. Make `safe_save_pickle` return success/failure and update caller messages/actions accordingly.
4. Strengthen `load_questions` validation to require:
- `answer` in `options`
- `category` in allowed categories
- option and answer types as strings.
5. Optionally add graceful handling for `EOFError`/`KeyboardInterrupt` at input boundaries.

## Final Verdict
- Core functionality and extension feature: **Implemented and mostly correct**.
- Full SPEC compliance: **Not yet fully compliant** due to malformed saved-data crash paths and weak write-error propagation.
