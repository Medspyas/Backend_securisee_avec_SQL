import re
from datetime import datetime
import bcrypt

def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_phone_number(phone):
    return bool(re.match(r"^0[1-9]\d{8}$", phone))

def get_valid_email():
    while True:
        email = input("Email: ")
        if is_valid_email(email):
            return email
        print("Adresse email invalide.")

def get_valid_phone_number():
    while True:
        phone = input("Téléphone: ")
        if is_valid_phone_number(phone):
            return phone
        print("Téléphone invalide.")

def is_valid_date(value, format="%d-%m-%Y %H:%M"):
    while True:
        date_str = input(value)
        try:
            return datetime.strptime(date_str, format)
        
        except ValueError:
            print("Format invalide.")    

    
def get_valid_integer(input_str):
    while True:
        value = input(input_str)
        if value.isdigit():
            return int(value)
        print("Veuillez entrer un nombre entier.")

def get_valid_float(value):
    while True:
        try:
            return float(input(value))
        except ValueError:
            print("Veuillez entrer un nombre decimal valide.")

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))



