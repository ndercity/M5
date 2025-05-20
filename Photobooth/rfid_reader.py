from mfrc522 import SimpleMFRC522
import threading
import time

class RFID_Reader:
    def __init__(self):
        self.reader = SimpleMFRC522()
        self.thread = None
        self.active = False
        self.lock = threading.Lock()
        self.last_scanned_id = None

    def read_loop(self):
        print("RFID read loop started.")
        while True:
            with self.lock:
                if not self.active:
                    break
            try:
                id, text = self.reader.read()
                if id:
                    print(f"RFID scanned: {id}")
                    self.last_scanned_id = str(id)
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

    def get_last_scan(self):
        return self.last_scanned_id

    def clear_scanned(self):
        self.last_scanned_id = None
