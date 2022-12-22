import threading
from uniland import SESSION
from uniland.db.tables import User, Submission, bookmarks_association
from uniland import usercache, search_engine
from uniland.utils.enums import UserLevel
from uniland.utils.steps import UserSteps
from datetime import datetime, timedelta

USER_INSERTION_LOCK = threading.RLock()


def add_user(user_id: int, last_step: str = UserSteps.START.value):
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


def add_user_object(user: User):
    with USER_INSERTION_LOCK:
        prev_user = SESSION.query(User).filter(User.user_id == user.user_id).first()
        if prev_user:
            SESSION.close()
            return
        SESSION.add(user)
        SESSION.commit()
        SESSION.close()


def get_user(user_id: int):
    return SESSION.query(User).filter(User.user_id == user_id).first()


def filter_users_by_access_level(
    access_levels: list = [UserLevel.Admin, UserLevel.Editor, UserLevel.Ordinary]
):
    return SESSION.query(User).filter(User.level in access_levels).all()


def update_user_access_level(user_id: int, access_level: int):
    with USER_INSERTION_LOCK:
        SESSION.query(User).filter(User.user_id == user_id).update(
            {User.access_level: UserLevel(access_level).name}, synchronize_session=False
        )
        SESSION.commit()
        SESSION.close()
        usercache.update_user_permission(user_id, access_level)


def toggle_bookmark(user_id: int, submission_id: int) -> int:
    # returns total liked submission by user with user_id
    # returns -1 if something went wrong
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user_id).first()
        submission = (
            SESSION.query(Submission).filter(Submission.id == submission_id).first()
        )
        result = 0
        if user == None or submission == None:
            result = 0  # Something went wrong
        elif submission in user.bookmarks:
            user.bookmarks.remove(submission)
            search_engine.decrease_likes(submission.id)
            usercache.decrease_achieved_likes(submission.owner_id, 1)
            SESSION.commit()
            result = -1  # Bookmark Removed
        elif not submission in user.bookmarks:
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


def add_user_submission(user_id: int, submission: Submission) -> bool:
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user_id).first()
        if user == None or submission == None or submission in user.user_submissions:
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


def remove_user_submission(user_id: int, submission: Submission) -> bool:
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user_id).first()
        if user == None or not submission in user.user_submissions:
            SESSION.close()
            return False
        user.user_submissions.remove(submission)
        SESSION.commit()
        SESSION.close()


def update_user_step(user_id: int, last_step: str):
    with USER_INSERTION_LOCK:
        if usercache.has_user(user_id):
            SESSION.query(User).filter(User.user_id == user_id).update(
                {User.last_step: last_step}, synchronize_session=False
            )
            SESSION.commit()
            SESSION.close()
            usercache.update_user_step(user_id, last_step)


def update_user_activity(user_id: int):
    with USER_INSERTION_LOCK:
        if usercache.has_user(user_id):
            SESSION.query(User).filter(User.user_id == user_id).update(
                {User.last_active: datetime.utcnow()}, synchronize_session=False
            )
            SESSION.commit()
            SESSION.close()


def get_user_bookmarks(user_id: int):
    return SESSION.query(User).filter(User.user_id == user_id).first().bookmarks


def count_user_submissions(user_id: int):
    return SESSION.query(Submission).filter(Submission.owner_id == user_id).count()


def get_user_submissions(user_id: int):
    return SESSION.query(Submission).filter(Submission.owner_id == user_id).all()


def count_user_bookmarks(user_id: int):
    return (
        SESSION.query(bookmarks_association)
        .filter(bookmarks_association.c.user_id == user_id)
        .count()
    )


def count_active_users(minutes: int):
    return (
        SESSION.query(User)
        .filter(User.last_active >= datetime.utcnow() - timedelta(minutes=minutes))
        .count()
    )


def count_new_signups(minutes: int):
    return (
        SESSION.query(User)
        .filter(User.signup_date >= datetime.utcnow() - timedelta(minutes=minutes))
        .count()
    )


def list_users():
    return SESSION.query(User).all()


def count_users():
    return len(usercache.users)


def count_admins():
    return sum(1 for user in usercache.users.values() if user.permission == 3)


def count_editors():
    return sum(1 for user in usercache.users.values() if user.permission == 2)
