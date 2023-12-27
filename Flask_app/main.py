from flask import Flask, render_template, request, flash

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "Password"


@app.route("/")
def index():
    flash("Please submit file")
    return render_template("base.html")


@app.route("/replay_uploaded", methods=["POST"])
def replay_uploaded(): #this is the name of the action in the html
    flash('Replay "' + request.form["replay_name"] + '" submitted successfully') #request.form["blah"] captures the input from the form name
    return render_template("replay.html")


app.run(debug=True)
