import threading

from uniland import BASE, SESSION
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid


class Admin(BASE):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, nullable=False) # user_id in telegram
    name = Column(String(25))
    family = Column(String(30))
    major = Column(String(25))
    
    # accepted_requests = relationship("Request", back_populates="corr_admin")

    def __init__(self, user_id, name, family, major):
        self.user_id = user_id
        self.name = name
        self.family = family
        self.major = major

    @property
    def fullname(self):
        return f'{self.name} {self.family}'
    
    def __repr__(self):
        return f'Admin {self.name} {self.family} \nid: {self.user_id}\nmajor: {self.major}\nnumber in db: {self.id}'


Admin.__table__.create(checkfirst=True)
ADMIN_INSERTION_LOCK = threading.RLock()

def get_admin(user_id):
    return SESSION.query(Admin).filter(Admin.user_id == user_id).first()

def list_admins():
    try:
        return SESSION.query(Admin).order_by(Admin.id.asc()).all()
    finally:
        SESSION.close()
    return False
