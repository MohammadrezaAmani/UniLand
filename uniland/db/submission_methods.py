import threading
from uniland import SESSION
from uniland.db.tables import Media
from uniland.db import user_methods as user_db
from uniland.utils.enums import UserLevel

'''
Submission Class Properties:
	- id: int
	- submission_data: datetime
	- is_confirmed: bool
	- faculty: str
	- search_text: str
	- description: str
	- correspondent_admin: int - -> fk user.user_id
	- owner: int - -> fk user.user_id
'''

SUBMISSION_INSERTION_LOCK = threading.RLock()

# Functionality: Search by keyworkds and paging and sort by likes
# TODO! Search: FTS5؟