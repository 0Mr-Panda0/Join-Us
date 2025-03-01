from flask import Flask, request, render_template, redirect, url_for
from mylib.database_conn import (
    users_table_creation,
    count_users,
    insert_fake_email,
    insert_email,
)
from faker import Faker


app = Flask(__name__)
fake = Faker()


@app.route("/")
def index():
    # Creating the users table if it doesn't exist
    users_table_creation()
    # Fetching the number of users in the users table
    count = count_users()
    if count == 0:
        # Inserting a fake email into the users table
        insert_fake_email()
    return render_template("hello.html", count=count)


@app.route("/join", methods=["POST"])
def join():
    # Getting the email from the form
    email = request.form["email"]
    # Inserting the email into the users table
    insert_email(email)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
