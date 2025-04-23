from auth import authentication_user
from token_user import create_token, read_token, logout
from view.gestion_cli import manage_create_user, manage_update_user, manage_delete_user, manage_assign_support
from view.commercial_cli import manage_create_client, manage_update_client, manage_create_contract, manage_update_contract, manage_get_contract_unsigned, manage_get_contract_unpaid, manage_create_event, manage_get_clients
from view.support_cli import manage_assigned_events, manage_update_event
from view.display_cli import view_all_clients, view_all_contracts, view_all_events
from database import SessionLocal

import sentry_sdk




sentry_sdk.init(
    dsn="https://b72b185fe485200e40908c89a9e04415@o4509196128092160.ingest.de.sentry.io/4509196145721424",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)



def main_menu():
    user_infos, status = read_token()

    if status == "expired":
        print("Session expiré. Veuillez vous reconnecter.")
    elif status == "invalid":
        print("Jeton corrompu. Veuillez vous reconnecter")
    elif status == "missing":
        print("Connexion requise.")

    if status != "ok":        
        email = input("Votre email: ")
        password = input("Votre mot de passe: ")
        user, error = authentication_user(email, password)
        
        if error:
            print(error)
            return
       
        print("Authentification réussie.")
        create_token(user)
        
        user_infos, status = read_token()
        if status != "ok":
            print("Erreur lors de la création du token")
            return
    
    menu_by_role(user_infos)

def menu_by_role(user_infos):
    role = user_infos["role"]
    print(f"Menu {role}.")

    if role == "gestion":
        gestion_menu(user_infos)
    elif role == "commercial":
        commercial_menu(user_infos)
    elif role == "support":
        support_menu(user_infos)
    else:
        print("Role inconnu.")


def gestion_menu(user_infos):   

    while True:
        print("\n--- Menu Gestion ---")
        print("1. Créer un utilisateur")
        print("2. Modifier un utilisateur")
        print("3. Supprimer un utilisateur" )
        print("4. Assigner un suport à un évènement")
        print("5. Voir tous les clients")
        print("6. Voir tous les contrats")
        print("7. Voir tous les événements")
        print("8. Quitter")

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
            view_all_clients()
        elif choix == "6":
            view_all_contracts()
        elif choix == "7":
            view_all_events()
        elif choix == "8":
            logout()
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
        print("9. Voir tous les clients")
        print("10. Voir tous les contrats")
        print("11. Voir tous les événements")
        print("12. Quitter")

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
            view_all_clients(user_infos)
        elif choix == "10":
            view_all_contracts(user_infos)
        elif choix == "11":
            view_all_events(user_infos)
        elif choix == "12":
            logout()
            break
        else:
            print("Choix invalide.")

def support_menu(user_infos):
     while True:
        print("\n--- Menu Support ---")
        print("1. Voir mes événements")
        print("2. Modifier un événement")
        print("3. Voir tous les clients")
        print("4. Voir tous les contrats")
        print("5. Voir tous les événements")       
        print("6. Quitter")

        choix = input("Choix: ")
        
        if choix == "1":
            manage_assigned_events(user_infos)
        elif choix == "2":
            manage_update_event(user_infos)
        elif choix == "3":
            view_all_clients(user_infos)
        elif choix == "4":
            view_all_contracts(user_infos)
        elif choix == "5":
            view_all_events(user_infos)
        elif choix == "6":
            logout()
            break
        else:
            print("Choix invalide")
        


if __name__ == '__main__':
    main_menu()

    



