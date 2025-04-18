from database import SessionLocal
from controls.event_manager import EventManager
from controls.client_manager import ClientManager
from controls.contract_manager import ContractManager
from models.models import Client, Contract
from datetime import datetime




def manage_create_client(user_infos):
    db = SessionLocal()
    client_manager = ClientManager(db)


    try:
        print("\n--- Création nouveau client")
        full_name = input("Nom complet: ")
        email = input("Email: ")
        phone = input("Téléphone: ")
        company_name = input("Nom de l'entreprise: ")
        commercial_id = user_infos['user_id']

        new_client = client_manager.create_client(full_name, email, phone, company_name, commercial_id)

        if new_client:
            print(f"Client créé avec succès : {new_client.full_name}")
        else:
            print("Erreur: Email ou téléphone déjà existant.")
    finally:
        db.close()
        
def manage_update_client(user_infos):
    db = SessionLocal()
    client_manager = ClientManager(db)

    try:
        clients = client_manager.get_all_client()
        clients = [c for c in clients if c.commercial_id == user_infos['user_id']]

        if not clients:
            print("Aucun à modifier.")
            return
        print("\n--- Vos clients ---")
        for c in clients:
            print(f"[{c.id}] {c.full_name} - {c.email}")
        try:
            client_id = int(input("ID du client à modifier: "))
        except ValueError:
            print("ID invalide.")
            return

        updated_data= {}

        while True:
            print("\n Champ à modifier ")
            print("1. Nom complet ")
            print("2. Email ")
            print("3. Téléphone ")
            print("4. Entreprise ")
            print("5. Valider modifications ")
            print("6. Quittez ")

            choix = input("choix: ")

            if choix == "1":
                updated_data["full_name"] = input("Nouveau Nom complet")
            elif choix == "2":
                updated_data["email"] = input("Nouvel email")
            elif choix == "3":
                updated_data["phone"] = input("Nouvel email")
            elif choix == "4":
                updated_data["company_name"] = input("Nouveau nom d'entreprise")
            elif choix == "5":
                if not updated_data:
                    print("Auncune modification")
                    return
                              
                result = client_manager.update_client(client_id, updated_data)

                if result:
                    print("Modification enregistrée")
                else:
                    print("Client introuvable.")
                    break   
            elif choix == "6":
                print("Modification terminé.")
                break
            else:
                print("Choix invalide.")                          
    finally:
        db.close()


def manage_create_contract(user_infos):
    db = SessionLocal()
    client_manager = ClientManager(db)
    contract_manager = ContractManager(db)

    try:
        clients = client_manager.get_all_client()
        clients = [c for c in clients if c.commercial_id == user_infos['user_id']]

        if not clients:
            print("Vous n'avez aucun client")
            return

        print("\n--- Vos clients ---")
        for c in clients:
            print(f"[{c.id}] {c.full_name} - {c.email}")

        try:
            client_id = int(input("ID du client pour le contrat: "))
        except ValueError:
            print("ID invalide.")
            return
        
        try :
            total_amount = float(input("Montant total (€): "))
            remaining_amount = float(input("Montant restant à payer (€): "))
        except ValueError:
            print("Montant invalide.")
            return
        
        status_input = input("Le contrat est-il signé ? (o/n): ").lower()
        status_contract = True if status_input == "o" else False

        commercial_id = user_infos["user_id"]


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

    try:
        contracts = contract_manager.get_all_contracts()
        contracts = [c for c in contracts if c.commercial_id == user_infos['user_id']]

        if not contracts:
            print("Vous n'avez aucun contrat à modifier.")
            return
        
        print("\n--- Vos contrats ---")
        for c in contracts:
            status = "Signé" if c.status_contract else "Non signé"
            print(f"[{c.id}] Client ID: {c.client_id} | Total: {c.total_amount}€ | Restant: {c.remaining_amount}€ | {status}")

        try:
            contract_id = int(input("ID du contrat à modifier: "))
        except ValueError:
            print("ID invalide.")
            return
        updated_data = {}

        while True:
            print("\n Champ à modifier ")
            print("1. Montant total ")
            print("2. Montant restant à payer ")
            print("3. Status du contrats (signé / non signé ) ")
            print("4. Valider modifications ")
            print("5. Quittez ")
            
            
            choix = input("choix: ")

            if choix == "1":
                try:
                    updated_data["total_amount"] = float(input("Montant total (€): "))
                except ValueError:
                    print("Montant invalide.")
            elif choix == "2":
                try:
                    updated_data["remaining_amount"] = float(input("Montant restant à payer (€): "))
                except ValueError:
                    print("Montant invalide.")
            elif choix == "3":
                status_input = input("Le contrat est-il signé ? (o/n): ").lower()
                updated_data["status_contract"] = True if status_input == 'o' else False        
            elif choix == "4":
                if not updated_data:
                    print("Auncune modification")
                    return
                result = contract_manager.update_contract(contract_id, updated_data)
                if result:
                    print("Modification enregistrée")
                else:
                    print("Contrat introuvable.")
                    break  
            elif choix == "5":
                print("Modification terminé.")
                break
            else:
                print("Choix invalide.")
    finally:
        db.close()


