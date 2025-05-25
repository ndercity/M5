import sys
import cups
import os
import threading
import time
from mfrc522 import SimpleMFRC522 #uncomment this in raspi
import rfid_db_func as dbf
from fpdf import FPDF
from printer import print_pdf  # Import the new printing function
import tempfile
import subprocess

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
        if is_update == 'activated':
            dbf.update_rfid_key_activation(rfid, False)
        else:
            dbf.update_rfid_key_activation(rfid, True)


    ###################################
    # Customer Page Operations
    ##################################
    def get_customer_name(self, key):
        
        result = dbf.get_customer_name(key)

        if result:
            name, status = result
            return name, status
        else:
            name = "d"
            status = "idle"
            return name, status
    
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
    

    ##################################
    # Cards Operation
    ##################################
    def print_image_admin(self, session_id, print_copy=True):
        """
        Finalize a photo session by creating PDF and sending to printer/email
        Args:
            session_id: The session ID to finalize
            print_copy: Whether to print a physical copy
            email_copy: Whether to email a digital copy
        Returns:
            bool: True if all requested operations succeeded
        """
        #photo_blob = dbf.get_pdf_blob(session_id)

        session = dbf.get_photo_session_by_id(session_id)
        if not session:
            print(f"[Error] No session found with ID {session_id}")
            return False

        email = session['email']
        photo_blob = session['pdf_data']


        # Create PDF from the image blob
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img_file:
                tmp_img_file.write(photo_blob)
                tmp_img_file_path = tmp_img_file.name

            pdf = FPDF(unit='pt', format=[1800, 1200])
            pdf.add_page()
            pdf.image(tmp_img_file_path, x=0, y=0, w=1800, h=1200)
            pdf_bytes = pdf.output(dest='S').encode('latin1')

            # Cleanup temp image file
            os.remove(tmp_img_file_path)

        except Exception as e:
            print(f"[PDF ERROR] Failed to create PDF: {e}")
            #update_photo_session_status(session_id, "failed")
            return False

        # Track success status for both operations
        operations_success = {
            'print': print_copy,  # If not printing, consider it "successful"
        }

        # Printing operation
        if print_copy:
            print("[Print] Attempting to print...")
            operations_success['print'] = print_pdf(pdf_bytes)
            if not operations_success['print']:
                print("[Print] Printing failed")

        # Update session status based on operations
        if all(operations_success.values()):
            #update_photo_session_status(session_id, "completed")
            print(f"[Session] Successfully completed all operations for session {session_id}")
            return True
        elif any(operations_success.values()):
            #update_photo_session_status(session_id, "partial_complete")
            print(f"[Session] Some operations completed for session {session_id}")
            return True  # or False depending on your requirements
        else:
            #update_photo_session_status(session_id, "failed")
            print(f"[Session] All operations failed for session {session_id}")
            return False
        
    def is_printer_online(printer_name="Your_Printer_Name"):
        try:
            result = subprocess.run(["lpstat", "-p", printer_name], capture_output=True, text=True)
            output = result.stdout.strip()
            print("[DEBUG] lpstat output:", output)
            if "disabled" in output or "not connected" in output:
                return False
            return True
        except Exception as e:
            print(f"[Error] Could not check printer status: {e}")
            return False
        

    def get_printer_status(printer_name="test_printer"):
        conn = cups.Connection()
        printers = conn.getPrinters()

        if printer_name not in printers:
            print(f"[ERROR] Printer '{printer_name}' not found.")
            return None, None  # or consider raising an exception

        printer = printers[printer_name]
        state = printer.get('printer-state', None)                   # 3 = idle, 4 = printing, 5 = stopped
        reason = printer.get('printer-state-reasons', 'unknown')    # String or list of strings depending on CUPS version

        print(f"[DEBUG] State: {state}, Reason: {reason}")
        return state, reason




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