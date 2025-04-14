from auth import authentication_user
from token_user import create_token, read_token


def main_menu():
    user_infos = read_token()

    if not user_infos:
        print("Connexion requise.")
        email = input("Votre email: ")
        password = input("Votre mot de passe: ")
        user = authentication_user(email, password)
        
        if isinstance(user, str):
            print(user)
            return
        else:
            print("Authentification réussie.")
            create_token(user)
            user_info = read_token()
    if user_infos:
        menu_by_role(user_infos)

def menu_by_role(user_infos):
    role = user_infos["role"]
    print(f"Menu {role}.")

    if role == "gestion":
        gestion_menu()
    elif role == "commercial":
        commercial_menu()
    elif role == "support":
        support_menu()
    else:
        print("Role inconnu.")


def gestion_menu():
    pass

def commercial_menu():
    pass

def support_menu():
    pass




    



