from random import randint
from classes.database import Database

class Client:

    db = Database()
    name = None
    client_id = None

    def __init__(self, name):
        self.name = name

    def add(self):

        # Generate random code
        unique = False

        while not unique:
            self.client_id = str(randint(10000, 99999))

            # Execute query
            row = self.db.fetchOne("SELECT * from clients where client_id=%s", [self.client_id])

            if row is None:
                unique = True

        self.db.insert("INSERT INTO clients (`name`, `client_id`) VALUES (%s, %s)", [self.name, self.client_id])