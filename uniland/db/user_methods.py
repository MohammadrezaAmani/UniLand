import threading
from uniland import SESSION
from uniland.db.tables import User, Submission, bookmarks_association
from uniland import usercache, search_engine
from uniland.utils.enums import UserLevel
from uniland.utils.steps import UserSteps
from uniland import search_engine as se
import os

USER_INSERTION_LOCK = threading.RLock()


def add_user(user_id: int, last_step: str = UserSteps.START.value):
  with USER_INSERTION_LOCK:
    user = SESSION.query(User).filter(User.user_id == user_id).first()
    if user:
      SESSION.close()
      return user
    user = User(user_id, last_step=last_step)
    user.access_level = UserLevel.Admin  # TODO! REMOVE THIS LINE
    usercache.add_user(user_id, 3, last_step)  # TODO! Change 3 to 1
    print(f"added user: {str(user)}")
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
    SESSION.add(user)
    SESSION.commit()
    SESSION.close()


def get_user(user_id: int):
  return SESSION.query(User).filter(User.user_id == user_id).first()


def filter_users_by_access_level(
        access_levels: list = [
            UserLevel.Admin, UserLevel.Editor, UserLevel.Ordinary
        ]):
  with USER_INSERTION_LOCK:
    return SESSION.query(User).filter(User.level in access_levels).all()


def toggle_bookmark(user_id: int, submission_id: int) -> int:
  # returns total liked submission by user with user_id
  # returns -1 if something went wrong
  with USER_INSERTION_LOCK:
    user = SESSION.query(User).filter(User.user_id == user_id).first()
    submission = SESSION.query(Submission).filter(
        Submission.id == submission_id).first()
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

    new_likes = len(submission.liked_users)
    SESSION.close()
    return (result, new_likes)


def add_user_submission(user_id: int, submission: Submission) -> bool:
  with USER_INSERTION_LOCK:
    print('from add_user_submission: ', user_id)
    user = SESSION.query(User).filter(User.user_id == user_id).first()
    if user == None or submission == None or submission in user.user_submissions:
      SESSION.close()
      return False
    submission.owner = user
    if user.access_level.value == UserLevel.Admin.value:
      print('Has Admin Access')
      submission.confirm(user)
      SESSION.commit()
      search_engine.index_record(id=submission.id,
                                 search_text=submission.search_text,
                                 sub_type=submission.submission_type,
                                 likes=0)
      print(str(submission.owner))
    SESSION.close()
    return True


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
  if usercache.has_user(user_id):
    SESSION.query(User).filter(User.user_id == user_id).update(
        {User.last_step: last_step}, synchronize_session=False)
    SESSION.commit()
    SESSION.close()
    usercache.update_user_step(user_id, last_step)


def get_user_bookmark(user_id: int):
  return SESSION.query(User).filter(User.user_id == user_id).first().bookmarks


def count_user_submissions(user_id: int):
  return SESSION.query(Submission).filter(
      Submission.owner_id == user_id).count()


def get_user_submission(user_id: int):
  return SESSION.query(Submission).filter(Submission.owner_id == user_id).all()


def count_user_bookmarks(user_id: int):
  return SESSION.query(bookmarks_association).filter(
      bookmarks_association.c.user_id == user_id).count()


def list_users():
  return SESSION.query(User).all()


def count_users():
  return len(usercache.users)


def count_admins():
  return sum(1 for user in usercache.users.values() if user.permission == 3)


def count_editors():
  return sum(1 for user in usercache.users.values() if user.permission == 2)
