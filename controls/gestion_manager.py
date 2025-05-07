from models.models import Event, User, UserRole


class GestionManager:
    """
    Gère les actions réservées au rôle gestion :
        - création, modification et suppression des utilisateurs,
        - attribution des supports aux événements,
        - récupération de tous les utilisateurs.

    """

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
        exist = self.db.query(User).filter(User.email == email).first()

        if exist:
            return None

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=UserRole(role),
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

    def get_all_users(self):
        return self.db.query(User).all()
