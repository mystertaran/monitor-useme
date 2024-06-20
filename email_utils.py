import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import FROM_EMAIL, EMAIL_PASSWORD, TO_EMAIL

# Konfiguracja logowania błędów
error_logger = logging.getLogger('error_logger')

def send_email(subject, body):
    try:
        msg = MIMEMultipart("alternative")
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject

        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)

        html_part = MIMEText(body, 'html')
        msg.attach(html_part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

        print("Email sent.")
    except Exception as e:
        error_logger.error(f"Error sending email: {e}")