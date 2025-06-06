import json
import random

def load_questions():
    try:
        with open("data/questions.json","r",
    encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
      return[]
    
def get_random_question(questions):
    return random.choice(questions)
