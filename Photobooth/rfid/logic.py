import sys
import os
import threading
import time
from mfrc522 import SimpleMFRC522 #uncomment this in raspi
import rfid_db_func as dbf

class AppState:
    def __init__(self):
        self.current_rfid = None
        self.current_rfid_status = None

    def set_rfid(self, rfid_key):
        self.current_rfid = rfid_key
        self.current_rfid_status = dbf.get_rfid_status(rfid_key)

    def get_current_rfid_details(self):
        self.current_rfid_status = dbf.get_rfid_status(self.current_rfid)
        return self.current_rfid, self.current_rfid_status
    
    def clear_details(self):
        self.current_rfid = None
        self.current_rfid_status = None

    def manipulate_rfid(self, rfid, is_update):
        is_exist = dbf.verify_rfid(rfid) 
        if is_exist:
            if is_update:
                dbf.update_rfid_key(rfid, True)
            elif not is_update:
                dbf.update_rfid_key(rfid, False)
        elif not is_exist and not is_update:
            dbf.insert_rfid_key(rfid)
            dbf.update_rfid_key(rfid, False)
        elif not is_exist and is_update:
            dbf.insert_rfid_key(rfid)

class RFID_Logic:
    def __init__(self, on_scan_callback):
        dbf.get_db()
        self.reader = None
        self.thread = None
        self.on_scan_callback = on_scan_callback
        self.active = False
        self.lock = threading.Lock()

        self.reader = SimpleMFRC522() #tanggalin ang comment kapg gagawin na

    def read_loop(self):
        print("RFID read loop started.")
        while True:
            with self.lock:
                if not self.active:
                    break
            try:
                id, text = self.reader.read()
                if id:
                    self.on_scan_callback(str(id))
                    break
            except Exception as e:
                print("RFID read error:", e)
            time.sleep(0.2)

        print("RFID read loop stopped.")

    def turn_on_rfid(self):
        if not self.active:
            print("Starting RFID reader...")
            self.active = True
            self.thread = threading.Thread(target=self.read_loop, daemon=True)
            self.thread.start()

    def turn_off_rfid(self):
        print("Stopping RFID reader...")
        with self.lock:
            self.active = False