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

@app.route('/login_register')
def login():
    return render_template("log_reg.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    session['user_id'] = session['user_id']
    data = {
        "id" : session['user_id']
    }
    return render_template("dashboard.html", user= session['user_id'], users = User.get_one(data))

@app.route('/articles')
def article():
    users = User.get_all()
    print(users)
    return render_template("articles.html", users=users)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

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

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def log():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')