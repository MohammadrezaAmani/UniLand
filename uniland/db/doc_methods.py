import threading
from uniland import SESSION
from uniland.db.tables import Document, DocType
from uniland.db import user_methods as user_db
from uniland.utils.enums import UserLevel
from random import randint

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

	Document Class Properties:
		* Inherits from Submissions with type='document'
		- file_id: str --> nullable=False
		- unique_id: str --> nullable=False
		- file_type: DocType --> nullable=False
		- course: str --> nullable=False
		- professor: str --> nullable=False
		- writer : str
		- semester: int
'''

DOCUMENT_INSERTION_LOCK = threading.RLock()

cnt = 1

def add_document(user_id):
	global cnt
	cnt = randint(1, 1e9)
	user = user_db.add_user(user_id)
	new_doc = {'file_id': f'{str(cnt)}',
            'unique_id': f'{str(cnt)}', 'file_type': DocType.Exercises, 'course': 'Riaza1', 'professor': 'Dehqan'}
	cnt += 1
	with DOCUMENT_INSERTION_LOCK:
		# document = SESSION.query(User).filter(User.user_id == user_id).first()
		# if user:
		# 	SESSION.close()
		# 	return
		doc = Document(user, new_doc['file_id'], new_doc['unique_id'])
		doc.file_type = new_doc['file_type']
		doc.course = new_doc['course']
		doc.professor = new_doc['professor']
		# user = User(user_id)
		print(f'add document: {str(doc)}')
		SESSION.merge(doc)
		SESSION.commit()
		SESSION.close()


def list_documents():
    return SESSION.query(Document).all()