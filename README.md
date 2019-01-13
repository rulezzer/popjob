# popJob
PopJob is a recruitment portal made for the Web Technologies exam project at Parthenope University of Naples.<br/>
It allows you to set and confirm your skills to help companies filtering peoples with certain skills.<br/>
It's based on Flask, Bootstrap 4, MongoDB and good intentions :P

## Requirements

- Python3
- wkhtmltopdf (just for the CV export)

## How to install
Install the project requirements with
```
pip3 install -r requirements.txt
```
## Setting the MongoDB credentials 
In the app.py file you must edit the following lines with your preferred host and db name (running it in localhost is always a good choice before going for production)

```
app.config["MONGODB_SETTINGS"] = {
    'host': 'MY_HOST',
    'db': 'MY_DATABASE_NAME'
}
```

## Setting the Mail Server 
In the app.py file you must edit the following lines with your preferred mail service server to use features like password reset. Yes, you can also use Gmail.

```
app.config['SECRET_KEY'] = 'MY_SECRET_KEY'
app.config['MAIL_SERVER'] = 'MAIL_SERVER_ADDRESS'
app.config['MAIL_PORT'] = // Mail port depends also if you use TLS or not, just put the number
app.config['MAIL_USE_TLS'] = // Set it to True or False
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'MY_EMAIL_ADDRESS')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS', 'MY_EMAIL_PASSWORD')
```

## Run it!
By default the project will start on port 80 (<i>for this we need to be root</i>).<br />
If you wanna start it on another port change it in the app.py file.
```
sudo python3 main.py
```

Now sit down, open your browser and enjoy!
