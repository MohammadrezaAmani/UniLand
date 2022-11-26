import threading
from uniland import SESSION
from uniland.db.tables import Profile
from uniland.db import user_methods as user_db
from uniland.utils.enums import UserLevel

'''
	Submission Class Properties:
		- id: int
		- submission_data : datetime
		- is_confirmed : bool
		- faculty : str
		- search_text : str
		- description : str
		- correspondent_admin : int --> fk user.user_id
		- owner : int --> fk user.user_id

	Profile Class Properties:
		* Inherits from Submissions with type='profile'
		- title: str --> nullable=False
		- email: str
		- phone_number: str
		- image_link: str
		- image_id: str
		- resume_link : str
		- resume_id: int
'''

PROFILE_INSERTION_LOCK = threading.RLock()

def add_profile(user_id):
	global cnt
	user = user_db.add_user(user_id)

	with PROFILE_INSERTION_LOCK:
		profile = Profile(user, title='some title')
		print(f'add profile: {str(profile)}')
		SESSION.add(profile)
		SESSION.commit()
		SESSION.close()


def list_profiles():
    return SESSION.query(Profile).all()
