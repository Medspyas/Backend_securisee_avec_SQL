from controls.client_manager import ClientManager
from controls.contract_manager import ContractManager
from controls.event_manager import EventManager
from database import SessionLocal
from utils import (
    get_valid_email,
    get_valid_float,
    get_valid_integer,
    get_valid_phone_number,
    is_valid_date,
)

"""
    Ce fichier contient les fonctionnalités accessibles aux utilisateurs ayant le rôle 'commercial'.
    Il permet notamment :
        - la gestion des clients (création, mise à jour)
        - la consultation et la modification contrats liés à leurs propres clients,
        - la création d'événements une fois les contrats signés,
        - le filtrage des contrats selon leurs statuts.
    Toutes les actions sont limitées aux données associées au commercial connecté.

"""


def manage_create_client(user_infos):
    db = SessionLocal()
    client_manager = ClientManager(db)

    try:
        print("\n--- Création nouveau client")
        full_name = input("Nom complet: ")
        email = get_valid_email()
        phone = get_valid_phone_number()
        company_name = input("Nom de l'entreprise: ")
        commercial_id = user_infos["user_id"]

        new_client = client_manager.create_client(
            full_name, email, phone, company_name, commercial_id
        )

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
        clients = [c for c in clients if c.commercial_id == user_infos["user_id"]]

        if not clients:
            print("Aucun à modifier.")
            return
        print("\n--- Vos clients ---")
        for c in clients:
            print(
                f"[{c.id}] {c.full_name} - {c.email} - {c.phone_number}"
                f" - {c.company_name} - {c.commercial_id}"
            )

        client_id = get_valid_integer("ID du client à modifier: ")

        if not any(e.id == client_id for e in clients):
            print("ID introuvable.")
            return

        updated_data = {}

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
                updated_data["email"] = get_valid_email()
            elif choix == "3":
                updated_data["phone"] = get_valid_phone_number()
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


def manage_update_own_contract(user_infos):
    db = SessionLocal()
    contract_manager = ContractManager(db)
    client_manager = ClientManager(db)
    try:
        all_clients = client_manager.get_all_client()
        my_clients = [
            c for c in all_clients if c.commercial_id == user_infos["user_id"]
        ]
        my_clients_ids = [c.id for c in my_clients]

        all_contracts = contract_manager.get_all_contracts()
        contracts = [c for c in all_contracts if c.client_id in my_clients_ids]

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

        contract_id = get_valid_integer("ID du contrat à modifier: ")

        if not any(e.id == contract_id for e in contracts):
            print("ID introuvable.")
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
                updated_data["total_amount"] = get_valid_float("Montant total (€): ")
            elif choix == "2":
                updated_data["remaining_amount"] = get_valid_float(
                    "Montant restant à payer (€): "
                )
            elif choix == "3":
                status_input = input("Le contrat est-il signé ? (o/n): ").lower()
                updated_data["status_contract"] = True if status_input == "o" else False
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
        contracts = contract_manager.get_contractby_commercial(user_infos["user_id"])
        contracts = [c for c in contracts if c.status_contract is True]

        if not contracts:
            print("Aucun contrats signé trouvé.")
            return
        print("\n--- Contrats signés disponibles ---")
        for c in contracts:
            print(
                f"[{c.id}] Client ID: {c.client_id} | Total: {c.total_amount}€ | Restant: {c.remaining_amount}€"
            )

        contract_id = get_valid_integer("ID du contrat pour créer l'événement: ")

        if not any(e.id == contract_id for e in contracts):
            print("ID introuvable.")
            return

        client_id = next((c.client_id for c in contracts if c.id == contract_id), None)
        if client_id is None:
            print("Contrat non trouvé")
            return

        event_name = input("Nom de l'événement: ")
        location = input("Lieu: ")

        attendees = get_valid_integer("Nombre de participants: ")
        while True:
            event_date_start = is_valid_date(
                "Date et heure du début (DD-MM-YYYY HH:MM): "
            )
            event_date_end = is_valid_date("Date et heure de fin (DD-MM-YYYY HH:MM): ")

            if event_date_end <= event_date_start:
                print("La date de fin doit être superieur à la date de début")
                continue
            break

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
            user_id=user_infos["user_id"],
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
            print(
                f"[{c.id}] Client ID: {c.client_id} | Total: {c.total_amount}€ | Restant: {c.remaining_amount}€"
            )
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
            print(
                f"[{c.id}] Client ID: {c.client_id} | Total: {c.total_amount}€ | Restant: {c.remaining_amount}€"
            )
    finally:
        db.close()


def manage_get_clients(user_infos):
    db = SessionLocal()
    client_manager = ClientManager(db)

    try:
        clients = client_manager.get_all_client()
        clients = [c for c in clients if c.commercial_id == user_infos["user_id"]]

        if not clients:
            print("Aucun clients")
            return

        print("\n--- Vos clients ---")
        for c in clients:
            print(f"[{c.id}] {c.full_name} - {c.email} - {c.company_name}")
    finally:
        db.close()
