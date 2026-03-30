#!/usr/bin/env python3
"""World Explorer Quiz - local command-line quiz app."""

import base64
import hmac
import hashlib
import json
import os
import pickle
import random
from datetime import datetime


QUESTIONS_FILE = "questions.json"
USERS_FILE = "users.dat"
SCORES_FILE = "scores.dat"
PREFERENCES_FILE = "preferences.dat"

VALID_CATEGORIES = [
    "Capitals",
    "Landmarks",
    "World Foods",
    "Culture & Traditions",
]


def safe_load_pickle(path, default, expected_type):
    """Load binary data safely and recover from missing/malformed content."""
    if not os.path.exists(path):
        return default

    try:
        with open(path, "rb") as file:
            raw = file.read()
            if not raw:
                return default
            data = pickle.loads(raw)
            if not isinstance(data, expected_type):
                return default
            return data
    except (pickle.UnpicklingError, EOFError, OSError, ValueError, TypeError):
        return default


def safe_save_pickle(path, data):
    try:
        with open(path, "wb") as file:
            pickle.dump(data, file)
    except OSError:
        print(f"Error: Could not save data to {path}.")


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return {
        "salt": base64.b64encode(salt).decode("ascii"),
        "hash": base64.b64encode(digest).decode("ascii"),
    }


def verify_password(password, stored_record):
    try:
        salt = base64.b64decode(stored_record["salt"].encode("ascii"))
        candidate = hash_password(password, salt=salt)["hash"]
        return hmac.compare_digest(candidate, stored_record["hash"])
    except (KeyError, ValueError, TypeError):
        return False


def ensure_storage_files(users, scores, preferences):
    if not os.path.exists(USERS_FILE):
        safe_save_pickle(USERS_FILE, users)
    if not os.path.exists(SCORES_FILE):
        safe_save_pickle(SCORES_FILE, scores)
    if not os.path.exists(PREFERENCES_FILE):
        safe_save_pickle(PREFERENCES_FILE, preferences)


def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        print("Error: questions.json is missing. Please add it and try again.")
        return None

    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
            payload = json.load(file)
    except json.JSONDecodeError:
        print("Error: questions.json contains invalid JSON. Please fix the file.")
        return None
    except OSError:
        print("Error: Could not read questions.json.")
        return None

    if not isinstance(payload, dict) or "questions" not in payload:
        print("Error: questions.json is malformed. Expected an object with 'questions'.")
        return None

    questions = payload["questions"]
    if not isinstance(questions, list):
        print("Error: questions.json is malformed. 'questions' must be a list.")
        return None

    valid_questions = []
    for item in questions:
        if not isinstance(item, dict):
            continue
        required = {"question", "type", "options", "answer", "category", "difficulty"}
        if not required.issubset(item.keys()):
            continue
        if item["type"] != "multiple_choice":
            continue
        if not isinstance(item["options"], list) or len(item["options"]) != 4:
            continue
        valid_questions.append(item)

    if not valid_questions:
        print("Error: No valid questions found in questions.json.")
        return None

    return valid_questions


def prompt_menu_choice(prompt, allowed):
    while True:
        raw = input(prompt).strip()
        if raw in allowed:
            return raw
        print("Invalid choice. Please try again.")


