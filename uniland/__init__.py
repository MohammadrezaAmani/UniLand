from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from uniland.db.tables import User, Submission, create_tables
from uniland.utils.search import SearchEngine
from uniland.utils.usercache import UserCache
from uniland.utils.uxhandler import UXTree
from .config import DB_URI


def start() -> scoped_session:
  # Creating db engine and session
  engine = create_engine(DB_URI)
  create_tables(engine)
  session = scoped_session(
      sessionmaker(bind=engine, autoflush=False, expire_on_commit=False))

  # adding users
  usercache = UserCache()
  for user in session.query(User).all():
    usercache.add_user(
        user_id=user.user_id,
        permission=user.access_level.value,
        last_step=user.last_step,
    )

  # Indexing all submissions
  search_engine = SearchEngine()
  for submission in session.query(Submission).all():
    usercache.increase_achieved_likes(submission.owner_id,
                                      len(submission.liked_users))
    if submission.is_confirmed:
      search_engine.index_record(id=submission.id,
                                 search_text=submission.search_text,
                                 sub_type=submission.submission_type,
                                 likes=len(submission.liked_users),
                                 search_times=submission.search_times)

  return (session, search_engine, usercache)


SESSION, search_engine, usercache = start()

ux_tree = UXTree()

print(search_engine)
print(usercache)
