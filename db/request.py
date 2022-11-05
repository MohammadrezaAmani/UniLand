# import threading

# from uniland import BASE, SESSION
# from sqlalchemy import Column, Integer, String, Boolean, DateTime
# from datetime import datetime
# from sqlalchemy_utils import UUIDType
# import uuid


# class Request(BASE):
#     __tablename__ = "requests"
#     id = Column(UUIDType(binary=False),
#                       primary_key=True, default=uuid.uuid4)
#     is_accepted = Column(Boolean, default=False)
#     owner_id = Column(Integer) # user_id of the user that has submitted this request
#     submission_date = Column(DateTime, default=datetime.utcnow)
#     # TODO : add foreign key for corr_admin and ON DELETE cascade
#     # corr_admin = Column(Integer, ForeignKey("parent_table.id"), default=None)  # user_id of the admin that has accepted this request
#     corr_admin_fullname = Column(String(55), default=None)
#     acceptation_date = Column(DateTime, default=None)

#     def __init__(self, req_id, owner_id):
#         self.owner_id = owner_id

#     def accept(self, admin):
#         self.corr_admin_fullname = admin.fullname
#         self.acceptation_date = datetime.utcnow()

#     def __repr__(self):
#         if self.is_accepted:
#             return f'Request {self.req_id} is not yet accepted'
#         else:
#             return f'Request {self.req_id} accepted by {self.corr_admin_fullname} in {self.acceptation_date}'

# class Document(BASE):
#     __tablename__ = "documents"


# Request.__table__.create(checkfirst=True)
# REQUEST_INSERTION_LOCK = threading.RLock()
