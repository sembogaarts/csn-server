from random import randint
from classes.database import Database

class Client:

    def __init__(self):
        self.db = Database()
        self.name = None
        self.client_id = None

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

    def setOnline(self, client_id):
        # SQL to update clients
        query = "UPDATE clients SET online = 1 WHERE client_id = %s"
        return self.db.update(query, [client_id])

    def setOffline(self, client_id):
        # SQL to update clients
        query = "UPDATE clients SET online = 0 WHERE client_id = %s"
        return self.db.update(query, [client_id])

    def get(self):
        # SQL to get the client
        query = "SELECT * FROM clients WHERE client_id = %s"
        client = self.db.fetchOne(query, [self.client_id])
        # Get latest log
        query = "SELECT status FROM logs WHERE client_id = %s ORDER BY id DESC LIMIT 1"
        status = self.db.fetchOne(query, [self.client_id])
        client['status'] = status['status']
        print(client)
        return client

    def logs(self):
        # SQL to get the client
        query = "SELECT * FROM logs WHERE client_id = %s ORDER BY id DESC LIMIT 5"
        return self.db.fetchAll(query, [self.client_id])

    @staticmethod
    def all():
        clients = Database().fetchAll("SELECT * FROM clients")
        for row in clients:
            query = "SELECT status FROM logs WHERE client_id = %s ORDER BY id DESC LIMIT 1"
            status = Database().fetchOne(query, [row['client_id']])

            row['status'] = status['status']
        return clients

    @staticmethod
    def resetClients():
        return Database().update("UPDATE clients SET online = 0")