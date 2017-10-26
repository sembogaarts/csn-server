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

        return self.db.fetchOne("SELECT * FROM clients WHERE client_id = %s", [self.client_id])

    @staticmethod
    def setOnline(client_id):
        return Database().update("UPDATE clients SET online = 1 WHERE client_id = %s", [client_id])

    @staticmethod
    def setOffline(client_id):
        return Database().update("UPDATE clients SET online = 0 WHERE client_id = %s", [client_id])

    @staticmethod
    def all():
        return Database().fetchAll("SELECT * FROM clients")

    @staticmethod
    def get(client_id):
        return Database().fetchOne("SELECT * FROM clients WHERE client_id = %s", [client_id])

    @staticmethod
    def getLogs(client_id):
        return Database().fetchOne("SELECT * FROM logs WHERE client_id = %s", [client_id])

    @staticmethod
    def getHeartbeats(client_id):
        return Database().fetchOne("SELECT * FROM heartbeats WHERE client_id = %s", [client_id])

    @staticmethod
    def resetClients():
        return Database().update("UPDATE clients SET online = 0")