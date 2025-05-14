import sqlite3
from flask import g
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'photobooth.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_connection(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
        db.executescript(f.read())
    db.commit()

def insert_photo_session(email, pdf_data, status='pending', session_id=None):
    import uuid
    if session_id is None:
        session_id = str(uuid.uuid4())
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO photo_sessions (email, pdf_data, status, session_id)
        VALUES (?, ?, ?, ?)
    ''', (email, pdf_data, status, session_id))
    db.commit()
    return session_id

def update_photo_blob(session_id, photo_blob):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        UPDATE photo_sessions
        SET pdf_data = ?
        WHERE session_id = ?
    ''', (photo_blob, session_id))
    db.commit()

def get_photo_session_by_id(session_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM photo_sessions WHERE session_id = ?', (session_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

def update_photo_session_status(session_id, status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE photo_sessions SET status = ? WHERE session_id = ?', (status, session_id))
    db.commit()

def delete_photo_session(session_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM photo_sessions WHERE session_id = ?', (session_id,))
    db.commit()

####################################################################
#RFID UTILS
####################################################################

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

