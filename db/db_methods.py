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
def search_jozve_by_name(text:str):
    """search jozves name in database and return a tuple of results
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
def search_jozve(id:int):
    """search jozves name in database and return a tuple of results
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
    return (1,'BQACAgQAAxkBAAIDymNm5VBIii8fsU5U5HikFG5__eCuAALaDAACJbbhUU8quAABkUBkSR4E','درس1','professor1','writer1',0,0)
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
