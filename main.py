import schedule
import time
import json
import os
from fetch_jobs import fetch_jobs
from email_utils import send_email
from config import PREVIOUS_JOBS_FILE

def load_previous_jobs():
    if os.path.exists(PREVIOUS_JOBS_FILE):
        with open(PREVIOUS_JOBS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_previous_jobs(jobs):
    with open(PREVIOUS_JOBS_FILE, 'w') as file:
        json.dump(jobs, file)

def notify_new_jobs(new_jobs):
    subject = "New Job Listings Available"
    body = "\n\n".join([f"{job['title']}: {job['link']}\n{job['description']}" for job in new_jobs])
    send_email(subject, body)

def check_for_new_jobs():
    global previous_jobs
    current_jobs = fetch_jobs()
    
    new_jobs = [job for job in current_jobs if job not in previous_jobs]
    if new_jobs:
        notify_new_jobs(new_jobs)
        print(f"Found {len(new_jobs)} new jobs.")
    
    previous_jobs = current_jobs
    save_previous_jobs(previous_jobs)

# Inicjalizacja poprzednich ogłoszeń
previous_jobs = load_previous_jobs()

# Harmonogram sprawdzania co 10 minut
schedule.every(10).minutes.do(check_for_new_jobs)

print("Starting job monitor...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Czekanie 60 sekund przed ponownym sprawdzeniem harmonogramu