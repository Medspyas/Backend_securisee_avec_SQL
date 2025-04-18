from database import SessionLocal
from controls.event_manager import EventManager
from datetime import datetime



def manage_assigned_events(user_infos):
    db = SessionLocal()
    event_manager = EventManager(db)


    try:
        events = event_manager.get_events_for_support(user_infos['user_id'])
        if not events:
            print("Aucun événement ne vous est attribué.")
            return
        
        print("\n--- Vos événement ---")
        for e in events:
            print(f"[{e.id}] {e.event_name} | {e.event_date_start} - {e.event_date_end} | Lieu : {e.location} | Notes: {e.notes or 'Aucune'}")
    finally:
        db.close()

def manage_update_event(user_infos):
    db = SessionLocal() 
    event_manager = EventManager(db)

    try:
        events = event_manager.get_events_for_support(user_infos['user_id'])
        if not events:
            print("Aucun événement ne vous est attribué.")
            return
        
        print("\n--- Vos événement ---")
        for e in events:
            print(f"[{e.id}] {e.event_name} | {e.event_date_start} - {e.event_date_end} | Lieu : {e.location} | Notes: {e.notes or 'Aucune'}")

        try: 
            event_id = int(input("ID de l'événement à modifier: "))
        except ValueError:
            print("ID invalide.")
            return
        updated_data = {}

        while True:
            print("\nModifier: ")
            print("1. Notes")
            print("2. Lieu")
            print("3. Nombre de participants")
            print("4. Date de début")
            print("5. Date de fin")
            print("6. Valider modification")
            print("7. Quitter")
            choix = input("Choix: ")
            if choix == "1":
                updated_data["notes"] = input("Nouvelles notes: ")
            elif choix == "2":
                updated_data["location"] = input("Nouveau lieu: ")
            elif choix == "3":
                try:
                    updated_data["attendees"] = int(input("Nombre de participants: "))
                except ValueError:
                    print("Nombre invalide.")
            elif choix == "4":
                try:
                    start = input("Date de début (YYYY-MM-DD HH:MM): ")
                    updated_data["event_date_start"] = datetime.strptime(start, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Format de date invalide.")
            elif choix == "5":
                try:
                    end = input("Date de fin (YYYY-MM-DD HH:MM): ")
                    updated_data["event_date_end"] = datetime.strptime(end, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Format de date invalide.")
            elif choix == "6":
                if not updated_data:
                    print("Aucune modification")                
                    return
                result = event_manager.update_event(event_id, updated_data)
                if result:
                    print("Modification enregistrée.")
                else:
                    print("Event introuvable.")
                    break
            elif choix == "7":
                print("Modification terminée")
                break
            else:
                print('Choix invalide.')
    finally:
        db.close()




            
