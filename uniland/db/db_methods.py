def add_user(user_id:int, name:str, family:str = '', student_number:int = 0, major:str='',entering_year:int=99, last_step:str='start'):
    """add user to databse

    Args:
        user_id (int): user id
        name (str): user name
        family (str, optional): last name. Defaults to ''.
        student_number (int, optional): student number of user. Defaults to 0.
        major (str, optional): major of user. Defaults to ''.
        entering_year (int, optional): entering year of user. Defaults to 99.
        last_step (str, optional): last step of user. Defaults to 'start'
    Returns:
        _type_: _description_
    """
    is_success = False
    return is_success
def search_document_by_name(text:str):
    """search documents name in database and return a tuple of results
        contains:
            id:int
            dars:str
            professor:str
            writer:str
            likes:int
            dislikes:int
        example:
            (
                (1,'dars1','professor1','writer1',0,0),
                (2,'dars2','professor2','writer2',0,0),
                (3,'dars3','professor3','writer3',0,0),
            )

    Args:
        text (str): name

    Returns:
        tuple: search results
    """
    return (
                (1,'dars1','professor1','writer1',0,0),
                (2,'dars2','professor2','writer2',0,0),
                (3,'dars3','professor3','writer3',0,0),
            )
def search_document(id:int):
    """search documents name in database and return a tuple of results
        contains:
            id:int
            file_id:int
            dars:str
            professor:str
            writer:str
            likes:int
            dislikes:int
        example:
                (1,'ascascascascascasc','dars1','professor1','writer1',0,0),
    Args:
        id (str): name

    Returns:
        tuple: search result
    """
    return (1,'BQACAgQAAxkBAAIDymNm5VBIii8fsU5U5HikFG5__eCuAALaDAACJbbhUU8quAABkUBkSR4E','پایتون','محمدرضا امانی','متردد',1000,0)
def change_last_step(user_id:int, step:str):
    """this function change last step of user in database

    Args:
        user_id (int): user id
        step (str): this is last step of user
    """
def get_last_step(user_id:int):
    """return last step of user

    Args:
        user_id (int): user id

    Returns:
        str: step
    """
    step = 'start'
    return step
def add_like(typed,id):
    pass

# TODO! hazf dislike
# users, requests, document, profile, media
# users: 
"""
    user_id int pk, 
    access_level,
    book_marks(many to many),
    user_documents(one to many),

"""
# requests
"""
    id pk,
    submition_date time(utcnow),
    is_confirmed bool,
    Correspondent_admin many_to_one,
    Correspondent_user many_to_one nullable = False,
    liked_users (many to many, book_mark users)
    search_text str,

"""
# documents (requests)
"""
   file_id str pk,
   course str,
   professor str,
   writer str,
   semester_year int,
   type (document,kholase,ketab,nemone_soal,...) Enum, 
   faculty Enum,
"""
# profile (requests)
"""
    id int pk,
    title str,
    email unique str,
    phone_number str,
    image_link str null True,
    image_id str null True,
    resume_link str null True,
    resume_id str null True,
"""
# media (requests)
"""
    id int pk,
    type enum (link, nima, lmshome, mp4)
    course str,
    professor str,
    semester_year int,
    faculity Enum,
"""