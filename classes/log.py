from classes.database import Database

class Log:

    def __init__(self):
        self.db = Database()

    def add(self, client_id, status):
        query = "INSERT INTO logs (client_id, status) VALUES (%s, %s)"
        return self.db.insert(query, [client_id, status])