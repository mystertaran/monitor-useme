import unittest
from unittest.mock import patch, MagicMock
from email_utils import send_email
from config import FROM_EMAIL, EMAIL_PASSWORD, TO_EMAIL

class TestEmailUtils(unittest.TestCase):

    @patch('smtplib.SMTP', autospec=True)
    @patch('email_utils.FROM_EMAIL', new='test@example.com')
    @patch('email_utils.EMAIL_PASSWORD', new='testpassword')
    @patch('email_utils.TO_EMAIL', new='recipient@example.com')
    def test_send_email(self, mock_smtp):
       
        mock_server = mock_smtp.return_value.__enter__.return_value

        send_email("Test Subject", "Test Body")

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test@example.com', 'testpassword')
        mock_server.sendmail.assert_called_once()
        self.assertEqual(mock_server.sendmail.call_args[0][0], 'test@example.com')
        self.assertEqual(mock_server.sendmail.call_args[0][1], 'recipient@example.com')
        self.assertIn("Test Subject", mock_server.sendmail.call_args[0][2])
        self.assertIn("Test Body", mock_server.sendmail.call_args[0][2])

if __name__ == '__main__':
    unittest.main()
