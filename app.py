from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os
from faker import Faker

# Load environment variables from .env file
load_dotenv() 

app = Flask(__name__)
fake = Faker()

# Configure MySQL connection
db = mysql.connector.connect(
    host=os.getenv('HOST_NAME'),
    port=os.getenv('PORT'),
    user=os.getenv('USER_NAME'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE_NAME')
)

@app.route('/')
def index():
    cursor = db.cursor()
    # Creating the users table if it doesn't exist
    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY, 
                            email VARCHAR(255))
                   ''')
    # Inserting a fake email into the users table
    for i in range(10):
        cursor.execute("INSERT INTO users (email) VALUES (%s)", (fake.email(),))
        db.commit()
    # Fetching the number of users
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
    cursor.execute("INSERT INTO users (email) VALUES (%s)", (email,))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)