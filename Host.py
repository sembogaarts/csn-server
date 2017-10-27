# Third Party
from flask import Flask
from flask import render_template, redirect, request, flash, session, url_for, jsonify
from flask_socketio import SocketIO

# Classes
from classes.user import User
from classes.client import Client
from classes.alarm import Alarm
from classes.socket import Socket
from classes.log import Log

# Config
app = Flask(__name__)
app.secret_key = 'vision'

# Create instances
socket = Socket()
socketio = SocketIO(app)
alarm = Alarm()

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
    # Check if it's a GET or POST request
    if request.method == 'GET':
        return render_template('client/client_add.html')
    else:
        # Add the client
        client = Client()
        client.name = request.form['name']
        row = client.add()
        return jsonify(row)

@app.route('/client/<client_id>', methods=['GET'])
def show_client(client_id):
    client = Client()
    client.client_id = client_id
    return render_template('client/client_show.html', client=client.get(), logs=client.logs())

@app.route('/alarm', methods=['POST'])
def alarm_request():
    action = request.form['turn']
    # Check what to do
    if action == 'off':
        alarm.cancel()
        alarm.armed = False
    elif action == 'on':
        alarm.waitToReconnect()
        alarm.armed = True
    return str('OK')

@app.route('/alarm/client', methods=['POST'])
def alarm_request_client():
    # Save variables
    data = request.form
    room = socket.room(request.form['client_id'])
    # Send alarm request to specific client
    socketio.emit('alarm', data, room=room)
    return str('OK')

@socketio.on('connect')
def socket_connect():
    # Save variables
    client_id = request.args['client_id']
    # Add client to list
    socket.add(request.sid, client_id)
    # Recheck the alarm
    alarm.check()

@socketio.on('disconnect')
def socket_disconnect():
    # Save variables
    client_id = request.args['client_id']
    # Add client to list
    socket.remove(client_id)
    # Recheck the alarm
    alarm.check()

@socketio.on('alarm')
def client_alarm(data):
    # Save variables
    client_id = request.args['client_id']
    status = data['status']
    # Create log
    log = Log()
    log.add(client_id, status)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    socketio.run(app)