def create_account(users):
    print("\n=== Create Account ===")
    while True:
        username = input("Choose a username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
        if username in users:
            print("That username already exists. Please choose another.")
            continue
        break

    while True:
        password = input("Choose a password: ").strip()
        if len(password) < 4:
            print("Password must be at least 4 characters.")
            continue
        break

    users[username] = hash_password(password)
    safe_save_pickle(USERS_FILE, users)
    print("Account created successfully.")


def login(users):
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username not in users or not verify_password(password, users[username]):
        print("Login failed: incorrect username or password.")
        return None

    print(f"Welcome, {username}!")
    return username


def choose_quiz_mode():
    print("\nQuiz Type:")
    print("1. Category quiz")
    print("2. Mixed quiz")
    choice = prompt_menu_choice("Choose an option (1-2): ", {"1", "2"})
    return "category" if choice == "1" else "mixed"


def choose_category():
    print("\nCategories:")
    for idx, category in enumerate(VALID_CATEGORIES, start=1):
        print(f"{idx}. {category}")

    choice = prompt_menu_choice("Choose a category (1-4): ", {"1", "2", "3", "4"})
    return VALID_CATEGORIES[int(choice) - 1]


def get_weighted_questions(question_pool, user_prefs, quiz_size=5):
    liked = user_prefs.get("liked", {})
    disliked = user_prefs.get("disliked", {})

    weighted_pool = []
    for question in question_pool:
        category = question["category"]
        weight = 1 + liked.get(category, 0) - disliked.get(category, 0)
        weight = max(1, weight)
        weighted_pool.extend([question] * weight)

    selected = []
    seen = set()
    random.shuffle(weighted_pool)

    for question in weighted_pool:
        q_text = question["question"]
        if q_text in seen:
            continue
        selected.append(question)
        seen.add(q_text)
        if len(selected) >= min(quiz_size, len(question_pool)):
            break

    # Fallback in case weighted list was unusually short after de-duplication.
    if len(selected) < min(quiz_size, len(question_pool)):
        remainder = [q for q in question_pool if q["question"] not in seen]
        random.shuffle(remainder)
        selected.extend(remainder[: min(quiz_size, len(question_pool)) - len(selected)])

    return selected


def ask_answer(question):
    print("\n" + question["question"])
    for idx, option in enumerate(question["options"], start=1):
        print(f"{idx}. {option}")

    while True:
        raw = input("Your answer (1-4): ").strip()
        if raw in {"1", "2", "3", "4"}:
            return question["options"][int(raw) - 1]
        print("Invalid answer choice. Please enter 1, 2, 3, or 4.")


def ask_feedback():
    print("Feedback on this question:")
    print("1. Like")
    print("2. Dislike")
    print("3. Skip")
    choice = prompt_menu_choice("Choose feedback (1-3): ", {"1", "2", "3"})
    return {"1": "like", "2": "dislike", "3": "skip"}[choice]


def apply_feedback(preferences, username, category, feedback):
    if username not in preferences or not isinstance(preferences[username], dict):
        preferences[username] = {"liked": {}, "disliked": {}}

    user_pref = preferences[username]
    user_pref.setdefault("liked", {})
    user_pref.setdefault("disliked", {})

    if feedback == "like":
        user_pref["liked"][category] = user_pref["liked"].get(category, 0) + 1
    elif feedback == "dislike":
        user_pref["disliked"][category] = user_pref["disliked"].get(category, 0) + 1


def start_quiz(username, questions, scores, preferences):
    mode = choose_quiz_mode()
    category = None

    if mode == "category":
        category = choose_category()
        question_pool = [q for q in questions if q["category"] == category]
    else:
        question_pool = questions[:]

    if not question_pool:
        print("No questions available for this selection.")
        return

    user_pref = preferences.get(username, {"liked": {}, "disliked": {}})
    selected_questions = get_weighted_questions(question_pool, user_pref, quiz_size=5)

    score = 0
    for question in selected_questions:
        chosen = ask_answer(question)
        if chosen == question["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer is: {question['answer']}")

        feedback = ask_feedback()
        apply_feedback(preferences, username, question["category"], feedback)

    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": mode,
        "category": category if category else "Mixed",
        "score": score,
        "total": len(selected_questions),
    }

    scores.setdefault(username, []).append(result)
    safe_save_pickle(SCORES_FILE, scores)
    safe_save_pickle(PREFERENCES_FILE, preferences)

    print(f"\nQuiz complete. Final score: {score}/{len(selected_questions)}")


def show_history(username, scores):
    print("\n=== Score History ===")
    history = scores.get(username, [])
    if not history:
        print("No quiz history found yet.")
        return

    for idx, item in enumerate(history, start=1):
        print(
            f"{idx}. {item.get('timestamp', 'Unknown time')} | "
            f"{item.get('mode', 'unknown')} | "
            f"{item.get('category', 'unknown')} | "
            f"{item.get('score', 0)}/{item.get('total', 0)}"
        )


def logged_in_menu(username, questions, scores, preferences):
    while True:
        print("\n=== User Menu ===")
        print("1. Start a quiz")
        print("2. View score history")
        print("3. Log out")

        choice = prompt_menu_choice("Choose an option (1-3): ", {"1", "2", "3"})
        if choice == "1":
            start_quiz(username, questions, scores, preferences)
        elif choice == "2":
            show_history(username, scores)
        else:
            print("Logged out.")
            return


def main():
    print("Welcome to World Explorer Quiz!")

    questions = load_questions()
    if questions is None:
        return

    users = safe_load_pickle(USERS_FILE, default={}, expected_type=dict)
    scores = safe_load_pickle(SCORES_FILE, default={}, expected_type=dict)
    preferences = safe_load_pickle(PREFERENCES_FILE, default={}, expected_type=dict)
    ensure_storage_files(users, scores, preferences)

    while True:
        print("\n=== Main Menu ===")
        print("1. Create a new account")
        print("2. Log in")
        print("3. Quit")

        choice = prompt_menu_choice("Choose an option (1-3): ", {"1", "2", "3"})

        if choice == "1":
            create_account(users)
        elif choice == "2":
            username = login(users)
            if username:
                logged_in_menu(username, questions, scores, preferences)
        else:
            print("Thanks for playing World Explorer Quiz. Goodbye!")
            break


if __name__ == "__main__":
    main()
