from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
import re

DB = "login_and_reg_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password,created_at,updated_at) VALUES ( %(fname)s,%(lname)s,%(email)s,%(pw)s, NOW(), NOW());"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(DB).query_db(query, data)

        if len(result) < 1:
            return False

        return cls(result[0])

    @classmethod
    def email_exsists(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(DB).query_db(query, data)
        print(result)
        if result:
            return True
        
        if not result:
            return False

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(DB).query_db(query, data)
        print(result)
        return result

    # @classmethod
    # def is_authenticated(cls):
    #     query = "INSERT "

    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true

        if len(user['fname']) <= 2:
            flash("First name must be at least 2 characters.", "first_name_error")
            is_valid = False
        if len(user['lname']) <= 2:
            flash("Last name must be at least 2 characters.", "last_name_error")
            is_valid = False
        if len(user['email']) < 3:
            flash("Invalid email address!", 'email_error')
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user['pw']) <= 7:
            flash("Password must be atleast 8 characters long.", "password_error")
            is_valid = False
        if user['pw'] != user['pwc']:
            flash("Passwords dont match.", "password_confirmation_error")
            is_valid = False
        return is_valid