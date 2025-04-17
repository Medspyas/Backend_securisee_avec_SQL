from auth import authentication_user
from token_user import create_token, read_token
from view.gestion_cli import manage_create_user, manage_update_user, manage_delete_user, manage_assign_support
from view.commercial_cli import manage_create_client, manage_update_client, manage_create_contract, manage_update_contract, manage_get_contract_unsigned, manage_get_contract_unpaid, manage_create_event, manage_get_clients
from database import SessionLocal

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
       
        print("Authentification réussie.")
        create_token(user)
        user_infos = read_token()
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

    while True:
        print("\n--- Menu Gestion ---")
        print("1. Créer un utilisateur")
        print("2. Modifier un utilisateur")
        print("3. Supprimer un utilisateur" )
        print("4. Assigner un suport à un évènement")
        print("5. Quitter")

        choix = input("Choix: ")
        if choix == "1":
            manage_create_user()
        elif choix == "2":
            manage_update_user()
        elif choix == "3":
            manage_delete_user()
        elif choix == "4":
            manage_assign_support()    
        elif choix == "5":
            break
        else:
            print("Choix invalide.")




def commercial_menu(user_infos):
    while True:
        print("\n--- Menu Commercial ---")
        print("1. Créer un client")
        print("2. Modifier un client")
        print("3. Créer un contrat" )
        print("4. Modifier un contrat")
        print("5. Afficher les contrats non signés")
        print("6. Afficher les contrats non payés")
        print("7. Créer un évènement")
        print("8. Voir mes clients")
        print("9. Quitter")

        choix = input("Choix: ")
        if choix == "1":
            manage_create_client(user_infos)
        elif choix == "2":
            manage_update_client(user_infos)
        elif choix == "3":
            manage_create_contract(user_infos)
        elif choix == "4":
            manage_update_contract(user_infos)    
        elif choix == "5":
            manage_get_contract_unsigned(user_infos)
        elif choix == "6":
            manage_get_contract_unpaid(user_infos)
        elif choix == "7":
            manage_create_event(user_infos)
        elif choix == "8":
            manage_get_clients(user_infos)
        elif choix == "9":
            break
        else:
            print("Choix invalide.")

def support_menu():
    pass




    



