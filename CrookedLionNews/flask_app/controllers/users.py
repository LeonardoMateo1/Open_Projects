from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask import flash

@app.route("/")
def index():
    return render_template("index.html")