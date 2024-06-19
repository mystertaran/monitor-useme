import requests
from bs4 import BeautifulSoup
from config import JOB_URL

def fetch_jobs():
    response = requests.get(JOB_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = []
    jobs_section = soup.find('div', class_='jobs')
    for job in jobs_section.find_all('article', class_='job'):
        title = job.find('a', class_='job__title-link').text.strip()
        link = job.find('a', class_='job__title-link')['href']
        full_link = f"https://useme.com{link}"
        description = job.find('p').text.strip()
        jobs.append({'title': title, 'link': full_link, 'description': description})

    print(f"Fetched {len(jobs)} jobs.")
    return jobs