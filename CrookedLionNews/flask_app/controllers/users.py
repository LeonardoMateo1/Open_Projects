from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.modules.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    users = User.get_all()
    print(users)
    return render_template("index.html", users=users)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    session['user_id'] = session['user_id']
    return render_template("dashboard.html", user= session['user_id'])

@app.route('/register', methods=["POST"])
def create_user():

    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    print(session['user_id'])

    return redirect('/login')