from flask import Flask, render_template, redirect, request, url_for, flash
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
    return render_template("dm2.html")

@app.route("/player")
def PlayerSide():
    return render_template("player.html")

@app.route("/button")
def button():
    return "<button>Click Here!</button>"

@app.route('/run_script', methods=['POST'])
def run_script():
    # Run your Python script here
    object_type = request.form["type"]
    match object_type:
        case "image":    
            object_name = request.form["object_name"]
            path = "5etools/MM/" + object_name + ".png"
            # payload = {"filepath":path, "view":True}
            subprocess.run(['python', 'App\current\Sending_Test_Data.py',"image",path])
        case "feature":
            # feature("./5etools/data/spells/spells-phb.json","Magic Missile", True)
            class_name = request.form["class_name"]
            path = f'./5etools/data/class/class-{class_name.lower()}.json'
            feature_name = request.form["feature_name"]
            subprocess.run(['python', 'App\current\Sending_Test_Data.py',"feature",path,feature_name])
            pass
        case "spell":
            pass
        case "feat":
            pass
        case "roll":
            pass
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