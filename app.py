from flask import Flask, render_template, request, session
from database import DataBase
from hashlib import sha256
import os

app = Flask(__name__)
DATABASE = DataBase()


def not_empty_login(username, password):
    """Check if user inputs are empty"""
    if username == "" or password == "":
        return False
    else:
        return True


def password_check(user_entry, db_entry):
    """Check hashed user imputted password agenst stored hash"""
    user_entry = sha256(user_entry.encode()).hexdigest()
    if user_entry == db_entry:
        return True
    else:
        return False


def get_db_password_entry(username):
    """Gets hash of password by username from database"""
    command = "SELECT password FROM users WHERE username=?"
    data = DATABASE.read_db(command, (username,))
    if data != []:
        return data[0][0]
    else:
        return None


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    username = request.form['username']
    password = request.form['password']
    if not_empty_login(username, password):
        if (db_password := get_db_password_entry(username)) is not None:
            if password_check(password, db_password):
                return render_template('secret_page.html', username=username)

    return render_template('login.html')


if __name__ == "__main__":
    # Add user - for testing
    password = sha256("testpassword".encode()).hexdigest()
    DATABASE.write("Jake", password)

    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
