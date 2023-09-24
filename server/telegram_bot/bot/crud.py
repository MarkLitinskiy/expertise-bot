from typing import List

import sqlalchemy as sa

from bot.models import Clients, Meetings
from bot.database import session

from datetime import date

import math

def get_client(id: int) -> Clients:
    return session.query(Clients).get(id)

def get_meeting(id: int) -> Meetings:
    return session.query(Meetings).get(id)

def get_client_by_tg(telegram_id: int) -> Clients:
    return session.query(Clients).filter_by(telegram_id=telegram_id).first()

def find_examination_expert(lat: float, lng: float, searchFor: Clients) -> Clients:
    if searchFor.is_admin:
        return None

    admins: List[Clients] = session.query(Clients).filter_by(is_admin=True).all()

    today = date.today()

    minDistance = float("inf")
    shoosenAdmin = None

    for admin in admins:
        meeting: Meetings = session.query(Meetings).filter_by(expert_id=admin.id).order_by(sa.desc(Meetings.date)).first()

        if meeting is None:
            shoosenAdmin = admin
            break

        distance = math.sqrt(((meeting.lat - lat) ** 2) + ((meeting.lng - lng) ** 2))
        if distance < minDistance:
            shoosenAdmin = admin
    
    return shoosenAdmin

def read_client_examinations(client: Clients) -> List[Meetings]:
    return session.query(Meetings).filter_by(client_id=client.id).all()

def read_expert_examinations(expert: Clients) -> List[Meetings]:
    return session.query(Meetings).filter_by(expert_id=expert.id).all()

def read_all_examinations() -> List[Meetings]:
    return session.query(Meetings).all()