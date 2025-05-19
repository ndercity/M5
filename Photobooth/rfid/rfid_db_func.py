import sqlite3
import os

DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'photobooth.db'))

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with get_db() as db:
        with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
            db.executescript(f.read())
        db.commit()

def insert_rfid_key(key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO rfid_db (rfid_key) VALUES (?)', key)
    db.commit()

def update_rfid_key(key, isActivated):
    db = get_db()
    cursor = db.cursor()
    activate_value = None
    if isActivated:
        activate_value = 'activated'
    else:
        activate_value = 'deactivated'
    cursor.execute('UPDATE rfid_db SET status = ? WHERE rfid_key = ?', activate_value, key)
    db.commit()

def verify_rfid(key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM rfid_db WHERE rfid_key = ?', key)
    db.commit()
    row = cursor.fetchone()

    if row:
        return True
    else:
        return False

def get_rfid_status(key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT status FROM rfid_db WHERE rfid_key = ?', key)
    db.commit()
    row = cursor.fetchone()
    return row['status'] if row else None

