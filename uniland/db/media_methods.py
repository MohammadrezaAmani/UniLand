"""
This module contains functions for managing media objects in the UniLand database.

Classes:
    - Submission: Represents a submission in the UniLand system.
    - Profile: Represents a user profile in the UniLand system.

Functions:
    - add_media(user_id: int) -> None: Adds media for a user.
    - get_media(id: int) -> Media: Retrieves a media object by its ID.
    - list_medias() -> List[Media]: Retrieves a list of all media objects from the database.
"""

import threading
from typing import List

from uniland import SESSION
from uniland.db import user_methods as user_db
from uniland.db.tables import Media

MEDIA_INSERTION_LOCK = threading.RLock()


def add_media(user_id: int) -> None:
    """
    Add media for a user.

    Args:
        `user_id (int)`: The ID of the user.

    Returns:
        `None`
    """
    global cnt
    user = user_db.add_user(user_id)

    with MEDIA_INSERTION_LOCK:
        media = Media(user, url="some title")
        print(f"add media: {str(media)}")
        SESSION.add(media)
        SESSION.commit()
        SESSION.close()


def get_media(id: int) -> Media:
    """
    Retrieve a media object by its ID.

    Args:
        `id (int)`: The ID of the media object to retrieve.

    Returns:
        `Media`:` The retrieved media object.
    """
    media = SESSION.query(Media).filter(Media.id == id).first()
    SESSION.expunge(media)
    SESSION.close()
    return media


def list_medias() -> List[Media]:
    """
    Retrieve a list of all media objects from the database.

    Returns:
        `List[Media]`: A list of Media objects.
    """
    return SESSION.query(Media).all()
