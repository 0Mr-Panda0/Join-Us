import sqlite3
from faker import Faker
import os
import re


def configuring_database():
    # Configure SQLite connection
    db_path = "data/database.db"

    # Check if the data directory exists, if not create it
    if not os.path.exists("data"):
        os.mkdir("data")

    db = sqlite3.connect(db_path, check_same_thread=False)
    return db


# Creating the users table if it doesn't exist, with UNIQUE email
def users_table_creation():
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        email TEXT UNIQUE)
                """)
    cursor.close()
    db.close()


def is_valid_email(email):
    # Simple regex for email validation
    if not isinstance(email, str):
        return False
    regex = r"^[A-Za-z0-9\.\+\-_]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}$"
    return re.match(regex, email) is not None


def email_exists(email):
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    exists = cursor.fetchone() is not None
    cursor.close()
    db.close()
    return exists


def count_users():
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return count


def insert_fake_email():
    db = configuring_database()
    cursor = db.cursor()
    fake = Faker()
    for i in range(500):
        email = fake.email()
        try:
            cursor.execute("INSERT INTO users (email) VALUES (?)", (email,))
            db.commit()
        except sqlite3.IntegrityError:
            pass  # Skip duplicates
    cursor.close()
    db.close()


def insert_email(email):
    if not is_valid_email(email):
        raise ValueError("Invalid email format")
    if email_exists(email):
        raise ValueError("Email already exists")
    db = configuring_database()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (email) VALUES (?)", (email,))
        db.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Email already exists")
    finally:
        cursor.close()
        db.close()
