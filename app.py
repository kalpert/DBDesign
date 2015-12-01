from flask import Flask
from flask import render_template
from flask import request
from flask import json
from flaskext.mysql import MySQL

import config


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True


mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = config.DB_USER
app.config['MYSQL_DATABASE_PASSWORD'] = config.DB_PW
app.config['MYSQL_DATABASE_DB'] = config.DB_SCHEMA
app.config['MYSQL_DATABASE_HOST'] = config.DB_HOST
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/signUp', methods=['GET'])
def show_sign_up():
    return render_template('sign-up.html')


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


@app.route('/signIn', methods=['GET'])
def show_sign_in():
    return render_template('sign-in.html')


@app.route('/signIn', methods=['POST'])
def sign_in():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _email and _password:
        return json.dumps({'html': '<span>Word.</span>'})
    else:
        return json.dumps({'html': '<span>You messed up. Try again.</span>'})

        # TODO: Actually validate


if __name__ == "__main__":
    app.run()
