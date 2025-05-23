import unittest
from unittest.mock import patch

from auth.auth import Auth


class TestUtils(unittest.TestCase):
    @patch("database.utils.Utils.get_username_by_email")
    def test_verify_email_exists_true(self, mock_get_username):
        mock_get_username.return_value = "test_user"
        self.assertTrue(Auth.verify_email_exists("user@example.com"))

    @patch("database.utils.Utils.get_username_by_email")
    def test_verify_email_exists_false(self, mock_get_username):
        mock_get_username.return_value = None
        self.assertFalse(Auth.verify_email_exists("nonexistent@example.com"))


if __name__ == "__main__":
    unittest.main()
