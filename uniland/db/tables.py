from uniland import BASE, SESSION
from sqlalchemy import (Column, Integer, String, DateTime, Enum, Table,
                        Boolean, ForeignKey)
from sqlalchemy.orm import relationship
from datetime import datetime
from uniland.utils.enums import UserLevel, DocType

bookmarks_association = Table(
    'bookmarks_association', BASE.metadata,
    Column('user_id', Integer,
           ForeignKey('users.user_id')),
    Column('submission_id', Integer,
           ForeignKey('submissions.id')))


# TODO! handle ON DELETE cascade in relationships
class User(BASE):
  __tablename__ = "users"
  user_id = Column(Integer, nullable=False,
                   primary_key=True)  # user_id in telegram
  access_level = Column(Enum(UserLevel), nullable=False)
  # many-to-many with Submission.liked_users
  bookmarks = relationship('Submission',
                           secondary=bookmarks_association,
                           back_populates='liked_users')
  # one-to_many with Submission.owner
  user_submissions = relationship('Submission',back_populates='owner')

  def __init__(self, user_id):
    self.user_id = user_id
    self.access_level = UserLevel.Ordinary

  def __repr__(self):
    return f'User {self.user_id} has access level {self.access_level}'


class Submission(BASE):
  __tablename__ = "submissions"
  id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
  submission_date = Column(DateTime, default=datetime.utcnow)
  is_confirmed = Column(Boolean, default=False)
  # many-to-one
  correspondent_admin = Column(Integer,
                               ForeignKey('users.user_id'),
                               default=None)
  # many-to-one with User.user_submissions
  # owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
  owner = relationship('User', back_populates='user_submissions')
  # many-to-many with User.bookmarks
  liked_users = relationship('User',
                             secondary=bookmarks_association,
                             back_populates='bookmarks')

  faculty = Column(String(30), default='نامشخص')
  search_text = Column(String(200), default='')
  description = Column(String(500),
                       default='توضیحاتی برای این فایل ثبت نشده است.')

  submission_type = Column(String(20))

  __mapper_args__ = {
      "polymorphic_identity": "submission",
      "polymorphic_on": submission_type,
  }

  def __init(self, owner_id):
    self.owner = owner

  def confirm(self):
    self.is_confirmed = True


class Document(Submission):
  __tablename__ = "documents"
  id = Column(Integer, ForeignKey("submissions.id"), primary_key=True)
  file_id = Column(String(30), nullable=False, unique=True)
  file_type = Column(Enum(DocType), nullable=False)  # Necessary field
  course = Column(String(30), nullable=False)  # Necessary field
  professor = Column(String(30), nullable=False)  # Necessary field
  writer = Column(String(30), default='نامشخص')
  semester_year = Column(Integer, default=None)

  def __init__(self, owner, file_id):
    super().__init__(owner)
    self.file_id = file_id

  __mapper_args__ = {
      "polymorphic_identity": "document",
  }


class Profile(Submission):
  __tablename__ = "profiles"
  id = Column(Integer, ForeignKey("submissions.id"), primary_key=True)
  title = Column(String(200), nullable=False)
  email = Column(String(50), default='')
  phone_number = Column(String(25), default='')
  image_link = Column(String, default='')
  image_id = Column(String(30), default='')
  resume_link = Column(String, default='')
  resume_id = Column(String(30), default='')

  def __init__(self, owner, title):
    super().__init__(owner)
    self.title = title

  __mapper_args__ = {
      "polymorphic_identity": "profile",
  }


class Media(Submission):
  __tablename__ = "medias"
  id = Column(Integer, ForeignKey("submissions.id"), primary_key=True)
  url = Column(String, nullable=False)
  media_type = Column(String(20), default=None)
  course = Column(String(30), nullable=False)  # Necessary field
  professor = Column(String(30), nullable=False)  # Necessary field
  semester_year = Column(Integer, default=None)

  def __init__(self, owner, url):
    super().__init__(owner)
    self.url = url

  __mapper_args__ = {
      "polymorphic_identity": "media",
  }

User.__table__.create(checkfirst=True)
Submission.__table__.create(checkfirst=True)
Document.__table__.create(checkfirst=True)
Profile.__table__.create(checkfirst=True)
Media.__table__.create(checkfirst=True)
