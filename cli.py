from auth import authentication_user
from token_user import create_token


def main_menu():
    print("----Bienvenu !----")
    print("Veuillez vous identifier")
    identifiant = input("id: ")
    mot_de_passe = input("Mot de passe: ")
    return identifiant , mot_de_passe


def main_user():
    email , mot_de_passe = main_menu()
    user = authentication_user(email, mot_de_passe)


    if isinstance(user, str):
        print(user)
        return
    

    create_token(user)



