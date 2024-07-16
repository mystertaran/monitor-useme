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

def normalize_job(job):
    return {
        'title': job['title'].strip().lower(),
        'link': job['link'].strip().lower(),
        'description': job['description'].strip()
    }

def are_jobs_equal(job1, job2):
    job1_norm = normalize_job(job1)
    job2_norm = normalize_job(job2)
    return (job1_norm['title'] == job2_norm['title'] and
            job1_norm['link'] == job2_norm['link'])

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
        current_jobs = fetch_jobs()
        app_logger.info(f"Fetched {len(current_jobs)} jobs.")
        
        new_jobs = []
        for current_job in current_jobs:
            if not any(are_jobs_equal(current_job, previous_job) for previous_job in previous_jobs):
                new_jobs.append(current_job)
            else:
                app_logger.info(f"Job already exists: {current_job['title']}")

        if new_jobs:
            notify_new_jobs(new_jobs)
            log_jobs(new_jobs)
            app_logger.info(f"Found {len(new_jobs)} new jobs.")
        else:
            app_logger.info("No new jobs")

        previous_jobs = current_jobs
        save_previous_jobs(previous_jobs)
    except Exception as e:
        error_logger.error(f"Error checking for new jobs: {e}")

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
