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
        

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM articles;"
        results = connectToMySQL(cls.db).query_db(query)
        articles = []
        for row in results:
            articles.append( cls(row))
        return articles


    @classmethod 
    def get_one(cls,data):
        query = "Select * FROM articles WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False 
        row = results[0]
        article = cls(row)
        return article

    @classmethod
    def get_u_one(cls,data):
        query = "Select * FROM articles WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False 
        article = []
        for row in results:
            article.append(cls(row))
        return article