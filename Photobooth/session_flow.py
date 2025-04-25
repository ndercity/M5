import uuid
import time
from db_functions import insert_photo_session, update_photo_session_status, get_photo_session_by_id
from email_utils import send_email_with_pdf  # hypothetical helper module for email sending

# Step 1: Initialize session
def start_photo_session(email):
    session_id = str(uuid.uuid4())
    pdf_placeholder = b""  # placeholder until actual PDF is generated
    insert_photo_session(email, pdf_placeholder, status="waiting", session_id=session_id)
    print(f"[Session] Started session for {email} with ID {session_id}")
    return session_id

# Step 2: Finalize and send output
def finalize_session(session_id, pdf_data):
    session = get_photo_session_by_id(session_id)
    if not session:
        print(f"[Error] No session found with ID {session_id}")
        return False

    update_photo_session_status(session_id, "processing")

    email = session['email']
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[Email] Attempt {attempt} to send PDF to {email}")
            send_email_with_pdf(email, pdf_data)
            update_photo_session_status(session_id, "sent")
            print(f"[Email] Sent successfully to {email}")
            return True
        except Exception as e:
            print(f"[Email] Failed attempt {attempt}: {e}")

    update_photo_session_status(session_id, "failed")
    print(f"[Session] Failed to send after {max_retries} attempts for session {session_id}")
    return False
