from database import SessionLocal
from controls.client_manager import ClientManager
from controls.contract_manager import ContractManager
from controls.event_manager import EventManager



def view_all_clients(user_infos):
    db = SessionLocal()
    client_manager = ClientManager(db)
    try:
        clients = client_manager.get_all_client()
        if not clients:
            print("Aucun client enregistré.")
            return
        print("\n--- Tous les clients ---")
        for c in clients:
            print(f"[{c.id}] {c.full_name} | {c.email} | {c.phone_number} | Entreprise: {c.company_name}")
    finally:
        db.close()

def view_all_contracts(user_infos):
    db = SessionLocal()
    contract_manager = ContractManager(db)
    try:
        contracts = contract_manager.get_all_contracts()
        if not contracts:
            print("Aucun contrats enregistré.")
            return
        print("\n--- Tous les contrats ---")
        for c in contracts:
            status = "Signé" if c.status_contract else "Non signé"
            print(f"[{c.id}] Client ID: {c.client_id} | Montant total: {c.total_amount}€ | Restant : {c.remaining_amount} | {status}")
    finally:
        db.close()

def view_all_events(user_infos):
    db = SessionLocal()
    eventt_manager = EventManager(db)
    try:
        events = eventt_manager.get_all_event()
        if not events:
            print("Aucun événement enregistré.")
            return
        print("\n--- Tous les événements ---")
        for e in events:
            support = f"Support ID: {e.support_id}" if e.support_id else "Pas encore assigné"            
            print(f"[{e.id}]  {e.event_name} | {e.event_date_start} - {e.event_date_end} | {support} | Lieu {e.location} | Notes {e.notes or 'Aucune'}")
    finally:
        db.close()
