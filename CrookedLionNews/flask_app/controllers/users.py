from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.modules.user import User
from flask_app.modules.article import Article
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    users = User.get_all()
    articles = Article.get_all()
    return render_template("index.html", users=users, articles=articles)

@app.route('/login_register')
def login():
    return render_template("log_reg.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['user_id']
    }
    return render_template("dashboard.html", user= session['user_id'], users = User.get_one(data), articles=Article.get_all())

@app.route('/articles')
def article():
    if 'user_id' not in session:
        return render_template("articles.html", articles=Article.get_all())
    else:
        session['user_id'] = session['user_id']
        data = {
            "id" : session['user_id']
        }
        return render_template("m-articles.html", user= session['user_id'], users = User.get_one(data), articles=Article.get_all())

@app.route('/article/create')
def c_article():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            "id" : session['user_id']
        }
    return render_template("c-article.html",user= session['user_id'], users = User.get_one(data))

@app.route('/edit/articles')
def e_article():
    data = {
        "id" : session['user_id']
    }
    return render_template("y-articles.html", user= session['user_id'], users = User.get_one(data), articles=Article.get_u_one(data))

@app.route('/article/edit/<int:id>')
def edit(id):
    data = {
        "id" : id
    }
    return

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/articles/<int:id>/<string:title>')
def read(id,title):
    data = {
        "id" : id,
        "title" : title,
    }
    if 'user_id' not in session:
        return render_template("read_article.html", article=Article.get_one(data), user=User.get_one(data))
    session['user_id'] = session['user_id']
    return render_template("read_article.html", user= session['user_id'], article=Article.get_one(data), users=User.get_one(data))







@app.route('/register', methods=["POST"])
def create_user():
    if not User.validate_register(request.form):
        return redirect('/login_register')

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
        return redirect('/login_register')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/login_register')
    session['user_id'] = user.id
    return redirect('/dashboard')