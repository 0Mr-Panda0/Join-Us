from invoke import task


@task
def manage_dependency(c):
    c.run("uv sync")


@task
def test_code(c):
    c.run("uv run -m pytest -vv --cov=mylib test_main.py")


@task
def lint_and_format_code(c):
    c.run("uv run ruff check .")
    c.run("uv run ruff check --fix .")
    c.run("uv run ruff format .")


@task
def type_hints_check(c):
    c.run("uv run mypy .")


@task(pre=[manage_dependency, test_code, lint_and_format_code, type_hints_check])
def build(c):
    c.run("uv run main.py")
