import enum


class UserLevel(enum.Enum):
    Ordinary = 1
    Editor = 2
    Admin = 3


class DocType(enum.Enum):
    Pamphlet = 'جزوه'
    Summary = 'خلاصه'
    Exercises = 'تمرینات'
    ExampleProblems = 'نمونه سوالات'
    CompressedFile = 'فایل فشرده'
