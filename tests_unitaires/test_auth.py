import unittest
from unittest.mock import patch, MagicMock
from auth import authentication_user

class TestAuthenticationUser(unittest.TestCase):

    @patch('auth.SessionLocal')
    def test_authentication_success(self, mock_session):
        user = MagicMock()
        user.email = "test1@mail.com"
        user.password = "abcd"
        user.role.value = "gestion"


        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = user

        mock_db = MagicMock()
        mock_db.query.return_value = mock_query
        
        mock_session.return_value = mock_db


        user = authentication_user('test1@mail.com', 'abcd')

        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test1@mail.com')
        self.assertEqual(user.role.value, 'gestion')


    @patch('auth.SessionLocal')
    def test_authentication_fail(self, mock_session):

        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None

        mock_db = MagicMock()
        mock_db.query.return_value = mock_query

        user = authentication_user('false@mail.com', "azer")

        self.assertIsInstance(user, str)

if __name__ == '__main__':
    unittest.main()
