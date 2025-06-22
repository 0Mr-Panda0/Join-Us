from src.database_conn import (
    configuring_database,
    users_table_creation,
    count_users,
    insert_fake_email,
    insert_email,
)
from faker import Faker


def test_database_connection():
    db = configuring_database()
    assert db is not None, "Database connection failed"


def test_users_table_creation():
    users_table_creation()
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


def test_insert_duplicate_email():
    """Test inserting the same email twice (should fail if unique constraint)."""
    faker = Faker()
    email = faker.email()
    insert_email(email)
    db = configuring_database()
    cursor = db.cursor()
    try:
        insert_email(email)
    except ValueError:
        pass  # Expecting failure
    finally:
        cursor.execute("DELETE FROM users WHERE email=?", (email,))
        db.commit()
        cursor.close()
        db.close()


def test_insert_invalid_email():
    """Test inserting invalid emails (empty string, None)."""
    db = configuring_database()
    cursor = db.cursor()
    invalid_emails = ["", None]
    for email in invalid_emails:
        try:
            insert_email(email)
        except Exception:
            pass  # Expecting failure
        cursor.execute("SELECT * FROM users WHERE email IS ?", (email,))
        result = cursor.fetchone()
        assert result is None, f"Invalid email '{email}' was inserted!"
    cursor.close()
    db.close()


def test_count_users_direct():
    """Test count_users returns correct number after insert/delete."""
    db = configuring_database()
    cursor = db.cursor()
    initial_count = count_users()
    faker = Faker()
    email = faker.email()
    insert_email(email)
    assert count_users() == initial_count + 1, "User count did not increment"
    cursor.execute("DELETE FROM users WHERE email=?", (email,))
    db.commit()
    assert count_users() == initial_count, "User count did not decrement"
    cursor.close()
    db.close()


def test_insert_long_email():
    """Test inserting a very long email address."""
    long_email = "a" * 240 + "@example.com"
    insert_email(long_email)
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("SELECT email FROM users WHERE email=?", (long_email,))
    result = cursor.fetchone()
    cursor.execute("DELETE FROM users WHERE email=?", (long_email,))
    db.commit()
    cursor.close()
    db.close()
    assert result is not None, "Long email was not inserted"


def test_insert_special_char_email():
    """Test inserting an email with special characters."""
    special_email = "user+test!#$%&'*-/=?^_`{|}~@example.com"
    try:
        insert_email(special_email)
    except ValueError:
        pass  # Expecting failure
