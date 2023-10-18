from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

users_file = "user.json"

def load_users():
    try:
        with open(users_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user(username, password):
    users = load_users()
    users[username] = password
    with open(users_file, 'w') as f:
        json.dump(users, f)
        
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username not in users:
            error = "User not found!"
        elif users[username] != password:
            error = "Incorrect password!"
        else:
            return redirect(url_for('home'))

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users:
            error = "Username already exists!"
        else:
            save_user(username, password)
            return redirect(url_for('login'))

    return render_template('register.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
