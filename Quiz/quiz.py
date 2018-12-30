from flask import Flask, render_template, request, Blueprint
import random, copy

quiz = Blueprint('quiz', __name__, template_folder='templates')

@quiz.route('/')
def home():
    return 0


original_questions = {
    # Format is 'question':[options]
    'Taj Mahal': ['Agra', 'New Delhi', 'Mumbai', 'Chennai'],
    'Great Wall of China': ['China', 'Beijing', 'Shanghai', 'Tianjin'],
    'Petra': ['Ma\'an Governorate', 'Amman', 'Zarqa', 'Jerash'],
    'Machu Picchu': ['Cuzco Region', 'Lima', 'Piura', 'Tacna'],
    'Egypt Pyramids': ['Giza', 'Suez', 'Luxor', 'Tanta'],
    'Colosseum': ['Rome', 'Milan', 'Bari', 'Bologna'],
    'Christ the Redeemer': ['Rio de Janeiro', 'Natal', 'Olinda', 'Betim']
}

questions = copy.deepcopy(original_questions)


def shuffle(q):
    """
 This function is for shuffling
 the dictionary elements.
 """
    selected_keys = []
    i = 0
    while i < len(q):
        current_selection = random.choice(list(q))
        if current_selection not in selected_keys:
            selected_keys.append(current_selection)
            i = i + 1
    return selected_keys


@quiz.route('/')
def quiz():
    questions_shuffled = shuffle(questions)
    for i in questions.keys():
        random.shuffle(questions[i])
    return render_template('quiz.html', q=questions_shuffled, o=questions)


@quiz.route('/quiz', methods=['POST'])
def quiz_answers():
    correct = 0
    for i in questions.keys():
        answered = request.form[i]
        if original_questions[i][0] == answered:
            correct = correct + 1
    return '<h1>Correct Answers: <u>' + str(correct) + '</u></h1>'

#
# if __name__ == '__main__':
#     app.run(debug=True)
