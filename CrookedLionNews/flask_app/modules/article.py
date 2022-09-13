from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.modules import user
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Article:
    db = "crookedlion"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.sum = data['sum']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

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
    def get_art(cls,data):
        query = "SELECT articles.id, articles.title, articles.description, users.first_name, users.last_name FROM articles, users WHERE articles.id = %(id)s AND users.id = articles.user_id"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def get_u_one(cls,data):
        query = "Select * FROM articles WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False 
        articles = []
        for row in results:
            articles.append(cls(row))
        return articles

    @classmethod
    def create_art(cls,data):
        query = "INSERT INTO articles ( title, sum, description, user_id) VALUES (%(title)s, %(sum)s, %(description)s, %(id)s);"
        article = connectToMySQL(cls.db).query_db( query, data )
        return article