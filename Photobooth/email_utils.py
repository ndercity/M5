import os
import socket
import dns.resolver
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')


def check_email(email):
    print("Checking email:", email)
    url = "https://mail7.net/emailchecker.html#emailCheck"
    data = {'email': email, 'submit': 'Check it'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=data, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    if soup.find('div', class_='alert alert-success'):
        return "OK"
    elif soup.find('div', class_='alert alert-danger') or soup.find('div', class_='alert alert-warning'):
        return "BAD"
    return "UNKNOWN"


def is_email_domain_valid(email):
    domain = email.split('@')[-1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return True if records else False
    except:
        return False


def send_email_with_pdf(to_email, pdf_data, session_id):
    try:
        # Sanity check: quick DNS and connectivity test
        socket.create_connection(("8.8.8.8", 53), timeout=3)  # Google's DNS
    except OSError:
        print("[NETWORK ERROR] No internet connection.")
        raise Exception("No internet connection")
    
    if not is_email_domain_valid(to_email):
        print("[EMAIL VALIDATION] Domain does not exist.")
        return False

    status = check_email(to_email)
    print(status, to_email)
    if status != "OK":
        print(f"[EMAIL VALIDATION] Email {to_email} rejected by mail7.net with status {status}. Not sending.")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = f"Your PhotoBooth Session PDF (Session ID: {session_id})"

        msg.attach(MIMEText('Thanks for using our PhotoBooth! Attached is your session PDF.', 'plain'))

        attachment = MIMEApplication(pdf_data, _subtype="pdf")
        attachment.add_header('Content-Disposition', 'attachment', filename=f'session_{session_id}.pdf')
        msg.attach(attachment)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return True

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {e}")
        return False
