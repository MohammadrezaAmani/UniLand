import threading
from datetime import datetime, timedelta
from typing import List

from uniland import SESSION, search_engine, usercache
from uniland.db.tables import Submission, User, bookmarks_association
from uniland.utils.enums import UserLevel
from uniland.utils.steps import UserSteps

USER_INSERTION_LOCK = threading.RLock()


def add_user(user_id: int, last_step: str = UserSteps.START.value) -> User:
    """
    Adds a new user to the database.

    Args:
        user_id (int): The ID of the user.
        last_step (str, optional): The last step the user completed. Defaults to UserSteps.START.value.

    Returns:
        User: The newly added user object.
    """
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user_id).first()
        if user:
            SESSION.expunge(user)
            SESSION.close()
            return user
        user = User(user_id, last_step=last_step)
        user.access_level = UserLevel.Ordinary
        usercache.add_user(user_id, 1, last_step)
        print(f"added user: {str(user)}")
        SESSION.add(user)
        SESSION.commit()
        SESSION.close()
        return user


def add_user_object(user: User) -> None:
    """
    Add a user object to the database.

    Args:
        user (User): The user object to be added.

    Returns:
        None
    """
    with USER_INSERTION_LOCK:
        prev_user = SESSION.query(User).filter(User.user_id == user.user_id).first()
        if prev_user:
            SESSION.close()
            return
        SESSION.add(user)
        SESSION.commit()
        SESSION.close()


def get_user(user_id: int) -> User:
    """
    Retrieve a user from the database based on the user ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user object corresponding to the given user ID.
    """
    return SESSION.query(User).filter(User.user_id == user_id).first()


def filter_users_by_access_level(
    access_levels: list = [UserLevel.Admin, UserLevel.Editor, UserLevel.Ordinary],
) -> List[User]:
    """
    Filter users by access levels.

    Args:
        access_levels (list, optional): List of access levels to filter by. Defaults to [UserLevel.Admin, UserLevel.Editor, UserLevel.Ordinary].

    Returns:
        List[User]: List of users matching the specified access levels.
    """
    return SESSION.query(User).filter(User.level in access_levels).all()


def update_user_access_level(user_id: int, access_level: int) -> None:
    """
    Update the access level of a user.

    Args:
        user_id (int): The ID of the user.
        access_level (int): The new access level.

    Returns:
        None
    """
    with USER_INSERTION_LOCK:
        SESSION.query(User).filter(User.user_id == user_id).update(
            {User.access_level: UserLevel(access_level).name}, synchronize_session=False
        )
        SESSION.commit()
        SESSION.close()
        usercache.update_user_permission(user_id, access_level)


def toggle_bookmark(user_id: int, submission_id: int) -> int:
    """
    Toggles the bookmark status of a submission for a user.

    Args:
        user_id (int): The ID of the user.
        submission_id (int): The ID of the submission.

    Returns:
        int: The result of the toggle operation:
            -1: Bookmark removed.
             0: Something went wrong.
             1: Bookmark added.
    """
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user_id).first()
        submission = (
            SESSION.query(Submission).filter(Submission.id == submission_id).first()
        )
        result = 0
        if user is None or submission is None:
            result = 0  # Something went wrong
        elif submission in user.bookmarks:
            user.bookmarks.remove(submission)
            search_engine.decrease_likes(submission.id)
            usercache.decrease_achieved_likes(submission.owner_id, 1)
            SESSION.commit()
            result = -1  # Bookmark Removed
        elif submission not in user.bookmarks:
            user.bookmarks.append(submission)
            search_engine.increase_likes(submission.id)
            usercache.increase_achieved_likes(submission.owner_id, 1)
            SESSION.commit()
            result = 1  # Bookmark Added

        new_likes = (
            SESSION.query(bookmarks_association)
            .filter(bookmarks_association.c.submission_id == submission.id)
            .count()
        )
        SESSION.close()
        return (result, new_likes)


def add_user_submission(user_id: int, submission: Submission) -> Submission:
    """
    Add a submission to a user's list of submissions.

    Args:
        user_id (int): The ID of the user.
        submission (Submission): The submission to be added.

    Returns:
        Submission: The submission object.
    """
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user_id).first()
        if user is None or submission is None or submission in user.user_submissions:
            SESSION.close()
            return None
        submission.owner = user
        if user.access_level.value >= UserLevel.Editor.value:
            submission.confirm(user)
            SESSION.commit()
            search_engine.index_record(
                id=submission.id,
                search_text=submission.search_text,
                sub_type=submission.submission_type,
                likes=0,
            )
        else:
            SESSION.commit()
        SESSION.expunge(submission)
        SESSION.close()
        return submission


