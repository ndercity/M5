import sys
import os
import threading
import time
from mfrc522 import SimpleMFRC522 #uncomment this in raspi

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import db_functions as dbf

class AppState:
    def __init__(self):
        self.current_rfid = None
        self.current_rfid_status = None

    def set_rfid(self, rfid_key):
        self.current_rfid = rfid_key
        self.current_rfid_status = dbf.get_rfid_status(rfid_key)

    def get_current_rfid_details(self):
        return self.current_rfid, self.current_rfid_status
    
    def clear_details(self):
        self.current_rfid = None
        self.current_rfid_status = None

    def manipulate_rfid(self, rfid, isUpdate):
        if dbf.verify_rfid(rfid):
            if isUpdate:
                dbf.update_rfid_key(rfid, True)
            elif not isUpdate:
                dbf.update_rfid_key(rfid, False)
        else:
            dbf.insert_rfid_key(rfid)

class RFID_Logic:
    def __init__(self, on_scan_callback):
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