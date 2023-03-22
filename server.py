
from flask import Flask
from flask import request
from assembler import run_mohican

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
    with open("adver.html", 'w') as f:
        f.write("""
                <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div id="main" style="margin: 50px; width: min-content;">
        @@
    </div>
</body>
<style>

    body, #main {
        width: 99%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-content: center;
        justify-content: center;
        background: white;
    }
</style>
</html>"

                """)
    run_mohican()
    
    return open('adver.html')

@app.route("/andu")
def login():
    username = request.args.get('a')
    password = request.args.get('b')
    
    return f"{username} {password}"

app.run(port=5000)
