class Socket:

    def __init__(self):
        self.sockets = {}

    def add(self, session_id, client_id):
        # Add client to socket dict
        self.sockets[client_id] = session_id

    def remove(self, client_id):
        # Remove client from socket dict
        self.sockets.pop(client_id)

    def room(self, client_id):
        return self.sockets[client_id]