import click
import ibm_db
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = ibm_db.connect(current_app.config["CONN_STR"], "", "")

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        ibm_db.close(db)


def init_db():
    db = get_db()
    ibm_db.exec_immediate(db, 'DROP TABLE IF EXISTS user')
    ibm_db.exec_immediate(db, 'DROP TABLE IF EXISTS expense')
    ibm_db.exec_immediate(
        db, """CREATE TABLE user (id INT NOT NULL GENERATED ALWAYS AS IDENTITY, name varchar(255) NOT NULL, username varchar(255) NOT NULL UNIQUE, email varchar(255) NOT NULL UNIQUE, password varchar(255) NOT NULL, balance DECIMAL NOT NULL DEFAULT 0, alert DECIMAL NOT NULL DEFAULT 0, PRIMARY KEY (id))""")
    ibm_db.exec_immediate(
        db, "CREATE TABLE expense (id INT NOT NULL GENERATED ALWAYS AS IDENTITY, user_id INT NOT NULL, category varchar(255) NOT NULL, amount DECIMAL NOT NULL, PRIMARY KEY (id))")
    ibm_db.exec_immediate(
        db, "ALTER TABLE Expense ADD CONSTRAINT Expense_fk0 FOREIGN KEY (user_id) REFERENCES User(id)")


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
