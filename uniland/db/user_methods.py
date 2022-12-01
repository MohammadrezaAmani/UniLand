import threading
from uniland import SESSION
from uniland.db.tables import User, Submission
from uniland import usercache
from uniland.utils.enums import UserLevel

USER_INSERTION_LOCK = threading.RLock()  # neccessay for add, remove & update


def add_user(user_id: int, last_step: str = ''):
  with USER_INSERTION_LOCK:
    user = SESSION.query(User).filter(User.user_id == user_id).first()
    if user:
      SESSION.close()
      return user
    user = User(user_id, last_step=last_step)
    print(f'add user: {str(user)}')
    usercache.add_user(user_id, 1, 'start')
    SESSION.add(user)
    SESSION.commit()
    SESSION.close()
    return user


def add_user_object(user: User):
  with USER_INSERTION_LOCK:
    prev_user = SESSION.query(User).filter(
      User.user_id == user.user_id).first()
    if prev_user:
      SESSION.close()
      return
    SESSION.merge(user)
    SESSION.commit()
    SESSION.close()


def get_user(user_id: int):
  with USER_INSERTION_LOCK:
    user = SESSION.query(User).get(user_id)
    if user:
      return user
    SESSION.close()
    return None


def check_admin(user_id: int):
  with USER_INSERTION_LOCK:
    user = SESSION.query(User).get(user_id)
    if user:
      return user.level == UserLevel.Admin
    SESSION.close()
    return False


def filter_users_by_access_level(
  access_levels: list = [
    UserLevel.Admin, UserLevel.Editor, UserLevel.Ordinary
  ]):
  with USER_INSERTION_LOCK:
    return SESSION.query(User).filter(User.level in access_levels).all()


def add_bookmark(user_id: int, submission: Submission) -> bool:
  with USER_INSERTION_LOCK:
    user = SESSION.query(User).filter(User.user_id == user.user_id).first()
    if user == None or submission in user.boomarks:
      SESSION.close()
      return False
    user.bookmarks.append(submission)
    SESSION.commit()
    SESSION.close()


def remove_bookmark(user_id: int, submission: Submission) -> bool:
  with USER_INSERTION_LOCK:
    user = SESSION.query(User).filter(User.user_id == user.user_id).first()
    if user == None or not submission in user.boomarks:
      SESSION.close()
      return False
    user.bookmarks.remove(submission)
    SESSION.commit()
    SESSION.close()


def add_user_submission(user_id: int, submission: Submission) -> bool:
  with USER_INSERTION_LOCK:
    user = SESSION.query(User).filter(User.user_id == user.user_id).first()
    if user == None or submission in user.user_submissions:
      SESSION.close()
      return False
    user.user_submissions.append(submission)
    SESSION.commit()
    SESSION.close()


def remove_user_submission(user_id: int, submission: Submission) -> bool:
  with USER_INSERTION_LOCK:
    user = SESSION.query(User).filter(User.user_id == user.user_id).first()
    if user == None or not submission in user.user_submissions:
      SESSION.close()
      return False
    user.user_submissions.remove(submission)
    SESSION.commit()
    SESSION.close()


def list_users():
  return SESSION.query(User).all()


def count_users():
  return SESSION.query(User).count()
