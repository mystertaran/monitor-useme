import schedule
import time
import json
import os
import logging
from fetch_jobs import fetch_jobs
from email_utils import send_email
from config import PREVIOUS_JOBS_FILE, LOG_FILE, ERROR_LOG_FILE

# Konfiguracja logowania informacji
app_logger = logging.getLogger('app_logger')
app_logger.setLevel(logging.INFO)
app_handler = logging.FileHandler(LOG_FILE)
app_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
app_logger.addHandler(app_handler)

# Konfiguracja logowania błędów
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(ERROR_LOG_FILE)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
error_logger.addHandler(error_handler)

def load_previous_jobs():
    try:
        if os.path.exists(PREVIOUS_JOBS_FILE):
            with open(PREVIOUS_JOBS_FILE, 'r') as file:
                return json.load(file)
        return []
    except Exception as e:
        error_logger.error(f"Error loading previous jobs: {e}")
        return []

def save_previous_jobs(jobs):
    try:
        with open(PREVIOUS_JOBS_FILE, 'w') as file:
            json.dump(jobs, file)
    except Exception as e:
        error_logger.error(f"Error saving previous jobs: {e}")

def notify_new_jobs(new_jobs):
    try:
        subject = "Nowe zlecenia na USEME"
        body = "<html><body>"
        for job in new_jobs:
            body += f"""
            <table border="1" cellspacing="0" cellpadding="10" style="margin-bottom: 20px;">
                <tr><td><strong>{job['title']}</strong></td></tr>
                <tr><td><a href="{job['link']}">LINK</a></td></tr>
                <tr><td>{job['description']}</td></tr>
            </table>
            """
        body += "</body></html>"
        send_email(subject, body)
    except Exception as e:
        error_logger.error(f"Error sending email: {e}")

def log_jobs(jobs):
    for job in jobs:
        app_logger.info(f"[{job['title']}] {job['link']}")

def check_for_new_jobs():
    global previous_jobs
    try:
        app_logger.info("Checking for new jobs...")
        print("Checking for new jobs...")  
        current_jobs = fetch_jobs()
        app_logger.info(f"Fetched {len(current_jobs)} jobs.")

        new_jobs = [job for job in current_jobs if job not in previous_jobs]
        if new_jobs:
            notify_new_jobs(new_jobs)
            log_jobs(new_jobs)
            print(f"Found {len(new_jobs)} new jobs.")

        previous_jobs = current_jobs
        save_previous_jobs(previous_jobs)
    except Exception as e:
        error_logger.error(f"Error checking for new jobs: {e}")
        print(f"Error checking for new jobs: {e}")  

previous_jobs = load_previous_jobs()

if __name__ == '__main__':
    check_for_new_jobs()
    
    schedule.every(1).minutes.do(check_for_new_jobs)

    print("Starting job monitor...")
    app_logger.info("Job monitor started.")
    while True:
        try:
            schedule.run_pending()
            time.sleep(15)  
        except Exception as e:
            error_logger.error(f"Error in main loop: {e}")
            print(f"Error in main loop: {e}")  
