from mylib.database_conn import *
from faker import Faker


def test_database_connection():
    db = configuring_database()
    assert db is not None, "Database connection failed"


def test_users_table_creation():
    db = configuring_database()
    table_name = "users"
    cursor = db.cursor()
    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    )
    result = cursor.fetchone()
    if result is None:
        assert False, "Table creation failed"
    else:
        assert True, "Table created successfully"
    cursor.close()


def test_insert_fake_email():
    count = count_users()
    insert_fake_email()
    if count_users() == count:
        assert False, "Inserting fake email failed"
    else:
        assert True, "Fake emails inserted successfully"
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id > 500")
    db.commit()
    cursor.close()
    db.close()


def test_insert_email():
    faker = Faker()
    email = faker.email()
    insert_email(email)
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("SELECT email FROM users WHERE email=?", (email,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    if result is None:
        assert False, "Inserting email failed"
    else:
        assert True, "Email inserted successfully"
