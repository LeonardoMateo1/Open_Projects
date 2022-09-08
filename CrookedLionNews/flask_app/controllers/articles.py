from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.modules.user import User
from flask_app.modules.article import Article
from flask import flash

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

#Post Methods Below ------------------------------------------------------------------------------------------------------

@app.route('/c/art', method=['POST'])
def c_art():
    session['user_id'] = ['user_id']
    data = {
        "title": request.form['title'],
        "sum": request.form['sum'],
        "description": request.form['description'],
        "user_id": request.form['user_id']
    }
    Article.save(data)
    return redirect('/article/create')
