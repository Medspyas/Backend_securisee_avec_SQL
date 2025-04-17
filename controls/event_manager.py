from models.models import Client, Contract, Event





class EventManager:
    def __init__(self, db):
        self.db = db        

    def create_event(self, contract_id, client_id, event_name, event_date_start, event_date_end, location, attendees, notes, user_id):
        contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract or not contract.status_contract:
            return None
        
        client = self.db.query(Client).filter(Client.id == contract.client_id).first()
        if client.commercial_id != user_id:
            return None
        
        new_event = Event(
            contract_id=contract_id,
            client_id=client_id,
            event_name=event_name,
            event_date_start=event_date_start,
            event_date_end=event_date_end,
            location=location,
            attendees=attendees,
            notes=notes,
            support_id = None
        )

        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)

        return new_event
    
    def get_all_event(self):
        return self.db.query(Event).all()
    
    def get_events_for_support(self, support_id):
        return self.db.query(Event).filter(Event.support_id == support_id).all()
    

    def get_events_without_support(self):
        return self.db.query(Event).filter(Event.support_id == None).all()