def manage_create_event(user_infos):
    db = SessionLocal()
    contract_manager = ContractManager(db)
    event_manager = EventManager(db)

    try:
        contracts = contract_manager.get_all_contracts(user_infos["user_id"])
        contracts = [c for c in contracts if c.status_contract is True] 

        if not contracts:
            print("Aucun contrats signé trouvé.")
            return
        print("\n--- Contrats signés disponibles ---")
        for c in contracts:
            print(f"[{c.id}] Client ID: {c.client_id} | Total: {c.total_amount}€ | Restant: {c.remaining_amount}€")
        try:
            contract_id = int(input("ID du contrat pour créer l'événement: "))
        except ValueError:
            print("ID invalide.")
            return
        
        client_id = next((c.client_id for c in contracts if c.id == contract_id), None)
        if client_id is None:
            print("Contrat non trouvé")
            return
        
        event_name = input("Nom de l'événement: ")
        location = input("Lieu: ")
        try:
            attendees = int(input("Nombre de participants: "))
        except ValueError:
            print("Nombre invalide.")
            return
        date_format = "%Y-%m-%d %H:%M"
        try : 
            date_start = input("Date et heure du début (YYYY-MM-DD HH:MM): ")
            date_end = input("Date et heure de fin (YYYY-MM-DD HH:MM): ")
            event_date_start = datetime.strptime(date_start, date_format)
            event_date_end = datetime.strptime(date_end, date_format)
        except ValueError:
            print("Mauvais format de date.")
            return
        notes = input("Notes eventuelles: ")

        new_event = event_manager.create_event(
            contract_id=contract_id,
            client_id=client_id,
            event_name=event_name,
            event_date_start=event_date_start,
            event_date_end=event_date_end,
            location=location,
            attendees=attendees,
            notes=notes,
            user_id=user_infos["user_id"]
        )

        if new_event:
            print("Evénement créé avec succès")
        else:
            print("Erreur: événement non créé.")
    finally:
        db.close()


def manage_get_contract_unsigned(user_infos):
    db = SessionLocal()
    contract_manager = ContractManager(db)

    try:
        contracts = contract_manager.get_unsigned_contract(user_infos["user_id"])

        if not contracts:
            print("Aucun contrats non signé trouvé.")
            return
        print("\n--- Contrats non signé.")
        for c in contracts:
            print(f"[{c.id}] Client ID: {c.client_id} | Total: {c.total_amount}€ | Restant: {c.remaining_amount}€")
    finally:
        db.close()

def manage_get_contract_unpaid(user_infos):
    db = SessionLocal()
    contract_manager = ContractManager(db)

    try:
        contracts = contract_manager.get_unpaid_contract(user_infos["user_id"])
        if not contracts:
            print("Aucun contrats impayés.")
            return
        print("\n--- Contrats non payés ---")
        for c in contracts:
            print(f"[{c.id}] Client ID: {c.client_id} | Total: {c.total_amount}€ | Restant: {c.remaining_amount}€")
    finally:
        db.close()

def manage_get_clients(user_infos):
    db = SessionLocal()
    client_manager = ClientManager(db)

    try:
        clients = client_manager.get_all_client()
        clients = [c for c in clients if c.commercial_id == user_infos['user_id']]

        if not clients:
            print("Aucun clients")
            return
        
        print("\n--- Vos clients ---")
        for c in clients:
            print(f"[{c.id}] {c.full_name} - {c.email} - {c.company_name}")
    finally:
        db.close()