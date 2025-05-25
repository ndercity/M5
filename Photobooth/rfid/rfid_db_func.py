import sqlite3
import os

DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'photobooth.db'))

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with get_db() as db:
        schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'schema.sql'))
        with open(schema_path, 'r') as f:
            db.executescript(f.read())
        db.commit()

def insert_rfid_key(name, contact, key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO rfid_db (admin_name, contact_number, rfid_key) VALUES (?,?,?)', (name, contact, key))
    db.commit()

def update_rfid_key(name, contact, key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE rfid_db SET admin_name = ?, contact_number = ? WHERE rfid_key = ?', 
                   (name, contact, key))
    db.commit()

def update_rfid_key_activation(key, isActivated):
    db = get_db()
    cursor = db.cursor()
    activate_value = None
    if isActivated:
        activate_value = 'activated'
    else:
        activate_value = 'deactivated'
    cursor.execute('UPDATE rfid_db SET status = ? WHERE rfid_key = ?', (activate_value, key))
    db.commit()


def verify_rfid(key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM rfid_db WHERE rfid_key = ?', (key,))
    db.commit()
    row = cursor.fetchone()

    if row:
        return True
    else:
        return False

def get_rfid_status(key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT status FROM rfid_db WHERE rfid_key = ?', (key,))
    db.commit()
    row = cursor.fetchone()
    return row['status'] if row else None

def get_admin_details(key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT admin_name, contact_number, status FROM rfid_db WHERE rfid_key = ?', (key,))
    return cursor.fetchone()  


def get_all_customer_details(key, offset, limit):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT 
            ps.email,
            ps.session_id,
            cd.customer_name,
            ps.status,
            ps.created_at
        FROM 
            photo_sessions ps
        JOIN 
            cust_db cd ON ps.cust_id = cd.id
        WHERE 
            cd.rfid_key = ?
        ORDER BY 
            ps.created_at DESC
        LIMIT ? OFFSET ?;
        ''', (key, limit, offset))
    return cursor.fetchall()  

def get_customer_name(key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT
            cd.customer_name, cd.use_status
        FROM
            cust_db cd
        JOIN
            rfid_db rd ON rd.rfid_key = cd.rfid_key
        WHERE
            rd.status = 'activated' AND cd.use_status = 'in use' AND cd.rfid_key = ?;
        ''', (key,))
    result = cursor.fetchone()
    return result

def use_rfid_card(name, key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO cust_db (customer_name, rfid_key) VALUES(?,?)', (name, key))
    db.commit()

def void_rfid_card(name, key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
                UPDATE cust_db
                SET use_status	= 'idle'
                WHERE customer_name = ? AND rfid_key = ? AND use_status = 'in use';
                ''',  (name, key))
    db.commit()

def get_pdf_blob(session_id):
    """
    Retrieve PDF binary data from database for given session ID
    
    Args:
        session_id: The session identifier string
        
    Returns:
        bytes: Raw PDF binary data or None if not found
    """
    cursor = get_db().cursor()
    cursor.execute(
        'SELECT pdf_data FROM photo_sessions WHERE session_id = ?', 
        (session_id,)
    )
    row = cursor.fetchone()
    
    if not row or row[0] is None:
        return None
        
    # Convert whatever blob format we get to bytes
    pdf_data = row['pdf_data']
    if isinstance(pdf_data, memoryview):
        return pdf_data.tobytes()
    if isinstance(pdf_data, str):
        return pdf_data.encode('latin1')  # Fallback for text storage
    return bytes(pdf_data)

def get_photo_session_by_id(session_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM photo_sessions WHERE session_id = ?', (session_id,))
    row = cursor.fetchone()
    return dict(row) if row else None
