from flask import g
import sqlite3
import traceback
import sys
# DB 
DATABASE = './APP/Database/mysql.db'
SCHEMA = './Database/mysql.sql'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def query_commit_db(query, args=(), one=False):
    try:
        db = get_db()
        if(one):
            db.execute(query, args)
        else:
            db.executemany(query, args)
        db.commit()
        return True
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        return False

