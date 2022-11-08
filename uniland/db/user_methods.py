import threading
from uniland.db.tables import User
from uniland.utils.enums import UserLevel

USER_INSERTION_LOCK = threading.RLock()

def add_user(user_id):
	with ADMINSET_INSERTION_LOCK:
		user = SESSION.query(User).filter(User.user_id == user_id).first()
		if prev:
			SESSION.close()
			return
		SESSION.add(user)
		SESSION.commit()
		SESSION.close()
    

def list_users():
    return SESSION.query(User).all()
