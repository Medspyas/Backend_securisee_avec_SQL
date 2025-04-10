from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_USER = os.getenv('DATABASE_USER')

DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')

DATABASE_NAME = os.getenv('DATABASE_NAME')

SECRET_KEY = os.getenv('SECRET_KEY')

JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

TOKEN_FILENAME = os.getenv('TOKEN_FILENAME')

JWT_EXPIRATION_SECONDS = int(os.getenv('JWT_EXPIRATION_SECONDS'))