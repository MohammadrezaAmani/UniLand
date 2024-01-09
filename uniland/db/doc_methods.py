"""
This module contains functions for managing documents in the database.

Submission Class Properties:
    - id: int
    - submission_data: datetime
    - is_confirmed: bool
    - faculty: str
    - search_text: str
    - description: str
    - correspondent_admin: int (foreign key to user.user_id)
    - owner: int (foreign key to user.user_id)

Document Class Properties:
    - Inherits from Submissions with type='document'
    - file_id: str `(nullable=False)`
    - unique_id: str `(nullable=False)`
    - file_type: DocType `(nullable=False)`
    - course: str `(nullable=False)`
    - professor: str `(nullable=False)`
    - writer: str
    - semester: int

Functions:
    - `add_document(user_id: int)` -> None:
        Adds a new document to the database.

    - `get_document(id: int)` -> Document:
        Retrieves a document from the database by its ID.

    - `unique_id_exists(unique_id: str)` -> bool:
        Checks if a document with the given unique ID exists in the database.

    - `list_documents() -> List[Document]`:
        Retrieves a list of all documents in the database.
"""

import logging
import threading
from random import randint
from typing import List

from uniland import SESSION
from uniland.db import user_methods as user_db
from uniland.db.tables import DocType, Document

DOCUMENT_INSERTION_LOCK = threading.RLock()

cnt = 1


def add_document(user_id: int) -> None:
    """
    Add a new document to the database.

    Args:
        user_id (int): The ID of the user adding the document.

    Returns:
        None
    """
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
        logging.info(f"add document: {str(doc)}")
        doc.update_search_text()
        SESSION.add(doc)
        SESSION.commit()
        SESSION.close()


def get_document(id: int) -> Document:
    """
    Retrieve a document from the database by its ID.

    Args:
        id (int): The ID of the document to retrieve.

    Returns:
        Document: The retrieved document object.
    """
    document = SESSION.query(Document).filter(Document.id == id).first()
    SESSION.expunge(document)
    SESSION.close()
    return document


def unique_id_exists(unique_id: str) -> bool:
    """
    Check if a document with the given unique ID exists in the database.

    Args:
        unique_id (str): The unique ID of the document.

    Returns:
        bool: True if a document with the given unique ID exists, False otherwise.
    """
    return SESSION.query(
        SESSION.query(Document).filter(Document.unique_id == unique_id).exists()
    ).scalar()


def list_documents() -> List[Document]:
    """
    Retrieve a list of all documents in the database.

    Returns:
        List[Document]: A list of Document objects.
    """
    return SESSION.query(Document).all()
