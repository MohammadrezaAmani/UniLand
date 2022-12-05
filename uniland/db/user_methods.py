import threading
from uniland import SESSION
from uniland.db.tables import User, Submission
from uniland import usercache, search_engine
from uniland.utils.enums import UserLevel
from uniland.utils.steps import UserSteps

USER_INSERTION_LOCK = threading.RLock()


def add_user(user_id: int, last_step: str = UserSteps.START.value):
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user_id).first()
        if user:
            SESSION.close()
            return user
        user = User(user_id, last_step=last_step)
        user.access_level = UserLevel.Admin # TODO! REMOVE THIS LINE
        usercache.add_user(user_id, 3, last_step) # TODO! Change 3 to 1
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
        SESSION.merge(user)
        SESSION.commit()
        SESSION.close()


def get_user(user_id: int):
    return SESSION.query(User).filter(User.user_id == user_id).first()


def filter_users_by_access_level(
    access_levels: list = [UserLevel.Admin, UserLevel.Editor, UserLevel.Ordinary]
):
    with USER_INSERTION_LOCK:
        return SESSION.query(User).filter(User.level in access_levels).all()

def toggle_bookmark(user_id: int, submission_id: int) -> int:
    # return 1 if added, 0 if something went wrong and 1 if removed
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user_id).first()
        submission = SESSION.query(Submission).filter(Submission.id == submission_id).first()
        if user == None or submission == None:
            SESSION.close()
            return 0
        if submission in user.bookmarks:
            user.bookmarks.remove(submission)
            search_engine.decrease_likes(submission.id)
            SESSION.commit()
            SESSION.close()
            return -1
        if not submission in user.bookmarks:
            user.bookmarks.append(submission)
            search_engine.increase_likes(submission.id)
            SESSION.commit()
            SESSION.close()
            return 1

def add_bookmark(user_id: int, submission: Submission) -> bool:
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user_id).first()
        if user == None or submission in user.boomarks:
            SESSION.close()
            return False
        user.bookmarks.append(submission)
        SESSION.commit()
        SESSION.close()
        search_engine.increase_likes(submission.id)


def remove_bookmark(user_id: int, submission: Submission) -> bool:
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user.user_id).first()
        if user == None or not submission in user.boomarks:
            SESSION.close()
            return False
        user.bookmarks.remove(submission)
        
        SESSION.commit()
        SESSION.close()
        search_engine.decrease_likes(submission.id)


def add_user_submission(user_id: int, submission: Submission) -> bool:
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == User.user_id).first()
        if user == None or submission in user.user_submissions:
            SESSION.close()
            return False
        submission.owner = user
        user.user_submissions.append(submission)
        if user.access_level == UserLevel.Admin:
            submission.confirm(user)
            search_engine.index_record(submission.id,
                                       submission.search_text,
                                       submission.submission_type,
                                       likes = 0)
        SESSION.commit()
        SESSION.close()
        return True


def remove_user_submission(user_id: int, submission: Submission) -> bool:
    with USER_INSERTION_LOCK:
        user = SESSION.query(User).filter(User.user_id == user.user_id).first()
        if user == None or not submission in user.user_submissions:
            SESSION.close()
            return False
        user.user_submissions.remove(submission)
        SESSION.commit()
        SESSION.close()


def update_user_step(user_id: int, last_step: str):
    if usercache.has_user(user_id):
        SESSION.query(User).filter(User.user_id == user_id).update(
            {User.last_step: last_step}, synchronize_session=False
        )
        SESSION.commit()
        SESSION.close()
        usercache.update_user_step(user_id, last_step)


def list_users():
    return SESSION.query(User).all()


def count_users():
    return SESSION.query(User).count()
