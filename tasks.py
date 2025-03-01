from invoke import task
import os


@task
def install(c):
    c.run("python -m pip install --upgrade pip && pip install -r requirements.txt")


@task
def setup(c):
    if not os.path.exists("data"):
        c.run("mkdir data")


@task
def test(c):
    c.run("python -m pytest -vv --cov=mylib test_app.py")


@task
def design(c):
    c.run("black *.py")


@task
def lint(c):
    c.run("pylint --disable=R,C --ignore-patterns=test_.*?py *.py")


@task(pre=[install, setup, test, design, lint])
def run(c):
    c.run("python app.py")
