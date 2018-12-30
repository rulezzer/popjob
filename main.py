from app import app, db
import models
import views

from quiz.blueprint import quiz_blueprint
app.register_blueprint(quiz_blueprint, url_prefix='/quiz')

if __name__ == '__main__':
	app.secret_key = 'mysecret'
	app.run(host='0.0.0.0', port=int("80"))