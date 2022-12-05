import sqlite3

import click
from flask import current_app, g


def insert_schedule(data):
    con = get_db()

    try:
        with con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO schedule (name, link, time, category)
            VALUES (?, ?, ?, ?);
            """, data)
            con.commit()
    except sqlite3.Error as e:
        print(e)


def update_schedule(data):
    con = get_db()

    try:
        with con:
            cur = con.cursor()
            cur.execute("""
                UPDATE schedule
                SET name = ?, link = ?, date = ? category = ?
                WHERE id = ?
                """, data)
            con.commit()
    except sqlite3.Error as e:
        print(e)


def delete_schedule(data):
    con = get_db()

    try:
        with con:
            cur = con.cursor()
            cur.execute("""
                    DELETE FROM schedule 
                    WHERE id = ?
                    """, (data,))
            con.commit()
    except sqlite3.Error as e:
        print(e)


def get_all_schedule():
    res = []
    con = get_db()

    try:
        with con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT * FROM schedule
                ORDER BY id DESC;
                """
            )
            rows = cur.fetchall()

            for row in rows:
                column = []
                for col in row:
                    column.append(col)
                res.append(column)

    except sqlite3.Error as e:
        print(e)

    return res


def get_schedule(selection_id):
    res = []
    con = get_db()

    try:
        with con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT * FROM schedule
                where ID = ?;
                """, selection_id)
            rows = cur.fetchall()

            for row in rows:
                column = []
                for col in row:
                    res.append(col)
                res.append(column)

    except sqlite3.Error as e:
        print(e)

    return res


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
