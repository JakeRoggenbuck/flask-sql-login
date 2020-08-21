from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from database import DataBase
import os

app = Flask(__name__)
DATABASE = DataBase()


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"


@app.route('/login', methods=['POST'])
def do_admin_login():
    username = request.form['username']
    password = request.form['password']
    command = "SELECT password FROM users WHERE username=?"
    data = DATABASE.read_db(command, (username,))
    if password == data[0][0]:
        return "Hello Boss!"
    else:
        return render_template('login.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
