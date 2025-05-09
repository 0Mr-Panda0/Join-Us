import sqlite3
from faker import Faker
import os

def configuring_database():

    # Configure SQLite connection
    db_path = 'data/database.db'

    # Check if the data directory exists, if not create it
    if not os.path.exists(db_path):
        os.mkdir('data')

    db = sqlite3.connect(db_path, check_same_thread=False)
    return db

# Creating the users table if it doesn't exist
def users_table_creation():
    db = configuring_database()
    cursor=db.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        email TEXT)
                ''')
    cursor.close()
    db.close()

# Fetching the number of users in the users table
def count_users():
    db = configuring_database()
    cursor=db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return count

# Inserting a fake email into the users table
def insert_fake_email():
    db = configuring_database()
    cursor=db.cursor()
    fake = Faker()
    for i in range(500):
        cursor.execute("INSERT INTO users (email) VALUES (?)", (fake.email(),))
        db.commit()
    cursor.close()
    db.close()

# inserting the email into the users table
def insert_email(email):
    db = configuring_database()
    cursor=db.cursor()
    cursor.execute("INSERT INTO users (email) VALUES (?)", (email,))
    db.commit()
    cursor.close()
    db.close()



