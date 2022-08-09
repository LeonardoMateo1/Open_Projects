from flask_app.config.mysqlconnection import connectToMySQL
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Article:
    db = "crookedlion"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        