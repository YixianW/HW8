# World Explorer Quiz - Specification

## 1. Project Overview

World Explorer Quiz is a local command-line quiz application written in Python. The app allows users to create accounts, log in, answer quiz questions, and save their quiz history across multiple runs. The quiz content focuses on travel, food, landmarks, and culture. Users can also give feedback on questions by marking them as liked or disliked, and this feedback affects future question selection.

## 2. Behavior Description

When the program starts, it displays a welcome message and a main menu. The main menu gives the user three choices:
- Create a new account
- Log in
- Quit

If the user chooses to create a new account, the program asks for a username and password. If the username already exists, the program shows an error message and asks the user to try another username. If the account is created successfully, the account information is saved locally.

If the user chooses to log in, the program asks for a username and password. If the login is successful, the user enters the logged-in menu. If the login fails, the program shows an error message and returns to the main menu.

After login, the program shows the following options:
- Start a quiz
- View score history
- Log out

If the user chooses to start a quiz, the program asks whether the user wants:
- A category quiz
- A mixed quiz

If the user chooses a category quiz, the program displays the available categories:
- Capitals
- Landmarks
- World Foods
- Culture & Traditions

The program loads questions from a separate file called `questions.json`. Questions are shown one at a time. Each question is multiple choice and has four options. The user answers by entering the number of the chosen option.

After the user answers a question, the program tells the user whether the answer is correct or incorrect. Then the program asks the user for feedback on that question:
- Like
- Dislike
- Skip

This feedback is saved locally. In future quizzes, the program should use stored feedback to influence question selection. For example, it may show more questions from liked categories and fewer questions from disliked categories.

At the end of the quiz, the program displays the final score and saves the result to the user’s history.

If the user chooses to view score history, the program displays previous quiz results for that user.

If the user chooses to log out, the program returns to the main menu.

The program continues until the user chooses to quit.

## 3. Data Format

The quiz questions are stored in a separate human-readable JSON file called `questions.json`.

Each question uses the following structure:

    {
      "question": "What is the capital of Japan?",
      "type": "multiple_choice",
      "options": ["Seoul", "Tokyo", "Beijing", "Bangkok"],
      "answer": "Tokyo",
      "category": "Capitals",
      "difficulty": "easy"
    }

Field descriptions:
- `question`: the question text
- `type`: the question type, which will be `multiple_choice`
- `options`: a list of four answer choices
- `answer`: the correct answer
- `category`: the question category
- `difficulty`: the difficulty level

The categories used in this project are:
- Capitals
- Landmarks
- World Foods
- Culture & Traditions

Sample questions:

    {
      "questions": [
        {
          "question": "What is the capital of Japan?",
          "type": "multiple_choice",
          "options": ["Seoul", "Tokyo", "Beijing", "Bangkok"],
          "answer": "Tokyo",
          "category": "Capitals",
          "difficulty": "easy"
        },
        {
          "question": "What is the capital of Italy?",
          "type": "multiple_choice",
          "options": ["Venice", "Rome", "Milan", "Florence"],
          "answer": "Rome",
          "category": "Capitals",
          "difficulty": "easy"
        },
        {
          "question": "In which city is the Eiffel Tower located?",
          "type": "multiple_choice",
          "options": ["Rome", "Paris", "Madrid", "Vienna"],
          "answer": "Paris",
          "category": "Landmarks",
          "difficulty": "easy"
        },
        {
          "question": "Tacos are a popular food from which country?",
          "type": "multiple_choice",
          "options": ["Mexico", "Spain", "Argentina", "Brazil"],
          "answer": "Mexico",
          "category": "World Foods",
          "difficulty": "easy"
        },
        {
          "question": "Diwali is a major festival celebrated in which country?",
          "type": "multiple_choice",
          "options": ["India", "Egypt", "Mexico", "Japan"],
          "answer": "India",
          "category": "Culture & Traditions",
          "difficulty": "medium"
        }
      ]
    }

## 4. File Structure

The project will include the following files:

- `quiz.py` - the main Python program
- `questions.json` - the human-readable question bank
- `users.dat` - stores user account information locally
- `scores.dat` - stores score history locally
- `preferences.dat` - stores liked and disliked question data locally
- `SPEC.md` - project specification
- `REVIEW.md` - AI review document
- `REFLECTION.md` - reflection on the workflow and results

The main program should include functions for:
- loading questions
- creating accounts
- logging in users
- starting quizzes
- checking answers
- saving scores
- saving preferences
- displaying score history

## 5. Required Features

The program must include all of the following features:

1. A local account creation and login system
2. A separate human-readable JSON file containing quiz questions
3. A score history system that saves results across multiple runs
4. Local storage of user-related data in a form that is not easily human-readable
5. A system that lets users like or dislike questions after answering
6. A system that uses saved preferences to affect future question selection
7. A local command-line interface implemented in Python

## 6. Extension Feature

The extension feature for this project is category selection before starting a quiz.

Before each quiz, the user can choose either:
- a quiz from one specific category
- a mixed quiz using questions from multiple categories

This feature makes the app more organized and gives users more control over the type of quiz they want to take.

## 7. Error Handling

The program should handle errors safely and should not crash in common user situations.

The program must handle at least the following cases:

1. If `questions.json` is missing, the program shows an error message and exits safely.
2. If `questions.json` contains invalid JSON, the program shows an error message and exits safely.
3. If the user enters an invalid main menu choice, the program asks again.
4. If the user enters an invalid logged-in menu choice, the program asks again.
5. If the user enters an invalid answer choice during a quiz, the program asks again.
6. If the user tries to create an account with an existing username, the program shows an error and asks for a different username.
7. If login information is incorrect, the program shows an error and returns to the main menu.
8. If saved local data files are empty, malformed, or missing expected content, the program handles the issue safely instead of crashing.

## 8. Acceptance Criteria

A completed version of this project should meet the following criteria:

1. The program starts successfully from the command line using Python.
2. A new user can create an account and later log in with the same credentials.
3. Quiz questions are loaded from a separate human-readable JSON file.
4. The user can choose either a category quiz or a mixed quiz.
5. The program displays one multiple-choice question at a time and validates answer input.
6. The program tells the user whether each answer is correct or incorrect.
7. The program saves quiz score history across multiple runs.
8. The program asks for like/dislike/skip feedback after each question and saves that feedback.
9. Saved feedback affects future question selection.
10. The program handles invalid input and common file errors without crashing.

## 9. Notes on Local Storage

The question bank must remain human-readable in `questions.json`. However, account data, score history, and preference data should not be stored in a way that is immediately easy to read.

At minimum:
- passwords must not be stored as plain text
- user score data should not be stored as a clearly readable plain-text list
- preference data should also be stored locally in a less human-readable format

The storage method should remain simple and appropriate for a beginner Python project. The goal is not advanced security, but a reasonable attempt to avoid obvious plain-text storage of sensitive data.

## 10. Design Goals

The app should feel like a small but complete command-line product rather than a one-file demo. The interface should be simple, clear, and easy to follow. The question bank should feel organized because it is grouped into meaningful categories. The app should be usable across multiple runs, with saved progress, score history, and preference data.