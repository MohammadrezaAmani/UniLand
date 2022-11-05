import database as db
from sqlalchemy.orm import sessionmaker
import random

Session = sessionmaker(db.engine)
session = Session()

# adding data
names = ['ilya', 'pouria', 'mohammadreza', 'ali']
families = ['khalafi', 'alimorad', 'amani', 'mehrabi']
user_ids = [random.randint(100, 1000) for i in range(4)]
for i in range(4):
    new_admin = db.Admin(names[i], families[i], user_ids[i])
    session.add(new_admin)
    # also session.add_all([objects]) is possible
    
# save changes in database
session.commit()

# All data
for s in session.query(db.Admin).all():
    print(s.name, s.family)
    
# Selected data
for s in session.query(db.Admin).filter(db.Admin.user_id>300):
    print(s.name, s.family)
