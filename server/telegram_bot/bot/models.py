from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy.orm import relationship

Base = declarative_base()

class Clients(Base):
    __tablename__ = 'client_data'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)
    telegram_id = sa.Column(sa.Integer, nullable=False)
    telegram_username = sa.Column(sa.Text, nullable=False)
    is_admin = sa.Column(sa.Boolean, nullable=False, default=False)

class Meetings(Base):
    __tablename__ = 'meetings'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    expert_id = sa.Column(sa.Integer, sa.ForeignKey('client_data.id'), nullable=False)
    client_id = sa.Column(sa.Integer, sa.ForeignKey('client_data.id'), nullable=False)
    date = sa.Column(sa.Date, nullable=False)
    time = sa.Column(sa.Time, nullable=False)
    lat = sa.Column(sa.Float, nullable=False)
    lng = sa.Column(sa.Float, nullable=False)
    house = sa.Column(sa.Text, nullable=False)

    expert = relationship("Clients", foreign_keys=[expert_id])
    client = relationship("Clients", foreign_keys=[client_id])
