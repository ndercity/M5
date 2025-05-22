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
        '''
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
                    break
            except Exception as e:
                print("RFID read error:", e)
            time.sleep(0.2)
        print("RFID read loop stopped.")
        '''
        print("RFID read loop started.")
        while True:
            with self.lock:
                if not self.active:
                    break
            try:
                id, _ = self.reader.read_no_block()  # Faster non-blocking read
                if id:
                    if str(id) != self.last_scanned_id:
                        print(f"RFID scanned: {id}")
                        self.last_scanned_id = str(id)
                        with self.lock:
                            self.active = False  # stop after successful new scan
                        break
                    else:
                        print("Same RFID scanned again, ignoring.")
            except Exception as e:
                print("RFID read error:", e)
            time.sleep(0.05)  # Reduce delay for more responsiveness
        print("RFID read loop stopped.")
        
    def turn_on_rfid(self):
        print("Starting RFID reader...")
        self.active = True
        self.thread = threading.Thread(target=self.read_loop, daemon=True)
        self.thread.start()

    def get_last_scan(self):
        print("scan value is now: ", self.last_scanned_id)
        return self.last_scanned_id

    def clear_scanned(self):
        self.last_scanned_id = None
        print("Cleared scan value is now: ", self.last_scanned_id)
