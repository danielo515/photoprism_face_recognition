from types import SimpleNamespace
from config import config
import db_setup
from flask import g


def create_connection():
    (cnx, cursor) = db_setup.connect(**config['db_config'])
    g.db = SimpleNamespace(cnx=cnx, cursor=cursor)


def get_db():
    if 'db' not in g:
        create_connection()
    if(not g.db.cnx.is_connected()):
        print('Database reconected')
        create_connection()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.cursor.close()
        db.cnx.close()


def init_app(app):
    pass
    # app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)
