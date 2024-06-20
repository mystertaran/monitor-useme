import unittest
import random
import string
from unittest.mock import patch, MagicMock
from main import check_for_new_jobs

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_random_job_link():
    title = generate_random_string(50)
    job_id = random.randint(10000, 99999)
    return f"https://useme.com/pl/jobs/{title},{job_id}/"

class TestMain(unittest.TestCase):

    @patch('main.fetch_jobs')
    @patch('main.load_previous_jobs')
    @patch('main.save_previous_jobs')
    @patch('main.notify_new_jobs')
    @patch('main.log_jobs')
    def test_check_for_new_jobs(self, mock_log_jobs, mock_notify_new_jobs, mock_save_previous_jobs, mock_load_previous_jobs, mock_fetch_jobs):
        
        mock_load_previous_jobs.return_value = []
        
        
        random_link_1 = generate_random_job_link()
        random_link_2 = generate_random_job_link()

        mock_fetch_jobs.return_value = [
            {'title': 'Test Job 1', 'link': random_link_1, 'description': 'Job description 1'},
            {'title': 'Test Job 2', 'link': random_link_2, 'description': 'Job description 2'}
        ]
        
        
        check_for_new_jobs()
        
        mock_notify_new_jobs.assert_called_once()
        mock_log_jobs.assert_called_once()
        mock_save_previous_jobs.assert_called_once_with(mock_fetch_jobs.return_value)

if __name__ == '__main__':
    unittest.main()
