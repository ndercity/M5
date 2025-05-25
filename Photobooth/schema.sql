CREATE TABLE IF NOT EXISTS photo_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    pdf_data BLOB,
    status TEXT NOT NULL,
    session_id TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    rfid_key VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS rfid_db (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_name TEXT NOT NULL,
    contact_number VARCHAR DEFAULT '0',
    rfid_key VARCHAR NOT NULL,
    status TEXT DEFAULT 'activated'
);

CREATE TABLE IF NOT EXISTS cust_db (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    rfid_key VARCHAR NOT NULL,
    use_status TEXT DEFAULT 'in use',
    session_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
