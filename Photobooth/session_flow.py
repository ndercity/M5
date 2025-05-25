import uuid
import io
import os
import tempfile
from db_functions import insert_photo_session, update_photo_session_status, get_photo_session_by_id
from email_utils import send_email_with_pdf
from fpdf import FPDF
from printer import print_pdf, check_printer_status  # Import the new printing function

# Step 1: Initialize session
def start_photo_session(email, rfid_key):
    session_id = str(uuid.uuid4())
    pdf_placeholder = b""  # placeholder until actual PDF is generated
    insert_photo_session(email, pdf_placeholder, rfid_key, status="waiting", session_id=session_id)
    print(f"[Session] Started session for {email} with ID {session_id}")
    return session_id

def finalize_session(session_id, print_copy=True, email_copy=True):
    """
    Finalize a photo session by creating PDF and sending to printer/email
    Args:
        session_id: The session ID to finalize
        print_copy: Whether to print a physical copy
        email_copy: Whether to email a digital copy
    Returns:
        bool: True if all requested operations succeeded
    """
    status = get_printer_status()
    return jsonify({"status": status})

    session = get_photo_session_by_id(session_id)
    if not session:
        print(f"[Error] No session found with ID {session_id}")
        return False

    update_photo_session_status(session_id, "processing")

    email = session['email']
    photo_blob = session['pdf_data']

    return jsonify(check_printer_status())

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
        update_photo_session_status(session_id, "failed")
        return False

    # Track success status for both operations
    operations_success = {
        'print': not print_copy,  # If not printing, consider it "successful"
        'email': not email_copy   # If not emailing, consider it "successful"
    }

    # Printing operation
    if print_copy:
        print("[Print] Attempting to print...")
        operations_success['print'] = print_pdf(pdf_bytes)
        if not operations_success['print']:
            print("[Print] Printing failed")

    # Email operation
    if email_copy:
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                print(f"[Email] Attempt {attempt} to send PDF to {email}")
                sent = send_email_with_pdf(email, pdf_bytes, session_id)
                if sent:
                    operations_success['email'] = True
                    print(f"[Email] Sent successfully to {email}")
                    break
                else:
                    print(f"[Email] Sending failed (status false) on attempt {attempt}")
            except Exception as e:
                print(f"[Email] Failed attempt {attempt}: {e}")

    # Update session status based on operations
    if all(operations_success.values()):
        update_photo_session_status(session_id, "completed")
        print(f"[Session] Successfully completed all operations for session {session_id}")
        return True
    elif any(operations_success.values()):
        update_photo_session_status(session_id, "partial_complete")
        print(f"[Session] Some operations completed for session {session_id}")
        return True  # or False depending on your requirements
    else:
        update_photo_session_status(session_id, "failed")
        print(f"[Session] All operations failed for session {session_id}")
        return False