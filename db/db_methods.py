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
