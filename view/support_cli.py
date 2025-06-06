from controls.contract_manager import ContractManager
from controls.event_manager import EventManager
from database import SessionLocal
from utils import get_valid_integer, is_valid_date

"""
    Ce fichier contient les fonctionnalités destinées aux utilisateurs ayant le rôle 'support'.
    Il leur permet de :
        - de consulter la liste d'événements qui leur sont assignés,
        - de mettre à jour les informations des événements dont ils sont responsables,
        - d'accéder en lecture aux données clients, contrats et événements.
"""


def manage_assigned_events(user_infos):
    db = SessionLocal()
    event_manager = EventManager(db)

    try:
        events = event_manager.get_events_for_support(user_infos["user_id"])
        if not events:
            print("Aucun événement ne vous est attribué.")
            return

        print("\n--- Vos événement ---")
        for e in events:
            print(
                f"[{e.id}] {e.event_name} | {e.event_date_start} - {e.event_date_end}"
                f"| Lieu : {e.location} | Notes: {e.notes or 'Aucune'}"
            )
    finally:
        db.close()


def manage_update_event(user_infos):
    db = SessionLocal()
    event_manager = EventManager(db)
    contract_manager = ContractManager(db)

    try:
        events = event_manager.get_events_for_support(user_infos["user_id"])
        if not events:
            print("Aucun événement ne vous est attribué.")
            return

        print("\n--- Vos événement ---")
        for e in events:
            print(
                f"[{e.id}] {e.event_name} | {e.event_date_start} - {e.event_date_end}"
                f"| Lieu : {e.location} | Nombre de participants: {e.attendees} | Notes: {e.notes or 'Aucune'}"
            )

        event_id = get_valid_integer("ID de l'événement à modifier: ")
        event = next((e for e in events if e.id == event_id), None)

        if not event:
            print("ID introuvable.")
            return

        updated_data = {}

        while True:
            print("\nModifier: ")
            print("1. Nom de l'évènement")
            print("2. Notes")
            print("3. Lieu")
            print("4. Nombre de participants")
            print("5. Date de début")
            print("6. Date de fin")
            print("7. ID contrat")
            print("8. Valider modification")
            print("9. Quitter")
            choix = input("Choix: ")
            if choix == "1":
                updated_data["event_name"] = input("Nouveau nom: ")
            elif choix == "2":
                updated_data["notes"] = input("Nouvelles notes: ")
            elif choix == "3":
                updated_data["location"] = input("Nouveau lieu: ")
            elif choix == "4":
                updated_data["attendees"] = get_valid_integer(
                    "Nombre de participants: "
                )
            elif choix == "5":
                updated_data["event_date_start"] = is_valid_date(
                    "Date de début (DD-MM-YYYY HH:MM): "
                )
            elif choix == "6":
                date_end = is_valid_date("Date de fin (DD-MM-YYYY HH:MM)")
                date_start = updated_data.get(
                    "event_date_start", event.event_date_start
                )

                if date_end <= date_start:
                    print("La date de fin doit être superieur à la date de début")
                    continue

                updated_data["event_date_end"] = date_end

            elif choix == "7":
                contrats_signes = contract_manager.get_all_contracts(
                    user_infos["user_id"]
                )
                contrats_signes = [
                    c
                    for c in contrats_signes
                    if c.status_contract and c.commercial_id == user_infos["user_id"]
                ]

                if not contrats_signes:
                    print("Aucun contrats signé trouvé.")
                    continue
                print("\n--- Contrats signés disponibles ---")
                for c in contrats_signes:
                    print(
                        f"[{c.id}] Client ID: {c.client_id} | Montant: {c.total_amount}€ | {c.remaining_amount}€"
                    )

                new_contract_id = get_valid_integer("Nouvel ID du contrat: ")

                if not any(c.id == new_contract_id for c in contrats_signes):
                    print("Contrats introuvable")
                    continue

                updated_data["contract_id"] = new_contract_id

            elif choix == "8":
                if not updated_data:
                    print("Aucune modification")
                    return
                result = event_manager.update_event(event_id, updated_data)
                if result:
                    print("Modification enregistrée.")
                else:
                    print("Event introuvable.")
                    break
            elif choix == "9":
                print("Modification terminée")
                break
            else:
                print("Choix invalide.")
    finally:
        db.close()
