from models import Client, Contract, Event, User,  UserRole
from database import SessionLocal
from datetime import datetime, timezone

class ClientManager:
    def __init__(self, db):
        self.db = db
        
    def create_client(self, full_name, email, phone_number, company_name, commercial_id):
        new_client = Client(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            created_date=datetime.now(timezone.utc).date(),
            updated_date=datetime.now(timezone.utc).date(),
            commercial_id=commercial_id
        )
        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)

        return new_client
    def update_client(self, client_id, updated_data):
        client = self.db.query(Client).filter(Client.id == client_id).first()

        if not client:
            return None
        
        for field, value in updated_data.items():
            if hasattr(client, field):
                setattr(client, field, value)
        client.updated_date = datetime.now(timezone.utc).date()

        self.db.commit()
        self.db.refresh(client)

        return client
    
    def get_all_client(self):
        return self.db.query(Client).all()
    

class ContractManager:
    def __init__(self, db):
        self.db = db

    def create_contract(self, client_id, commercial_id, total_amount, remaining_amount, status_contract):
        new_contract = Contract(
            client_id=client_id,
            commercial_id=commercial_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            created_date=datetime.now(timezone.utc).date(),
            status_contract=status_contract
        )
        self.db.add(new_contract)
        self.db.commit()
        self.db.refresh(new_contract)

        return new_contract

    def update_contract(self, contract_id, updated_data):
        contract = self.db.query(Contract).filter(Contract.id == contract_id).first()

        if not contract:
            return None
        for field, value in updated_data.items():
            if hasattr(contract, field):
                setattr(contract, field, value)
        self.db.commit()
        self.db.refresh(contract)

        return contract      
    
    def get_contract(self, contract_id):
        return self.db.query(Contract).filter(Contract.id == contract_id).first()
    
    def get_all_contracts(self):
        return self.db.query(Contract).all()
    

    def get_unsigned_contract(self, commercial_id):
        return  self.db.query(Contract).filter(Contract.commercial_id == commercial_id, Contract.status_contract == False).all()
    
    def get_unpaid_contract(self, commercial_id):
        return  self.db.query(Contract).filter(Contract.commercial_id == commercial_id, Contract.remaining_amount > 0).all()

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
    

class GestionManager:
    def __init__(self, db):
        self.db = db

    def assign_support_to_event(self, event_id, support_id):
        event = self.db.query(Event).filter(Event.id == event_id).first()

        if not event:
            return None
        
        event.support_id = support_id
        self.db.commit()
        self.db.refresh(event)
        return event
    

    def create_user(self, first_name, last_name, email, password, role):
        exist = self.db.query(User).filter(User.email).first()

        if exist:
            return None
        
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=UserRole(role)
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def updated_user(self, user_id, updated_data):
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return None
        
        for field, value in updated_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        self.db.commit()    
        self.db.refresh(user)
        return user
    
    def delete_user(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        self.db.delete(user)
        self.db.commit()
        return True