def edit_admin_submission(admin_id: int, submission: Submission) -> bool:
    """
    Edit an admin submission.

    Args:
        admin_id (int): The ID of the admin.
        submission (Submission): The submission to be edited.

    Returns:
        bool: True if the submission was successfully edited, False otherwise.
    """
    with USER_INSERTION_LOCK:
        SESSION.expunge_all()
        admin = (
            SESSION.query(User)
            .filter(User.user_id == admin_id, User.access_level == UserLevel.Admin)
            .first()
        )
        if admin is None:
            SESSION.close()
            return False
        likes = search_engine.get_likes(submission.id)
        search_engine.remove_record(submission.id)
        submission.confirm(admin)
        search_engine.index_record(
            submission.id,
            submission.search_text,
            submission.submission_type,
            likes,
            submission.search_times,
        )
        SESSION.commit()
        SESSION.close()
        return True


def remove_user_submission(user_id: int, submission: Submission) -> bool:
    # FIXME: why there is no `True` return?
    """
    Removes a submission from a user's list of submissions.

    Args:
        user_id (int): The ID of the user.
        submission (Submission): The submission to be removed.

    Returns:
        bool: True if the submission was successfully removed, False otherwise.
    """
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user_id).first()
        if user is None or submission not in user.user_submissions:
            SESSION.close()
            return False
        user.user_submissions.remove(submission)
        SESSION.commit()
        SESSION.close()


def update_user_step(user_id: int, last_step: str) -> None:
    """
    Update the last step of a user in the database.

    Args:
        user_id (int): The ID of the user.
        last_step (str): The last step of the user.

    Returns:
        None
    """
    with USER_INSERTION_LOCK:
        if usercache.has_user(user_id):
            SESSION.query(User).filter(User.user_id == user_id).update(
                {User.last_step: last_step}, synchronize_session=False
            )
            SESSION.commit()
            SESSION.close()
            usercache.update_user_step(user_id, last_step)


def update_user_activity(user_id: int) -> None:
    """
    Update the last active timestamp for a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        None
    """
    with USER_INSERTION_LOCK:
        if usercache.has_user(user_id):
            SESSION.query(User).filter(User.user_id == user_id).update(
                {User.last_active: datetime.utcnow()}, synchronize_session=False
            )
            SESSION.commit()
            SESSION.close()


def get_user_bookmarks(user_id: int) -> List:
    """
    Retrieve the bookmarks of a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List: A list of bookmarks belonging to the user.
    """
    return SESSION.query(User).filter(User.user_id == user_id).first().bookmarks


def count_user_submissions(user_id: int) -> int:
    """
    Count the number of submissions owned by a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        int: The number of submissions owned by the user.
    """
    return SESSION.query(Submission).filter(Submission.owner_id == user_id).count()


def get_user_submissions(user_id: int) -> List[Submission]:
    """
    Retrieve all submissions owned by a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Submission]: A list of Submission objects owned by the user.
    """
    return SESSION.query(Submission).filter(Submission.owner_id == user_id).all()


def count_user_bookmarks(user_id: int) -> int:
    """
    Count the number of bookmarks for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        int: The number of bookmarks for the user.
    """
    return (
        SESSION.query(bookmarks_association)
        .filter(bookmarks_association.c.user_id == user_id)
        .count()
    )


def count_active_users(minutes: int) -> int:
    """
    Count the number of active users within the specified time frame.

    Args:
        minutes (int): The number of minutes to consider for user activity.

    Returns:
        int: The count of active users.

    """
    return (
        SESSION.query(User)
        .filter(User.last_active >= datetime.utcnow() - timedelta(minutes=minutes))
        .count()
    )


def count_new_signups(minutes: int) -> int:
    """
    Count the number of new signups within the specified number of minutes.

    Args:
        minutes (int): The number of minutes to look back for new signups.

    Returns:
        int: The count of new signups within the specified time frame.
    """
    return (
        SESSION.query(User)
        .filter(User.signup_date >= datetime.utcnow() - timedelta(minutes=minutes))
        .count()
    )


def list_users() -> List[User]:
    """
    Retrieve a list of all users from the database.

    Returns:
        List[User]: A list of User objects.
    """
    return SESSION.query(User).all()


def count_users() -> int:
    """
    Counts the number of users in the user cache.

    Returns:
        int: The number of users in the user cache.
    """
    return len(usercache.users)


def count_admins() -> int:
    """
    Counts the number of administrators in the user cache.

    Returns:
        int: The number of administrators.
    """
    return sum(1 for user in usercache.users.values() if user.permission == 3)


def count_editors() -> int:
    """
    Counts the number of users with editor permission.

    Returns:
        int: The number of users with editor permission.
    """
    return sum(1 for user in usercache.users.values() if user.permission == 2)
