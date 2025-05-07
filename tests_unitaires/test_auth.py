import unittest
from unittest.mock import MagicMock, patch

from auth import authentication_user
from utils import hash_password

"""
    Tests unitaire pour le module d'authentification
    vérifie que l'authentification réussit avec des identifiants valides
    et échoue correctement avec des identifiants invalides.

"""


class TestAuthenticationUser(unittest.TestCase):

    @patch("auth.SessionLocal")
    def test_authentication_success(self, mock_session):
        user = MagicMock()
        user.email = "test1@mail.com"
        user.password = hash_password("abcd")
        user.role.value = "gestion"

        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = user

        mock_db = MagicMock()
        mock_db.query.return_value = mock_query

        mock_session.return_value = mock_db

        result_user, error = authentication_user("test1@mail.com", "abcd")

        self.assertIsNotNone(result_user)
        self.assertIsNone(error)
        self.assertEqual(result_user.email, "test1@mail.com")
        self.assertEqual(result_user.role.value, "gestion")

    @patch("auth.SessionLocal")
    def test_authentication_fail(self, mock_session):

        mock_query = MagicMock()
        mock_db = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session.return_value = mock_db

        mock_db.query.return_value = mock_query

        user, error = authentication_user("false@mail.com", "azer")

        self.assertIsNone(user)
        self.assertIsNotNone(error)


if __name__ == "__main__":
    unittest.main()
