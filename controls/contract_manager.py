from datetime import datetime, timezone

from models.models import Contract


class ContractManager:
    """
    Gère les contrats entre l'entreprise et les clients :
      - création, mise à jour, et à la récupération des contrats,
      - suivi des contrats impayés
      - suivi des contrats non signés

    """

    def __init__(self, db):
        self.db = db

    def create_contract(
        self, client_id, commercial_id, total_amount, remaining_amount, status_contract
    ):
        new_contract = Contract(
            client_id=client_id,
            commercial_id=commercial_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            created_date=datetime.now(timezone.utc).date(),
            status_contract=status_contract,
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

        contract.updated_date = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(contract)

        return contract

    def get_contract(self, contract_id):
        return self.db.query(Contract).filter(Contract.id == contract_id).first()

    def get_all_contracts(self):
        return self.db.query(Contract).all()

    def get_contractby_commercial(self, commercial_id):
        return (
            self.db.query(Contract)
            .filter(Contract.commercial_id == commercial_id)
            .all()
        )

    def get_unsigned_contract(self, commercial_id):
        return (
            self.db.query(Contract)
            .filter(
                Contract.commercial_id == commercial_id,
                Contract.status_contract.is_(False),
            )
            .all()
        )

    def get_unpaid_contract(self, commercial_id):
        return (
            self.db.query(Contract)
            .filter(
                Contract.commercial_id == commercial_id, Contract.remaining_amount > 0
            )
            .all()
        )
