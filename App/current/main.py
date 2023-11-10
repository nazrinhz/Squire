from flask import Flask
import sys
import os

baseLocationStr = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(baseLocationStr)
import Sending_Test_Data

app = Flask(__name__)

@app.route("/dm")
def DMSide():
    return "Welcome, Dungeon Master!"

@app.route("/player<int:number>")
def PlayerSide(number):
    str2 = "Welcome, player "+str(number)
    return str2

@app.route("/button")
def button():
    return "<button>Click Here!</button>"

@app.route("/test")
def test():
    return baseLocationStr

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)