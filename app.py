from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DB_NAME = 'users.db'

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('homepage'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(f"Submitted username: {username}, password: {password}")  # for checking

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result and result[0] == password:
        session['username'] = username
        return redirect(url_for('homepage'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('index'))
        except:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/homepage')
def homepage():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('homepage.html', username=session['username'])



@app.route('/schedule')
def schedule():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('schedule.html')

@app.route('/task')
def task():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('task.html')

@app.route('/timeblocking')
def timeblocking():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('timeblocking.html')

@app.route('/priority')
def priority():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('priority.html')

@app.route('/reminder')
def reminder():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('reminder.html')

@app.route('/adjustments')
def adjustments():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('adjustments.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

