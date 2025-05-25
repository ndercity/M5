import sys
import os
import threading
import time
from mfrc522 import SimpleMFRC522 #uncomment this in raspi
import rfid_db_func as dbf

class AppState:
    def __init__(self):
        dbf.get_db()
        dbf.init_db()
        self.current_rfid = None
        self.current_rfid_status = None
        self.page_destination = None

    def set_page_destination(self, page):
        self.page_destination = page
    
    def get_page_destination(self):
        return self.page_destination

    def set_rfid(self, rfid_key):
        self.current_rfid = rfid_key
        self.current_rfid_status = dbf.get_rfid_status(rfid_key)

    def get_current_rfid_details(self):
        self.current_rfid_status = dbf.get_rfid_status(self.current_rfid)
        return self.current_rfid, self.current_rfid_status
    
    def get_rfid_details(self, key):
        result = dbf.get_admin_details(key)
        if result:
            name, cont_number, status = result
        else:
            name, cont_number, status = None, None, None
        return name, cont_number, status, self.current_rfid
    
    def clear_details(self):
        self.current_rfid = None
        self.current_rfid_status = None

    def verify_rfid_exist(self,key):
        is_exist = dbf.verify_rfid(key)
        return is_exist

    ###################################
    # Admin Page Operations
    ##################################
    def insert_admin(self, name, contact, key):
        dbf.insert_rfid_key(name,contact,key)

    def update_admin_details(self, name, contact, key):
        dbf.update_rfid_key(name,contact,key)

    def manipulate_rfid(self, rfid, is_update):
        if is_update:
            dbf.update_rfid_key_activation(rfid, True)
        elif not is_update:
            dbf.update_rfid_key_activation(rfid, False)


    ###################################
    # Customer Page Operations
    ##################################
    def get_customer_name(self, key):
        name = dbf.get_customer_name(key)
        return name
    
    def use_card(self, name, key):
        dbf.use_rfid_card(name, key)

    def void_card(self, name, key):
        dbf.void_rfid_card(name, key)

    ###################################
    # History Page Operations
    ###################################
    def get_customer_details(self, key, offset = 0, limit = 4):
        results = dbf.get_all_customer_details(key)
        #print(results)
        return results

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