from models.models import Client, Contract, Event, User,  UserRole
from datetime import datetime, timezone


class ClientManager:
    def __init__(self, db):
        self.db = db
        
    def create_client(self, full_name, email, phone_number, company_name, commercial_id):
        if self.check_client_exists(email, phone_number):
            return None
        
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
    
    def check_client_exists(self, email, phone):
        return self.db.query(Client).filter(
            (Client.email == email) | (Client.phone_number == phone)
        ).first() is not None