# popJob
PopJob is a recruitment CMS portal made  for a University's project.<br/>
It's based on Flask, Bootstrap 4, MongoDB and good intentions :P

## Requirements

- Python3
- pip3

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

## Run it!
By default the project will start on port 80 (<i>for this we need to be root</i>).<br />
If you wanna start it on another port change it in the app.py file.
```
sudo python3 main.py
```

Now sit down, open your browser and enjoy!
