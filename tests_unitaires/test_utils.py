from datetime import datetime

from utils import (
    check_password,
    get_valid_email,
    get_valid_float,
    get_valid_integer,
    get_valid_phone_number,
    hash_password,
    is_valid_date,
    is_valid_email,
    is_valid_phone_number,
)

"""
    Tests pour les fonctions utilitaires :
        - validation des emails, numéros, dates,
        - hash et vérification de mot de passe
        - conversion sécurisée des entrées utilisateur.

"""


def test_hash_password():
    password = "mypassword"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password


def test_check_password_valid():
    password = "mypassword"
    hashed = hash_password(password)
    assert check_password(password, hashed) is True


def test_check_password_invalid():
    password = "mypassword"
    hashed = hash_password(password)
    assert not check_password("wrong", hashed)


def test_is_mail_valid():
    assert is_valid_email("valid@mail.com")


def test_is_mail_invalid():
    assert is_valid_email("invalid@") is False


def test_is_phone_valid():
    assert is_valid_phone_number("0612345678")


def test_is_phone_invalid():
    assert is_valid_phone_number("123456") is False


def test_get_valid_email(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "test@mail.com")
    assert get_valid_email() == "test@mail.com"


def test_get_valid_phone(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0612345678")
    assert get_valid_phone_number() == "0612345678"


def test_get_valid_integer(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "42")
    assert get_valid_integer("Entrez un entier: ") == 42


def test_get_valid_float(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2.16")
    assert get_valid_float("Entrez un nombre décimal: ") == 2.16


def test_is_valid_date(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "24-04-2025 11:00")
    result = is_valid_date("Date: ")
    assert isinstance(result, datetime)
    assert result == datetime(2025, 4, 24, 11, 0)
