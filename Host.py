# Third Party
from flask import Flask
from flask import render_template, redirect, request, flash, session, url_for, jsonify
from flask_socketio import SocketIO, emit

# Classes
from classes.database import Database
from classes.user import User
from classes.client import Client
from classes.alarm import Alarm
from classes.socket import Socket

# Config
app = Flask(__name__)
app.secret_key = 'vision'

# Create instances
db = Database()
socket = Socket()
socketio = SocketIO(app)
alarm = Alarm()

# Boot the alarm
alarm.boot()

@app.route('/', methods=['GET'])
def start():
    if User.isLoggedIn():
        clients = Client.all()
        showWarning = False
        for client in clients:
            if client['online'] == 0:
                showWarning = True
        return render_template('dashboard.html', clients=clients, showWarning=showWarning, showStart=alarm.armed)
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
        client = Client()
        client.name = name
        row = client.add()
        return jsonify(row)

@app.route('/client/<client_id>', methods=['GET'])
def show_client(client_id):
    client = Client.get(client_id)
    logs = Client.getLogs(client_id)
    return render_template('client/client_show.html', client=client, logs=logs)

@app.route('/alarm', methods=['POST'])
def alarm_request():
    if request.form['go'] == 'off':
        alarm.cancel()
        alarm.armed = False
    else:
        alarm.waitToReconnect()
        alarm.armed = True
    return str('OK')

@app.route('/alarm/client', methods=['POST'])
def alarm_request_client():

    socketio.emit('alarm', request.form, room=socket.room(request.form['client_id']))

    return str('OK')

@socketio.on('connect')
def client_online():
    # Save variables
    client_id = request.args['client_id']
    # Add client to list
    socket.add(request.sid, client_id)
    # Recheck the alarm
    alarm.check()

@socketio.on('disconnect')
def client_offline():
    # Save variables
    client_id = request.args['client_id']
    # Add client to list
    socket.remove(client_id)
    # Recheck the alarm
    alarm.check()

@socketio.on('alarm')
def client_alarm(data):
    print(str(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    socketio.run(app)
