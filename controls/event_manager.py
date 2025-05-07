from models.models import Client, Contract, Event


class EventManager:
    """
    Gère les opérations liées aux événements :
        - récupération des événements une fois contrats signés,
        - modification des événements par le support ou la gestion.

    """

    def __init__(self, db):
        self.db = db

    def create_event(
        self,
        contract_id,
        client_id,
        event_name,
        event_date_start,
        event_date_end,
        location,
        attendees,
        notes,
        user_id,
    ):
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
            support_id=None,
        )

        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)

        return new_event

    def update_event(self, event_id, updated_data):
        event = self.db.query(Event).filter(Event.id == event_id).first()

        if not event:
            return None

        for field, value in updated_data.items():
            if hasattr(event, field):
                setattr(event, field, value)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_all_event(self):
        return self.db.query(Event).all()

    def get_events_for_support(self, support_id):
        return self.db.query(Event).filter(Event.support_id == support_id).all()

    def get_events_without_support(self):
        return self.db.query(Event).filter(Event.support_id.is_(None)).all()
