from classes.client import Client

class Socket:

    def __init__(self):
        self.client = Client()
        self.sockets = {}

    def add(self, session_id, client_id):
        # Add client to socket dict
        self.sockets[client_id] = session_id
        # Set the client online
        self.client.setOnline(client_id)

    def remove(self, client_id):
        # Remove client from socket dict
        self.sockets.pop(client_id)
        # Set the client offline
        self.client.setOffline(client_id)

    def room(self, client_id):
        return self.sockets[client_id]