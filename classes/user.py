from classes.database import Database
from werkzeug.security import check_password_hash
from flask import session

class User:

    username = None
    password = None
    db = Database()

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):

        # Get the user
        user = self.db.fetchOne("SELECT password FROM users WHERE username = %s", (self.username))

        # Check if the user exists
        if user is None:
            return False

        if not check_password_hash(user['password'], self.password):
            return False

        return user

    @staticmethod
    def isLoggedIn():
        return 'username' in session

