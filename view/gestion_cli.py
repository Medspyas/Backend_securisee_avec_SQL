from controls.gestion_manager import GestionManager
from controls.event_manager import EventManager
from controls.contract_manager import ContractManager
from controls.client_manager import ClientManager
from models.models import UserRole
from database import SessionLocal
from utils import *



def manage_create_user():
    db = SessionLocal()
    gestion_manager = GestionManager(db)
    try:
        valides_roles = ["gestion", "support", "commercial"] 
        print("\n--- Création d'un utilisateur ---")
        first_name = input("Prénom: ")
        last_name = input("Nom: ")
        email = get_valid_email()
        password = input("Mot de passe: ").strip()
        hashed_password = hash_password(password)
        while True:
            role = input("Rôle (gestion/support/commercial)").lower()
            if role in valides_roles:
                break
            print("Rôle invalide réessayez.")

        user = gestion_manager.create_user(first_name, last_name, email, hashed_password, role)

        if user: 
            print("Utilisateur Créé avec succès.")
        else:
            print("Echec : email deja existant")
    finally:
        db.close()


def manage_update_user():
    db = SessionLocal()
    gestion_manager = GestionManager(db)
    try:
        users = gestion_manager.get_all_users()

        print("Utilisateurs : ")
        for user in users:
            print(f"[{user.id}] {user.first_name} {user.last_name} - {user.role.value}")

        
        user_id = get_valid_integer("ID de l'utilisateur à modifier: ")

        if not any(e.id == user_id for e in users):
            print("ID introuvable.")
            return
       
        
        updated_data = {}
        while True:
            print("\n--- Que voulez-vous modifier ? ---")
            print("1. Prénom")
            print("2. Nom")
            print("3. email")
            print("4. Mot de passe")
            print("5. Rôle")
            print("6. Valider modification")
            print("7. Quittez")

            choix = input("Choix: ")
           

            if choix == "1":
                updated_data["first_name"] = input("Nouveau prénom: ")
            elif choix == "2":
                updated_data["last_name"] = input("Nouveau nom: ")
            elif choix == "3":
                updated_data["email"] = get_valid_email()
            elif choix == "4":
                new_password = input("Nouveau mot de passe").strip()
                updated_data["password"] = hash_password(new_password)
            elif choix == "5":
                role = input("Nouveau rôle (gestion/support/commercial): ").lower()
                if role not in ["gestion", "support", "commercial"]:
                    print("Rôle invalide.")
                    continue
                updated_data["role"] = role
            elif choix == "6":
                if not updated_data:
                    print("Aucune modification")                
                    return
                result = gestion_manager.updated_user(user_id, updated_data)
                if result:
                    print("Modification enregistrée.")
                else:
                    print("Utilisateur introuvable.")
                    break
            elif choix == "7":
                print("Modification terminé")
                break
            else:
                print("choix invalide.")
    finally:
        db.close()

def manage_delete_user():
    db = SessionLocal()
    gestion_manager = GestionManager(db)

    try:
        users = gestion_manager.get_all_users()
        if not users:
            print("Aucun utilisateur à supprimer")
            return
        
        print("\n Listes des utilisateurs: ")
        for user in users:
            print(f"[{user.id}] {user.first_name} {user.last_name} - {user.role.value}")   

        
        user_id = get_valid_integer("ID de l'utilisateur à supprimer: ")
        
        if not any(e.id == user_id for e in users):
            print("ID introuvable.")
            return
        
        confirm = input("Confirmer la suppression ? o/n: ").lower()

        

        if confirm != "o":
            print("Supression annulée")
            return
        
        result = gestion_manager.delete_user(user_id)
        if result:
            print("Utilisateur supprimé avec succès.")
        else:
            print("Utilisateur introuvable.")
    finally:
        db.close()

def manage_create_contract():
    db = SessionLocal()
    client_manager = ClientManager(db)
    contract_manager = ContractManager(db)
    gestion_manager = GestionManager(db)

    try:
        clients = client_manager.get_all_client()
        

        if not clients:
            print("Aucun client trouvé.")
            return

        print("\n--- Tous les clients ---")
        for c in clients:
            print(f"[{c.id}] {c.full_name} - Commercial ID {c.commercial_id} ")

        
        client_id = get_valid_integer("ID du client pour le contrat: ")

        if not any(e.id == client_id for e in clients):
            print("ID introuvable.")
            return
        
        users = gestion_manager.get_all_users()
        commerciaux = [u for u in users if u.role == UserRole.commercial]

        if not commerciaux:
            print("Aucun commercial trouvé.")
            return

        print("\n--- Tous les commerciaux ---")
        for u in commerciaux:
            print(f"[{u.id}] {u.first_name} - {u.last_name} - {u.email} ")

        commercial_id = get_valid_integer("ID du commercial à associer: ")

        if not any(u.id == commercial_id for u in commerciaux):
            print("ID introuvable.")
            return       
        
        
        total_amount = get_valid_float("Montant total (€): ")
        remaining_amount = get_valid_float("Montant restant à payer (€): ")
        
        
        status_input = input("Le contrat est-il signé ? (o/n): ").lower()
        status_contract = True if status_input == "o" else False

        


        contract = contract_manager.create_contract(
            client_id=client_id,
            commercial_id=commercial_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            status_contract=status_contract
        )

        if contract:
            print(f"Contrat créé avec succès (ID: {contract.id}).")
        else:
            print("Erreur lors de la création du contrat.")
    finally:
        db.close()


