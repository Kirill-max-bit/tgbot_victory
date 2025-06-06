# utils/quiz_utils.py
import json
import random


def load_questions():
    try:
        with open("data/questions.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def get_random_question(questions):
    return random.choice(questions)


if __name__ == "main":
    questions = load_questions()
    print(f"Загружено вопросов: {len(questions)}")
    if questions:
        print(f"Случайный вопрос: {get_random_question(questions)}")
