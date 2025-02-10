from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from dotenv import load_dotenv
import os
from faker import Faker

# Load environment variables from .env file
load_dotenv() 

app = Flask(__name__)
fake = Faker()

# Configure SQLite connection
db_path = os.getenv('DATABASE_PATH', 'database.db')
db = sqlite3.connect(db_path, check_same_thread=False)

@app.route('/')
def index():
    cursor = db.cursor()
    # Creating the users table if it doesn't exist
    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            email TEXT)
                   ''')
    # Fetching the number of users in the users table if no users are present then anywhere from 10-100 users are added else the number of users is fetched
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:
        # Inserting a fake email into the users table
        for i in range(10):
            cursor.execute("INSERT INTO users (email) VALUES (?)", (fake.email(),))
            db.commit()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
    cursor.close()
    return render_template('hello.html', count=count)

@app.route('/join', methods=['POST'])
def join():
    # Getting the email from the form
    email = request.form['email']
    cursor = db.cursor()
    # Inserting the email into the users table
    cursor.execute("INSERT INTO users (email) VALUES (?)", (email,))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)