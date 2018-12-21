from app import app
import views

if __name__ == '__main__':
	app.secret_key = 'mysecret'
	app.run(host='0.0.0.0', port=int("80"))