import threading
from uniland import SESSION
from uniland.db.tables import Media
from uniland.db import user_methods as user_db
from uniland.utils.enums import UserLevel

"""
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
		* Inherits from Submissions with type='media'
		- url: str --> nullable=False
"""

MEDIA_INSERTION_LOCK = threading.RLock()


def add_media(user_id):
    global cnt
    user = user_db.add_user(user_id)

    with MEDIA_INSERTION_LOCK:
        media = Media(user, url="some title")
        print(f"add media: {str(media)}")
        SESSION.add(media)
        SESSION.commit()
        SESSION.close()


def get_media(id: int):
	media = SESSION.query(Media).filter(Media.id == id).first()
	SESSION.expunge(media)
	SESSION.close()
	return media


def list_medias():
    return SESSION.query(Media).all()
