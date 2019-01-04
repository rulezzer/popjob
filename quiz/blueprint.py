import os
from app import db
from flask import Flask, session, render_template, url_for, redirect, request, flash, Blueprint
from flask_login import current_user, login_required
from models import User, Cskills
from datetime import datetime

quiz_blueprint = Blueprint('quiz', __name__, template_folder='templates')
quiz_blueprint.secret_key = os.urandom(24)

# Java questions
questions = {
    "1": {"question": "What is correct syntax for main method of a java class?", "options": ["public static int main(String[] args)", "public int main(String[] args)", "public static void main(String[] args)", "None of the above."],
          "answer": "public static void main(String[] args)"},
    "2": {"question": "What is the size of short variable?",
          "options": ['8 bit', '16 bit', '32 bit', '64 bit'], "answer": "16 bit"},
    "3": {"question": "What is the default value of byte variable?",
          "options": ['0', '0.0', 'null', 'undefined'], "answer": "0"},
    "4": {"question": "Which of the following is true about super class?",
          "options": ["Variables, methods and constructors which are declared private can be accessed only by the members of the super class.", "Variables, methods and constructors which are declared protected can be accessed by any subclass of the super class.",
                      "Variables, methods and constructors which are declared public in the superclass can be accessed by any class.", "All of the above."],
          "answer": "All of the above."},
    "5": {"question": "What is local variable?",
          "options": ["Variables defined inside methods, constructors or blocks are called local variables.", "Variables defined outside methods, constructors or blocks are called local variables.",
                      "Static variables defined outside methods, constructors or blocks are called local variables.", "None of the above."], "answer": "Variables defined inside methods, constructors or blocks are called local variables."},
    "6": {'question': "Can be constructor be made private?",
          "options": ["True.", "False."], "answer": "True."},
    "7": {'question': "What is true about a final class?",
          "options": ["class declard final is a final class.", "Final classes are created so the methods implemented by that class cannot be overridden.",
                      "It can't be inherited.", "All of the above."], "answer": "All of the above."},
    "8": {'question': "What invokes a thread's run() method?",
          "options": ["JVM invokes the thread's run() method when the thread is initially executed.", "Main application running the thread.",
                      "start() method of the thread class.", "None of the above."], "answer": "JVM invokes the thread's run() method when the thread is initially executed."},
    "9": {'question': "Deletion is faster in LinkedList than ArrayList.", "options": ["True.", "False."], "answer": "True."},
    "10": {'question': "Which of the following is Faster, StringBuilder or StringBuffer?",
           "options": ["StringBuilder ", "StringBuffer", "Both of the above.", "None of the above."], "answer": "StringBuilder"}}


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
                  score = session["mark"]
                  perc = score * 100 / 40
                  if perc > 70:
                      print(User.objects(email=current_user.email, kskills__skillName__exact="java"))
                      x = User.objects(email=current_user.email).first()
                      print(x.name)
                      # utente = User.ob
                      x(kskills__skillName__exact="java").update(set__kskills__skillName_status=True, set__kskills__skillName_date=datetime.now())
                  return render_template("score.html", score=session["mark"], perc=score * 100 / 40)

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
