"""
This module contains functions for managing profiles in the UniLand database.

Classes:
- Profile: Represents a user profile in the database.

Functions:
- add_profile(user_id: int) -> None: Adds a profile for the given user ID.
- get_profile(id: int) -> Profile: Retrieves a profile from the database based on the given ID.
- list_profiles() -> List[Profile]: Retrieves a list of all profiles from the database.
"""

import threading
from typing import List

from uniland import SESSION
from uniland.db import user_methods as user_db
from uniland.db.tables import Profile

PROFILE_INSERTION_LOCK = threading.RLock()


def add_profile(user_id: int) -> None:
    """
    Adds a profile for the given user ID.

    Args:
            user_id (int): The ID of the user.

    Returns:
            None
    """
    global cnt
    user = user_db.add_user(user_id)

    with PROFILE_INSERTION_LOCK:
        profile = Profile(user, title="some title")
        print(f"add profile: {str(profile)}")
        SESSION.add(profile)
        SESSION.commit()
        SESSION.close()


def get_profile(id: int) -> Profile:
    """
    Retrieves a profile from the database based on the given ID.

    Args:
            id (int): The ID of the profile to retrieve.

    Returns:
            Profile: The retrieved profile object.
    """
    profile = SESSION.query(Profile).filter(Profile.id == id).first()
    SESSION.expunge(profile)
    SESSION.close()
    return profile


def list_profiles() -> List[Profile]:
    """
    Retrieves a list of all profiles from the database.

    Returns:
            List[Profile]: A list of Profile objects.
    """
    return SESSION.query(Profile).all()
