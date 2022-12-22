import threading
from uniland import SESSION
from uniland.db.tables import Document, DocType
from uniland.db import user_methods as user_db
from uniland.utils.enums import UserLevel
from random import randint

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

	Document Class Properties:
		* Inherits from Submissions with type='document'
		- file_id: str --> nullable=False
		- unique_id: str --> nullable=False
		- file_type: DocType --> nullable=False
		- course: str --> nullable=False
		- professor: str --> nullable=False
		- writer : str
		- semester: int
"""

DOCUMENT_INSERTION_LOCK = threading.RLock()

cnt = 1


def add_document(user_id):
    global cnt
    cnt = randint(1, 1e9)
    user = user_db.add_user(user_id)
    new_doc = {
        "file_id": f"{str(cnt)}",
        "unique_id": f"{str(cnt)}",
        "file_type": DocType.Exercises,
        "course": "Riaza1",
        "professor": "Dehqan",
    }
    cnt += 1
    courses = ["ریاضی", "فیزیک", "مبانی علوم کامپیوتر", "شیمی"]
    professors = ["محمدی", "زارع", "غیبی", "شیری"]
    writers = ["محمدی", "زارع", "غیبی", "شیری"]
    universities = ["صنعتی شریف", "صنعتی امیرکبیر", "صنعتی اصفهان", "امیرکبیر"]
    with DOCUMENT_INSERTION_LOCK:
        doc = Document(
            user,
            new_doc["file_id"],
            new_doc["unique_id"],
            course=courses[randint(0, 3)],
            professor=professors[randint(0, 3)],
            writer=writers[randint(0, 3)],
            university=universities[randint(0, 3)],
        )
        doc.file_type = new_doc["file_type"]
        doc.course = new_doc["course"]
        doc.professor = new_doc["professor"]
        print(f"add document: {str(doc)}")
        doc.update_search_text()
        SESSION.add(doc)
        SESSION.commit()
        SESSION.close()


def get_document(id: int):
    document = SESSION.query(Document).filter(Document.id == id).first()
    SESSION.expunge(document)
    SESSION.close()
    return document


def unique_id_exists(unique_id: str):
    return SESSION.query(
        SESSION.query(Document).filter(Document.unique_id == unique_id).exists()
    ).scalar()


def list_documents():
    return SESSION.query(Document).all()
