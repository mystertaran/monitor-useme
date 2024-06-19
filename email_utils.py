import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import FROM_EMAIL, EMAIL_PASSWORD, TO_EMAIL

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        
    print("Email sent.")