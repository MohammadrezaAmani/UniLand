import enum


class UserLevel(enum.Enum):
    """
    Enumeration representing the different levels of users.

    Attributes:
      Ordinary (int): Represents an ordinary user.
      Editor (int): Represents an editor user.
      Admin (int): Represents an admin user.
    """

    Ordinary = 1
    Editor = 2
    Admin = 3


class DocType(enum.Enum):
    """
    Enumeration representing different types of documents.
    """

    BOOK = "کتاب"  # AND RESOURCE
    Pamphlet = "جزوه"  # AND KHOLASE
    Exercises = "تمرینات"  # AND NEMOONE SOAL
    CompressedFile = "ترکیبی"  # AND ZIP
    Template = "تمپلیت"  # AND PLANS AND SHEETS


# class CallbackCondition(enum.Enum):
#   """
#   Enum class representing callback conditions.

#   Attributes:
#     PVSEARCH (str): Represents the condition for PV search.
#     BOOKMARKS (str): Represents the condition for bookmarks page.
#     MYSUBS (str): Represents the condition for my submissions.
#   """
#   PVSEARCH = "pvsearch"
#   BOOKMARKS = "bookmarkspage"
#   MYSUBS = "mysubmission"
