import os
from app import db
from flask import Flask, session, render_template, url_for, redirect, request, flash, Blueprint
from flask_login import current_user, login_required
from models import User

quiz_blueprint = Blueprint('quiz', __name__, template_folder='templates')
quiz_blueprint.secret_key = os.urandom(24)

questions = {
    "1": {"question": "Which city is the capital of Iran?", "options": ["Dhaka", "Kabul", "Tehran", "Istambul"],
          "answer": "Tehran"},
    "2": {"question": "What is the human bodys biggest organ?",
          "options": ['The cerebrum', 'Epidermis', 'Ribs', 'The skin'], "answer": "The skin"},
    "3": {"question": "Electric current is typically measured in what units?",
          "options": ['joule', 'Ampere', 'Watt', 'Ohm'], "answer": "Ampere"},
    "4": {"question": "Who was known as Iron man of India?",
          "options": ["Govind Ballabh Pant", "Jawaharlal Nehru", "Subhash Chandra Bose", "Sardar Vallabhbhai Patel"],
          "answer": "Sardar Vallabhbhai Patel"},
    "5": {"question": "What is the smallest planet in the Solar System?",
          "options": ["Mercury", "Mars", "Jupitar", "Neptune"], "answer": "Mercury"},
    "6": {'question': "What is the name of the largest ocean on earth?",
          "options": ["Atlantic", "Pacafic", "Indian Ocean", "Meditanarian"], "answer": "Pacafic"},
    "7": {'question': "What country has the second largest population in the world?",
          "options": ["Indonasia", "America", "India", "China"], "answer": "India"},
    "8": {'question': "Zurich is the largest city in what country?",
          "options": ["France", "Spain", "Scotland", "Switzerland"], "answer": "Switzerland"},
    "9": {'question': "What is the next prime number after 7?", "options": ["13", "9", "17", "11"], "answer": "11"},
    "10": {'question': "At what temperature is Fahrenheit equal to Centigrade?",
           "options": ["0 degrees ", "-40 degrees", "213 degrees", "-213 degrees"], "answer": "-40 degrees"}}


@quiz_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "POST":
        if "question" in session:
            entered_answer = request.form.get('answer', '')
            if questions.get(session["question"], False):

                if entered_answer != questions[session["question"]]["answer"]:
                  mark = 0 #points per wrong answer
                else:
                  mark = 4 #points per right answer
                
                session["mark"] += mark  
                session["question"] = str(int(session["question"]) + 1) #move to next question
                if session["question"] in questions:
                  redirect(url_for('homepage'))
                else:
                  print('render score')
                  return render_template("score.html", score=session["mark"])

    if "question" not in session:
        session["question"] = "1"
        session["mark"] = 0

    elif session["question"] not in questions:
        mark = session["mark"]
        score = mark
        return render_template("score.html")
    elif session["question"] in session:
        mark = session["mark"]
        score = mark
    return render_template("quiz.html",
                           question=questions[session["question"]]["question"],
                           question_number=session["question"],
                           options=questions[session["question"]]["options"],
                           score=session["mark"]
                           )
