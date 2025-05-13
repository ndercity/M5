import uuid
import io
import os
import tempfile
from db_functions import insert_photo_session, update_photo_session_status, get_photo_session_by_id
from email_utils import send_email_with_pdf
from fpdf import FPDF

# Step 1: Initialize session
def start_photo_session(email):
    session_id = str(uuid.uuid4())
    pdf_placeholder = b""  # placeholder until actual PDF is generated
    insert_photo_session(email, pdf_placeholder, status="waiting", session_id=session_id)
    print(f"[Session] Started session for {email} with ID {session_id}")
    return session_id

# Step 2: Finalize and send output
def finalize_session(session_id):
    session = get_photo_session_by_id(session_id)
    if not session:
        print(f"[Error] No session found with ID {session_id}")
        return False

    update_photo_session_status(session_id, "processing")

    email = session['email']
    photo_blob = session['pdf_data']  # Actually your saved PNG or JPEG image blob

    # Create temp image file from blob
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img_file:
            tmp_img_file.write(photo_blob)
            tmp_img_file_path = tmp_img_file.name

        pdf = FPDF(unit='pt', format=[1800, 1200])  # same size as your canvas
        pdf.add_page()
        pdf.image(tmp_img_file_path, x=0, y=0, w=1800, h=1200)

        pdf_bytes = pdf.output(dest='S').encode('latin1')

        # Cleanup temp image file
        os.remove(tmp_img_file_path)

    except Exception as e:
        print(f"[PDF ERROR] Failed to create PDF: {e}")
        update_photo_session_status(session_id, "failed")
        return False

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[Email] Attempt {attempt} to send PDF to {email}")
            send_email_with_pdf(email, pdf_bytes, session_id)
            update_photo_session_status(session_id, "sent")
            print(f"[Email] Sent successfully to {email}")
            return True
        except Exception as e:
            print(f"[Email] Failed attempt {attempt}: {e}")

    update_photo_session_status(session_id, "failed")
    print(f"[Session] Failed to send after {max_retries} attempts for session {session_id}")
    return False