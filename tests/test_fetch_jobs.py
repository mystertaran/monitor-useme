import unittest
import re
import random
import string
import requests_mock
from fetch_jobs import fetch_jobs

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

class TestFetchJobs(unittest.TestCase):
    
    @requests_mock.Mocker()
    def test_fetch_jobs(self, m):
       
        random_link_1 = f"/pl/jobs/{generate_random_string(50)},{random.randint(10000, 99999)}/"
        random_link_2 = f"/pl/jobs/{generate_random_string(50)},{random.randint(10000, 99999)}/"

        # Symulowana zawartość HTML, która odzwierciedla strukturę strony Useme
        html_content = f"""
        <div class="jobs">
            <article class="job">
                <a class="job__title-link" href="{random_link_1}">Test Job 1</a>
                <p>Job description 1</p>
            </article>
            <article class="job">
                <a class="job__title-link" href="{random_link_2}">Test Job 2</a>
                <p>Job description 2</p>
            </article>
        </div>
        """
        # Symulowanie odpowiedzi HTTP dla URL Useme
        m.get('https://useme.com/pl/jobs/category/serwisy-internetowe,34/', text=html_content)

        # Wywołanie funkcji fetch_jobs, która ma być testowana
        jobs = fetch_jobs()

        # Sprawdzanie wyników
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0]['title'], 'Test Job 1')
        self.assertRegex(jobs[0]['link'], r'https://useme.com/pl/jobs/.*,\d+/')
        self.assertEqual(jobs[0]['description'], 'Job description 1')
        self.assertEqual(jobs[1]['title'], 'Test Job 2')
        self.assertRegex(jobs[1]['link'], r'https://useme.com/pl/jobs/.*,\d+/')
        self.assertEqual(jobs[1]['description'], 'Job description 2')

if __name__ == '__main__':
    unittest.main()