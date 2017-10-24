from classes.database import Database

class Heartbeat:

    db = Database()
    client_id = None

    def __init__(self, client_id):
        self.client_id = client_id

    def add(self):
        return self.db.insert("INSERT INTO `heartbeats` (client_id) VALUES (%s)", [self.client_id])
