
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/") # ‘https://www.google.com/‘
def home():
    return """
        <body>
        <h1>Mohican!</h1>
        <a href='adver'>Click to see generated add!</a>
        <h3>Run "./gen.sh" if you see no add generated!</h3>
        </body>
"""

@app.route("/adi")
def adi():
    return "<body bgcolor='red'><h1>Adi!</h1></body>"

@app.route("/adver")
def adver():
    return open('adver.html')

@app.route("/andu")
def login():
    username = request.args.get('a')
    password = request.args.get('b')
    
    return f"{username} {password}"

app.run(port=5000)
