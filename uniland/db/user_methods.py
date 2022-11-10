import threading
from uniland import SESSION
from uniland.db.tables import User
from uniland.utils.enums import UserLevel

USER_INSERTION_LOCK = threading.RLock()

def add_user(user_id):
	with USER_INSERTION_LOCK:
		user = SESSION.query(User).filter(User.user_id == user_id).first()
		if user:
			SESSION.close()
			return
		user = User(user_id)
		print(f'add user: {str(user)}')
		SESSION.merge(user)
		SESSION.commit()
		SESSION.close()
    

def list_users():
    return SESSION.query(User).all()
