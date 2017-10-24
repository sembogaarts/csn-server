# Third Party
from flask import Flask
from flask import render_template, redirect, request, flash, session, url_for

# Classes
from classes.database import Database
from classes.user import User
from classes.client import Client
from classes.heartbeat import Heartbeat

# Config
app = Flask(__name__)
app.secret_key = 'visionbeta'

# MySQL connection
db = Database()

@app.route('/', methods=['GET'])
def start():
    if User.isLoggedIn():
        clients = db.fetchAll("SELECT * FROM clients")
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

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    # Form Input
    client_id = request.form['client_id']
    heartbeat = Heartbeat(client_id)
    heartbeat.add()
    return str({'status': 'success'})

@app.route('/client', methods=['POST'])
def register_client():
    name = request.form['name']
    client = Client(name)
    client.add()
    return str({'status': 'success'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run()
