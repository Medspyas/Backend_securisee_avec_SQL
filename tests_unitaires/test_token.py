import unittest
from unittest.mock import patch, MagicMock, mock_open
from token_user import create_token, read_token



class TestCreateToken(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    @patch('jwt.encode')
    def test_create_token(self, mock_jwt_encode,  mock_open_file):
        user = MagicMock()
        user.id = 1
        user.email = 'test1@mail.com'
        user.role.value = 'gestion'

        mock_jwt_encode.return_value = "FAKE_JWT_TOKEN"

        create_token(user)

        mock_open_file.assert_called_once_with('.jwt_token', 'w')

        mock_open_file().write.assert_called_once_with("FAKE_JWT_TOKEN")

    @patch('builtins.open', new_callable=mock_open, read_data="FAKE_JWT_TOKEN")
    @patch('os.path.exists', return_value=True)
    @patch('jwt.decode')
    def test_read_token(self, mock_jwt_decode, mock_exists, mock_open_file):
        mock_jwt_decode.return_value = {
            "user_id" : 1,
            "email": "test1@mail.com",
            "rôle": "gestion"
        }

        infos, status = read_token()


        mock_open_file.assert_called_once_with(".jwt_token", 'r')

        mock_jwt_decode.assert_called_once()


        self.assertEqual(status, "ok")
        self.assertEqual(infos['email'], "test1@mail.com")
        self.assertEqual(infos['rôle'], "gestion")


    

if __name__ == '__main__':
    unittest.main()
