import enum
from datetime import datetime, timezone

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)

from database import Base


class UserRole(enum.Enum):
    gestion = "gestion"
    support = "support"
    commercial = "commercial"


class User(Base):
    """
    Représente un collaborateur de l'entreprise Epic events.
    Identifier par un rôle : gestion, commercial ou support.
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)


class Client(Base):
    """
    Représente un client géré par un commercial.
    Contient les informations de contact et d'entreprise.
    """

    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(30), unique=True, nullable=False)
    company_name = Column(String(255), nullable=False)
    created_date = Column(Date, nullable=False)
    updated_date = Column(Date, nullable=True)
    commercial_id = Column(
        Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )


class Contract(Base):
    """
    Représente un contrat signé ou en cours avec un client.
    Chaque contrat est associé à un client et à un commercial.

    """

    __tablename__ = "contract"

    id = Column(Integer, primary_key=True)
    client_id = Column(
        Integer, ForeignKey("client.id", ondelete="CASCADE"), nullable=False
    )
    commercial_id = Column(
        Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    remaining_amount = Column(DECIMAL(10, 2), nullable=False)
    created_date = Column(Date, nullable=False)
    updated_date = Column(DateTime, default=datetime.now(timezone.utc))
    status_contract = Column(Boolean, nullable=False)


class Event(Base):
    """
    Représente un événement d'un client qui a été généré par le commercial
    une fois le contrat signé.
    Il est ensuite associé à un support pour sa gestion.

    """

    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    event_name = Column(String(255), nullable=False)
    contract_id = Column(
        Integer, ForeignKey("contract.id", ondelete="CASCADE"), nullable=False
    )
    client_id = Column(
        Integer, ForeignKey("client.id", ondelete="CASCADE"), nullable=False
    )
    support_id = Column(
        Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    event_date_start = Column(DateTime, nullable=False)
    event_date_end = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(1000), nullable=True)
