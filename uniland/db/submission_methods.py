"""
This module contains functions for managing submissions in the UniLand database.

Submission Class Properties:
    - id (int): The ID of the submission.
    - submission_data (datetime): The date and time of the submission.
    - is_confirmed (bool): Indicates whether the submission is confirmed or not.
    - faculty (str): The faculty associated with the submission.
    - search_text (str): The search text associated with the submission.
    - description (str): The description of the submission.
    - correspondent_admin (int): The ID of the correspondent admin (foreign key to user.user_id).
    - owner (int): The ID of the owner (foreign key to user.user_id).
    
Functions:
    - add_submission(user_id: int, submission_type: SubmissionType, faculty: str, search_text: str, description: str) -> None:
        Adds a new submission to the database.
        
    - get_submission(id: int) -> Submission:
        Retrieves a submission from the database by its ID.
        
    - list_submissions() -> List[Submission]:
        Retrieves a list of all submissions in the database.
        
    - increase_search_times(id: int) -> None:
        Increase the search times for a submission with the given ID.
        
    - confirm_user_submission(admin_id: int, submission_id: int) -> None:
        Confirms a user submission by an admin.
        
    - delete_submission(submission_id: int) -> bool:
        Deletes a submission from the database.
        
    - get_unconfirmed_submissions() -> List[Submission]:
        Retrieves a list of unconfirmed submissions.
        
    - is_pending(submission_id: int) -> bool:
        Check if a submission is pending.
        
    - count_total_submissions() -> int:
        Counts the total number of submissions.
        
    - count_confirmed_submissions() -> int:
        Counts the number of confirmed submissions.
"""

import threading
from typing import List

from uniland import SESSION, search_engine, usercache
from uniland.db import user_methods as user_db
from uniland.db.tables import Submission


SUBMISSION_INSERTION_LOCK = threading.RLock()


def increase_search_times(id: int) -> None:
    """
    Increase the search times for a submission with the given ID.

    Args:
        id (int): The ID of the submission.

    Returns:
        None
    """
    with SUBMISSION_INSERTION_LOCK:
        submission = SESSION.query(Submission).filter(Submission.id == id).first()
        if submission:
            submission.search_times += 1
            search_engine.increase_search_times(id)
            SESSION.commit()
        SESSION.close()


def confirm_user_submission(admin_id: int, submission_id: int) -> None:
    """
    Confirms a user submission by an admin.

    Args:
        admin_id (int): The ID of the admin confirming the submission.
        submission_id (int): The ID of the submission to be confirmed.

    Returns:
        None
    """
    admin = user_db.get_user(admin_id)
    if admin == None:
        return
    with SUBMISSION_INSERTION_LOCK:
        submission = (
            SESSION.query(Submission).filter(Submission.id == submission_id).first()
        )
        if submission:
            submission.confirm(user_db.get_user(admin_id))
            search_engine.index_record(
                id=submission.id,
                search_text=submission.search_text,
                sub_type=submission.submission_type,
                likes=0,
            )
            SESSION.commit()
        SESSION.close()


def delete_submission(submission_id: int) -> bool:
    """
    Deletes a submission from the database.

    Args:
        submission_id (int): The ID of the submission to be deleted.

    Returns:
        bool: True if the submission is successfully deleted, False otherwise.
    """
    with SUBMISSION_INSERTION_LOCK:
        target_submission = (
            SESSION.query(Submission).filter(Submission.id == submission_id).first()
        )
        # Also decrease search times and achieved likes from usercache and search engine
        if not target_submission:
            SESSION.close()
            return False

        for user in target_submission.liked_users:
            usercache.decrease_achieved_likes(
                user.user_id, amount=search_engine.get_likes(target_submission.id)
            )

        total_searches = target_submission.search_times

        if target_submission.id in search_engine.subs:
            search_engine.remove_record(target_submission.id)
        target_submission.liked_users.clear()
        SESSION.commit()

        for submission in (
            SESSION.query(Submission).filter(Submission.is_confirmed == True).all()
        ):
            if submission.search_times > 0:
                submission.search_times += 1
                search_engine.increase_search_times(submission.id)
                total_searches -= 1
                SESSION.commit()
                if total_searches <= 0:
                    break

        SESSION.delete(target_submission)
        SESSION.commit()
        return True


def get_submission(submission_id: int) -> Submission:
    """
    Search in the database for a submission with the given id and return it.

    Args:
        submission_id (int): The id of the submission.

    Returns:
        Submission: The submission object.
    """
    submission = (
        SESSION.query(Submission).filter(Submission.id == submission_id).first()
    )
    SESSION.refresh(submission)
    SESSION.expunge_all()
    SESSION.close()
    return submission


def get_unconfirmed_submissions() -> List[Submission]:
    """
    Retrieves a list of unconfirmed submissions.

    Returns:
        List[Submission]: A list of unconfirmed submissions.
    """
    subs = (
        SESSION.query(Submission)
        .filter(Submission.is_confirmed == False)
        .order_by(Submission.submission_date.desc())
        .all()
    )
    SESSION.expunge_all()
    SESSION.close()
    return subs


def is_pending(submission_id: int) -> bool:
    """
    Check if a submission is pending.

    Args:
        submission_id (int): The ID of the submission.

    Returns:
        bool: True if the submission is pending, False otherwise.
    """
    submission = (
        SESSION.query(Submission).filter(Submission.id == submission_id).first()
    )
    if submission:
        return not submission.is_confirmed
    return False


def count_total_submissions() -> int:
    """
    Counts the total number of submissions.

    Returns:
        int: The total number of submissions.
    """
    return SESSION.query(Submission).count()


def count_confirmed_submissions() -> int:
    """
    Counts the number of confirmed submissions.

    Returns:
        int: The number of confirmed submissions.
    """
    return len(search_engine.subs)
