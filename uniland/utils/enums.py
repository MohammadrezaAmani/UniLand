import enum


class UserLevel(enum.Enum):
    Ordinary = 1
    Editor = 2
    Admin = 3
  


class DocType(enum.Enum):
    BOOK = "کتاب"  # AND RESOURCE
    Pamphlet = "جزوه"  # AND KHOLASE
    Exercises = "تمرینات"  # AND NEMOONE SOAL
    CompressedFile = "ترکیبی"  # AND ZIP

'''
class CallbackCondition(enum.Enum):
  PVSEARCH = 'pvsearch'
  BOOKMARKS = 'bookmarkspage'
  MYSUBS = 'mysubmission'
'''
