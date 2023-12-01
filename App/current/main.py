from flask import Flask, render_template, redirect
import sys
import os
import subprocess

baseLocationStr = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(baseLocationStr)

app = Flask(__name__)

@app.route("/")
def Menu():
    return render_template("menu.html")

@app.route("/dm")
def DMSide():
    return render_template("dm.html")

@app.route("/player")
def PlayerSide():
    return render_template("player.html")

@app.route("/button")
def button():
    return "<button>Click Here!</button>"

@app.route('/run_script', methods=['POST'])
def run_script():
    # Run your Python script here
    subprocess.run(['python', 'Sending_Test_Data.py','picture'])
    return redirect("/dm")


@app.route("/test")
def test():
    file_path = baseLocationStr + "Sending_Test_Data.py"
    try:
      os.system(f'python {file_path}')
    except FileNotFoundError:
      print(f"Error: The file '{file_path}' does not exist.")
    return "is running"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)