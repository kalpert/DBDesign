from flask import Flask
from flask import render_template
from flask import request
from flask import json
from flask import session
from flask import redirect
from flask import url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time, timedelta
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
    if session.get('user'):
        return redirect('/userHome')
    else:
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
                return json.dumps({'redirect': url_for('sign_in')})
            else:
                return json.dumps({'error': str(data[0][0])}), 400
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'}), 400

    except Exception as e:
        return json.dumps({'redirect': url_for('error')}), 500
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

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.callproc('sp_getPostsOfConnectedUsers', (session.get('user'), 50))
        posts = cursor.fetchall()

        post_list = []

        for post in posts:
            post_dict = {
                'pid': post[0],
                'timestamp': post[1],
                'author': post[2],
                'body': post[3],
                'tags': post[4].split(',') if post[4] is not None else [],
                'favorites': post[5]
            }
            post_list.append(post_dict)
        return render_template('user-home.html', posts=post_list)
    else:
        return render_template('sign-in.html', error='Unauthorized Access')


@app.route('/friends')
def friends():
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users')
        people = cursor.fetchall()

        people_list = []

        for person in people:
            person_dict = {
                'id': person[0],
                'name': person[1],
                'email': person[2]
            }
            people_list.append(person_dict)

        return render_template('friends.html', people_list=people_list)
    else:
        return render_template('sign-in.html', error='Unauthorized Access')


@app.route('/friends/<pid>', methods=['POST'])
def add_friend(pid):
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.callproc('sp_connectUsers', (session.get('user'), pid))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'response': 'success'})

        else:
            return json.dumps({'response': 'error'}), 400


@app.route('/post', methods=['POST'])
def post():
    if session.get('user'):
        try:
            _user = session.get('user')
            _post = request.form['post']
            _tags = request.form.getlist('tags')
            _pid = 0

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_newPost', (_user, _post, _pid))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()

            cursor.close()

            cursor = conn.cursor()
            cursor.execute('SELECT @_sp_newPost_2')

            outParam = cursor.fetchall()
            cursor.close()

            if len(outParam) > 0:
                _id = outParam[0][0]
                cursor = conn.cursor()
                for _tag in _tags:
                    cursor.callproc('sp_createPostTopic', (_id, _tag))
                    data = cursor.fetchall()
                    if len(data) is 0:
                        conn.commit()
                return json.dumps({'response': 'success'})
            else:
                return json.dumps({'error': str(data[0])}), 400
        except Exception as e:
            return json.dumps({'redirect': url_for('error')}), 500
        finally:
            cursor.close()
            conn.close()


@app.route('/favorite/<pid>', methods=['POST'])
def favorite(pid):
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.callproc('sp_createFavorite', (session.get('user'), pid))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'response': 'success'})

        else:
            return json.dumps({'response': 'error'}), 400


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/error')
def error():
    return render_template('error', error='Sorry there was a problem with your request.')


@app.template_filter('date')
def date_filter(_date):
    if _date > datetime.now() - timedelta(seconds=60):
        return 'a few seconds ago'
    elif _date > datetime.now() - timedelta(minutes=15):
        return 'a few minutes ago'
    elif _date > datetime.combine(date.today(), time.min):
        return 'today'
    elif _date > datetime.combine(date.today(), time.min) - timedelta(days=1):
        return 'yesterday'
    else:
        return _date.strftime('%a %b %e %y')


if __name__ == "__main__":
    app.run()
