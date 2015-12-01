from flask import Flask
from flask import render_template
from flask import request
from flask import json
from flask import session
from flask import redirect
from flask import url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

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

app.secret_key = 'I miss the comfort in being sad.'


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/signUp', methods=['GET'])
def show_sign_up():
    return render_template('sign-up.html')


@app.route('/signUp', methods=['POST'])
def sign_up():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/signIn', methods=['GET'])
def show_sign_in():
    return render_template('sign-in.html')


@app.route('/signIn', methods=['POST'])
def sign_in():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return json.dumps({'redirect': url_for('user_home')})
            else:
                return json.dumps({'message': 'Wrong Email address or Password.'}), 401
        else:
            return json.dumps({'message': 'Wrong Email address or Password.'}), 401

    except Exception as e:
        return json.dumps({'redirect': url_for('error')}), 500
    finally:
        cursor.close()
        con.close()


@app.route('/userHome')
def user_home():
    if session.get('user'):
        return render_template('user-home.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/error')
def error():
    return render_template('error', error='Sorry there was a problem with your request.')


if __name__ == "__main__":
    app.run()
