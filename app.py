from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

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
    return render_template('hello.html')

@app.route('/join', methods=['POST'])
def join():
    email = request.form['email']
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (email) VALUES (%s)", (email,))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)