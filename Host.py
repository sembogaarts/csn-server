# Third Party
from flask import Flask
from flask import render_template, redirect, request, flash, session, url_for, jsonify
from flask_socketio import SocketIO, emit

# Classes
from classes.database import Database
from classes.user import User
from classes.client import Client

# Config
app = Flask(__name__)
app.secret_key = 'visionbeta'

# MySQL connection
db = Database()
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def start():
    if User.isLoggedIn():
        clients = Client.all()
        return render_template('dashboard.html', clients=clients)
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():

    # Credentials
    username = request.form['username']
    password = request.form['password']

    # Perform login
    user = User(username, password)
    userLogin = user.login()

    if userLogin:
        session['username'] = username
        session['password'] = password
        return redirect('/')
    else:
        return redirect(url_for('.start', messages='Foutief wachtwoord'))

@app.route('/client/add', methods=['GET', 'POST'])
def add_client_view():
    if request.method == 'GET':
        return render_template('client/client_add.html')
    else:
        name = request.form['name']
        client = Client(name)
        row = client.add()
        return jsonify(row)

@app.route('/client/<client_id>', methods=['GET'])
def show_client(client_id):
    client = Client.get(client_id)
    logs = Client.getLogs(client_id)
    return render_template('client/client_show.html', client=client, logs=logs)

@socketio.on('connect')
def client_online():
    client_id = request.args['client_id']
    Client.setOnline(client_id)

@socketio.on('disconnect')
def client_offline():
    client_id = request.args['client_id']
    Client.setOffline(client_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    socketio.run(app)
