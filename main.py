from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

users_file = "user.json"

def load_users():
    try:
        with open(users_file, 'r') as f: # mo file json, "r" -read, f la bien doc file
            return json.load(f)  # tra ve gia tri cua file json
    except FileNotFoundError: # neu khong tim thay file thi tra ve mot dict rong
        return {}

def save_user(username, password):
    users = load_users()
    users[username] = password
    with open(users_file, 'w') as f: # "w" -write
        json.dump(users, f) # xoa noi dung cu, ghi noi dung moi vao file
        
@app.route('/') 
def index():
    return redirect(url_for('login')) # chuyen huong qua man login page

@app.route('/home')
def home():
    username = request.args.get('username') # lay gia tri cua username tu url
    return render_template('home.html', username=username)

@app.route('/login', methods=['GET', 'POST']) # neu khong co method thi mac dinh la GET
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username'] # lay gia tri cua username 
        password = request.form['password'] # lay gia tri cua password
        users = load_users() # load user tu file json

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
