from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///AUT_Archive.sqlite')

base = declarative_base()

class Admin(base):
    
    __tablename__ = 'Admins'
    
    name = Column(String)
    family = Column(String)
    user_id = Column(Integer(), primary_key=True)
    
    def __init__(self, name, family, user_id):
        self.name = name
        self.family = family
        self.user_id = user_id

class Request(base):

    __tablename__ = 'Requests'

    course = Column(String)
    professor = Column(String)
    preparator = Column(String)
    year = Column(Integer)
    doctype = Column(String)
    submission_date = Column(DateTime, default=datetime.utcnow)
    file_id = Column(Integer, primary_key=True)
 
    def __init__(self, course, professor, preparator, year, doctype, file_id):
        self.course = course
        self.professor = professor
        self.preparator = preparator
        self.year = year
        self.doctype = doctype
        self.file_id = file_id

        

class Document(base):

    __tablename__ = 'Documents'

    course = Column(String)
    professor = Column(String)
    preparator = Column(String)
    year = Column(Integer)
    doctype = Column(String)
    file_id = Column(Integer, primary_key=True)
    corespondent = Column(String, nullable=False)
    acceptation_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, request, admin):
        self.course = request.course
        self.professor = request.professor
        self.preparator = request.preparator
        self.year = request.year
        self.doctype = request.doctype
        self.file_id = request.file_id
        self.corespondent = f'{admin.name} {admin.family}'
    
base.metadata.create_all(engine)
