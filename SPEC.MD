World Explorer Quiz 

1. Project Overview
World Explorer Quiz  can make an account, log in, do quiz questions, and save their score history. The topic of the quiz is travel, food, landmarks, and culture.

2. Behavior Description
main menu:
- Create a new account
- Log in
- Quit
If creates an account, the program asks for a username and password, then saved.
If logs in, the program asks for username and password. If the login is correct, the user goes to the next menu. If not, it shows an error and goes back.
After login, the user can:
- Start a quiz
- View score history
- Log out
If starts a quiz, they can choose:
- category quiz
- mixed quiz
If choose category quiz, the categories are:
- Capitals
- Landmarks
- World Foods
- Culture & Traditions
The questions come from `questions.json`.The user answers by typing the number.
After each question, the program tells the user if the answer is right or wrong. Then it asks for feedback:
- Like
- Dislike
- Skip
The feedback is saved. Later, the program should use it when picking questions, so liked categories may show up more and disliked ones less.
At the end, the program shows the final score and saves it.
If the user chooses score history, the program shows old quiz results.

3. Data Format
The questions are stored in a separate JSON file called `questions.json`.
Each question looks like this:
    {
      "question": "What is the capital of Japan?",
      "type": "multiple_choice",
      "options": ["Seoul", "Tokyo", "Beijing", "Bangkok"],
      "answer": "Tokyo",
      "category": "Capitals",
      "difficulty": "easy"
    }
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

4. File Structure
The project includes these files:
- `quiz.py`
- `questions.json`
- `users.dat`
- `scores.dat`
- `preferences.dat`
- `SPEC.md`
- `REVIEW.md`
- `REFLECTION.md`

5. Required Features
The program should have:
1. account creation and login
2. saved score history
3. user data stored in a way that is not too easy to read
4. like/dislike feedback

6. Extension Feature
The extension feature is category selection before the quiz starts.The user can choose:
- one category
- or a mixed quiz

7. Error Handling
The program should handle:
1. missing `questions.json`
2. wrong login information
3. broken or empty saved data files

8. Acceptance Criteria
The project is complete if:
1. a user can create an account and log in later
2. questions are loaded from a separate JSON file
3. the user can choose category quiz or mixed quiz
4. the program tells the user if the answer is right or wrong
5. score history is saved across runs
6. like/dislike/skip feedback is saved