def manage_update_contract(user_infos):
    db = SessionLocal()
    contract_manager = ContractManager(db)
    client_manager = ClientManager(db)
    gestion_manager = GestionManager(db)
    try:    
        contracts = contract_manager.get_all_contracts()
        

        if not contracts:
            print("Vous n'avez aucun contrat à modifier.")
            return
        
        print("\n--- Vos contrats ---")
        for c in contracts:
            status = "Signé" if c.status_contract else "Non signé"
            print(
                f"[{c.id}] Client ID: {c.client_id} | Commercial ID: {c.commercial_id} "
                f" | Total: {c.total_amount}€ | Restant: {c.remaining_amount}€ | {status}"
                  )

        
        contract_id = get_valid_integer ("ID du contrat à modifier: ")

        if not any(e.id == contract_id for e in contracts):
            print("ID introuvable.")
            return
       
        updated_data = {}

        while True:
            print("\n Champ à modifier ")
            print("1. Montant total ")
            print("2. Montant restant à payer ")
            print("3. Status du contrats (signé / non signé ) ")
            print("4. Modifier client")    
            print("5. Modifier commercial ")                   
            print("6. Valider modifications ")
            print("7. Quittez ")
            
            
            choix = input("choix: ")

            if choix == "1":                
                updated_data["total_amount"] = get_valid_float("Montant total (€): ")                
            elif choix == "2":                
                updated_data["remaining_amount"] = get_valid_float("Montant restant à payer (€): ")                
            elif choix == "3":
                status_input = input("Le contrat est-il signé ? (o/n): ").lower()
                updated_data["status_contract"] = True if status_input == 'o' else False 
            elif choix == "4":    
                clients = client_manager.get_all_client()
                for c in clients:
                    print(f"[{c.id}] {c.full_name} - {c.email}") 
                new_client_id = get_valid_integer("Nouvel ID client: ")   
                if not any(c.id == new_client_id for c in clients):
                    print("Client introuvable.")
                    continue   
                updated_data['client_id'] = new_client_id   
            elif choix == "5":  
                users = gestion_manager.get_all_users()
                commerciaux = [u for u in users if u.role == UserRole.commercial]
                if not commerciaux:
                    print("Aucun commerciaux")
                    continue
                print("\n--- Liste des commerciaux ---")
                for u in commerciaux:
                    print(f"[{u.id}] {u.first_name} - {u.last_name} - {u.email}") 
                new_commercial_id = get_valid_integer("Nouvel ID commercial: ")   
                
                if not any(u.id == new_commercial_id for u in commerciaux):
                        print("Commercial introuvable.")
                        continue 
                
                updated_data['commercial_id'] = new_commercial_id
            elif choix == "6":
                if not updated_data:
                    print("Auncune modification")
                    return 
                result = contract_manager.update_contract(contract_id, updated_data)
                if result:
                    print("Modification enregistrée")
                else:
                    print("Contrat introuvable.")
                    break  
            elif choix == "7":
                print("Modification terminé.")
                break
            else:
                print("Choix invalide.")
    finally:
        db.close()


def manage_assign_support():
    db = SessionLocal()
    gestion_manager = GestionManager(db)
    event_manager = EventManager(db)

    try:
        events = event_manager.get_events_without_support()

        if not events:
            print("Tous les évènements ont déja un support assigné.")
            return
        
        print("\n Evenements sans support :")
        for event in events:
            print(f"[{event.id}] {event.event_name} ({event.event_date_start}) - Client ID : {event.client_id}")


        event_id = get_valid_integer("\n Entrez l' ID de l'évènement: ")
        
        
        users = gestion_manager.get_all_users()
        supports = [user for user in users if user.role.value == "support"]

        if not supports:
            print("Aucun support disponible.")
            return
        
        print("\n Utilisateurs support disponibles.")
        for user in supports:
            print(f"[{user.id}] {user.first_name} {user.last_name} - {user.email}")

        
        support_id = get_valid_integer("\nEntrez l'ID du support à assigner: ")
        
        
        result = gestion_manager.assign_support_to_event(event_id, support_id)

        if result:
            print("Support assigné à l'évenement.")
        else: 
            print("Echec: événement introuvable ou erreur ou erreur d'assignation")
    finally:
        db.close()