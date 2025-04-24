# SAMPLE CODE ONLY. NO FUNCTIONALITY YET
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your_email@example.com'
SENDER_PASSWORD = 'your_app_password'  # Use app password if using Gmail with 2FA

def send_email_with_pdf(to_email, pdf_data, session_id):
    try:
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = f"Your PhotoBooth Session PDF (Session ID: {session_id})"

        # Add a body text
        msg.attach(MIMEText('Thanks for using our PhotoBooth! Attached is your session PDF.', 'plain'))

        # Attach the PDF
        attachment = MIMEApplication(pdf_data, _subtype="pdf")
        attachment.add_header('Content-Disposition', 'attachment', filename=f'session_{session_id}.pdf')
        msg.attach(attachment)

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return True

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {e}")
        return False
