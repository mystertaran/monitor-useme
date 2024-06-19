import os
from dotenv import load_dotenv

load_dotenv()

FROM_EMAIL = os.getenv("FROM_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
JOB_URL = "https://useme.com/pl/jobs/category/serwisy-internetowe,34/"
PREVIOUS_JOBS_FILE = 'previous_jobs.json'