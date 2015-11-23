from flask import Flask
from flask import render_template
from flask import request
from flask import json

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def show_sign_up():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def sign_up():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _name and _email and _password:
        return json.dumps({'html': '<span>Word.</span>'})
    else:
        return json.dumps({'html': '<span>You messed up. Try again.</span>'})

    # TODO: Actually validate and add user into database.


if __name__ == "__main__":
    app.run()
