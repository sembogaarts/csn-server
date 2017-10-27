import pymysql.cursors
from classes.config import config

class Database:

    connection = None
    cursor = None

    def __init__(self):

        self.connection = pymysql.connect(
            host=config.get('MYSQL', 'host'),
            user=config.get('MYSQL', 'user'),
            password=config.get('MYSQL', 'password'),
            db=config.get('MYSQL', 'database'),
        )

        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def fetchAll(self, query, values = []):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def fetchOne(self, query, values = []):
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def insert(self, query, values = []):
        self.cursor.execute(query, values)
        self.connection.commit()
        return True

    def update(self, query, values = []):
        self.cursor.execute(query, values)
        self.connection.commit()
        return True