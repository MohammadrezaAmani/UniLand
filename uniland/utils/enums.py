import enum


class UserLevel(enum.Enum):
    Ordinary = 1
    Editor = 2
    Admin = 3


class DocType(enum.Enum):
    Pamphlet = 1
    Summary = 2
    Exercises = 3
    ExampleProblems = 4
    CompressedFile = 5
