import threading
from uniland import SESSION, search_engine, usercache
from uniland.db.tables import Submission
from uniland.db import user_methods as user_db
"""
Submission Class Properties:
	- id: int
	- submission_data: datetime
	- is_confirmed: bool
	- faculty: str
	- search_text: str
	- description: str
	- correspondent_admin: int - -> fk user.user_id
	- owner: int - -> fk user.user_id
"""

SUBMISSION_INSERTION_LOCK = threading.RLock()


def increase_search_times(id: int):
  with SUBMISSION_INSERTION_LOCK:
    submission = SESSION.query(Submission).filter(Submission.id == id).first()
    if submission:
      submission.search_times += 1
      search_engine.increase_search_times(id)
      SESSION.commit()
    SESSION.close()


def confirm_user_submission(admin_id: int, submission_id: int):
  admin = user_db.get_user(admin_id)
  if admin == None:
    return
  with SUBMISSION_INSERTION_LOCK:
    submission = (SESSION.query(Submission).filter(
      Submission.id == submission_id).first())
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
  with SUBMISSION_INSERTION_LOCK:
    target_submission = (SESSION.query(Submission).filter(
      Submission.id == submission_id).first())
    # Also decrease search times and achieved likes from usercache and search engine
    if not target_submission:
      SESSION.close()
      return False

    for user in target_submission.liked_users:
      usercache.decrease_achieved_likes(user.user_id,
                                        amount=search_engine.get_likes(
                                          target_submission.id))

    total_searches = target_submission.search_times

    if target_submission.id in search_engine.subs:
      search_engine.remove_record(target_submission.id)
    target_submission.liked_users.clear()
    SESSION.commit()

    for submission in SESSION.query(Submission).filter(Submission.is_confirmed == True).all():
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


def get_submission(submission_id: int):
  """search in database for a submission with given id and return it

    Args:
        submission_id (int): id of the submission

    Returns:
        tuple: (Submission, bool) -> (submission, is_confirmed)
    """
  submission = (SESSION.query(Submission).filter(
    Submission.id == submission_id).first())
  SESSION.refresh(submission)
  SESSION.expunge_all()
  SESSION.close()
  return submission


def get_unconfirmed_submissions():
  subs = (SESSION.query(Submission).filter(
    Submission.is_confirmed == False).order_by(
      Submission.submission_date.desc()).all())
  SESSION.expunge_all()
  SESSION.close()
  return subs


def is_pending(submission_id: int):
  submission = (SESSION.query(Submission).filter(
    Submission.id == submission_id).first())
  if submission:
    return not submission.is_confirmed
  return False


def count_total_submissions():
  return SESSION.query(Submission).count()


def count_confirmed_submissions():
  return len(search_engine.subs)
