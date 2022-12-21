import threading
from uniland import SESSION, search_engine
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
    submission = SESSION.query(Submission).filter(
      Submission.id == submission_id).first()
    if submission:
      submission.confirm(user_db.get_user(admin_id))
      search_engine.index_record(id=submission.id,
                                 search_text=submission.search_text,
                                 sub_type=submission.submission_type,
                                 likes=0)
      SESSION.commit()
    SESSION.close()


def get_submission(submission_id: int):
  return SESSION.query(Submission).filter(
    Submission.id == submission_id).first()


def get_unconfirmed_submissions():
  subs = SESSION.query(Submission).filter(
    Submission.is_confirmed == False).order_by(
      Submission.submission_date.desc()).all()
  SESSION.expunge_all()
  SESSION.close()
  return subs


def is_pending(submission_id: int):
  submission = SESSION.query(Submission).filter(
    Submission.id == submission_id).first()
  if submission:
    return not submission.is_confirmed
  return False


def count_total_submissions():
  return SESSION.query(Submission).count()


def count_confirmed_submissions():
  return len(search_engine.subs)


def delete_submission(submission_id: int):
  with SUBMISSION_INSERTION_LOCK:
    submission = SESSION.query(Submission).filter(
      Submission.id == submission_id).first()
    if submission:
      SESSION.delete(submission)
      SESSION.commit()
    SESSION.close()
