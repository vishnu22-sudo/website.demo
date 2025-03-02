from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

USERS_FILE = 'data/users.xlsx'
os.makedirs('data', exist_ok=True)

if not os.path.exists(USERS_FILE):
    df = pd.DataFrame(columns=['username', 'password', 'email'])
    df.to_excel(USERS_FILE, index=False)

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        df = pd.read_excel(USERS_FILE)
        user = df[(df['username'] == username) & (df['password'] == password)]
        
        if not user.empty:
            session['user'] = username
            return redirect(url_for('home'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        df = pd.read_excel(USERS_FILE)
        if username in df['username'].values:
            flash('Username already exists')
            return redirect(url_for('register'))
            
        new_user = pd.DataFrame([[username, password, email]], 
                              columns=['username', 'password', 'email'])
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_excel(USERS_FILE, index=False)
        
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)