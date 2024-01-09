class UserRecord:
    """
    Represents a user record with information such as user ID, permission level, last step, and achieved likes.
    """

    permission_values = {"Admin": 3, "Editor": 2, "Ordinary": 1}

    def __init__(
        self, user_id: int, permission, last_step: str, achieved_likes: int = 0
    ):
        """
        Initializes a UserRecord object.

        Args:
            user_id (int): The ID of the user.
            permission (str or int): The permission level of the user. Can be a string value ("Admin", "Editor", "Ordinary") or an integer value.
            last_step (str): The last step performed by the user.
            achieved_likes (int, optional): The number of likes achieved by the user. Defaults to 0.
        """
        self.user_id = user_id
        self.update_permission(permission)
        self.last_step = last_step.strip().lower() if last_step else ""
        self.achieved_likes = achieved_likes

    def update_permission(self, permission):
        """
        Updates the permission level of the user.

        Args:
            permission (str or int): The new permission level. Can be a string value ("Admin", "Editor", "Ordinary") or an integer value.
        """
        if permission in self.permission_values.keys():
            self.permission = self.permission_values[permission]
        else:
            self.permission = permission

    def has_permission(self, min_permission: int = 1, max_permission: int = 3):
        """
        Checks if the user has a permission level within the specified range.

        Args:
            min_permission (int, optional): The minimum permission level to check. Defaults to 1.
            max_permission (int, optional): The maximum permission level to check. Defaults to 3.

        Returns:
            bool: True if the user has a permission level within the specified range, False otherwise.
        """
        return self.permission >= min_permission and self.permission <= max_permission

    def __repr__(self):
        """
        Returns a string representation of the UserRecord object.

        Returns:
            str: A string representation of the UserRecord object.
        """
        return str(
            {
                "id": self.user_id,
                "permission": self.permission,
                "last_step": self.last_step,
            }
        )


# -----------------------------------------------------------------------


class UserCache:
    """
    A class that represents a cache of user records.

    Attributes:
        users (dict): A dictionary that maps user IDs to UserRecord objects.

    Methods:
        add_user(user_id, permission, last_step): Adds a new user to the cache.
        update_user_permission(user_id, permission): Updates the permission of a user.
        update_user_step(user_id, last_step): Updates the last step of a user.
        increase_achieved_likes(user_id, amount): Increases the achieved likes of a user.
        decrease_achieved_likes(user_id, amount): Decreases the achieved likes of a user.
        get_achieved_likes(user_id): Returns the achieved likes of a user.
        total_users(): Returns the total number of users in the cache.
        remove_user(user_id): Removes a user from the cache.
        has_user(user_id): Checks if a user exists in the cache.
        match_step(user_id, step): Checks if a user's last step matches a given step.
        has_permission(user_id, min_permission, max_permission): Checks if a user has a permission level within a given range.
        get_last_step(user_id): Returns the last step of a user.
    """

    def __init__(self):
        self.users = {}  # int id -> UserRecord

    def add_user(self, user_id: int, permission, last_step: str):
        """
        Adds a new user to the cache.

        Args:
            user_id (int): The ID of the user.
            permission: The permission level of the user.
            last_step (str): The last step performed by the user.
        """
        user = UserRecord(user_id, permission, last_step)

        self.users[user_id] = user

    def update_user_permission(self, user_id: int, permission):
        """
        Updates the permission of a user.

        Args:
            user_id (int): The ID of the user.
            permission: The new permission level of the user.
        """
        if user_id not in self.users:
            return

        self.users[user_id].update_permission(permission)

    def update_user_step(self, user_id: int, last_step: str):
        """
        Updates the last step of a user.

        Args:
            user_id (int): The ID of the user.
            last_step (str): The new last step performed by the user.
        """
        if user_id not in self.users:
            return

        self.users[user_id].last_step = last_step.strip().lower()

    def increase_achieved_likes(self, user_id: int, amount: int = 1):
        """
        Increases the achieved likes of a user.

        Args:
            user_id (int): The ID of the user.
            amount (int): The amount by which to increase the achieved likes. Default is 1.
        """
        if user_id not in self.users:
            return
        self.users[user_id].achieved_likes += amount

    def decrease_achieved_likes(self, user_id: int, amount: int = 1):
        """
        Decreases the achieved likes of a user.

        Args:
            user_id (int): The ID of the user.
            amount (int): The amount by which to decrease the achieved likes. Default is 1.
        """
        if user_id not in self.users:
            return
        self.users[user_id].achieved_likes -= amount

    def get_achieved_likes(self, user_id: int):
        """
        Returns the achieved likes of a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            int: The achieved likes of the user.
        """
        if user_id not in self.users:
            return 0
        return self.users[user_id].achieved_likes

    @property
    def total_users(self):
        """
        Returns the total number of users in the cache.

        Returns:
            int: The total number of users.
        """
        return len(self.users)

    def remove_user(self, user_id: int):
        """
        Removes a user from the cache.

        Args:
            user_id (int): The ID of the user.

        Returns:
            UserRecord or None: The removed user record, or None if the user does not exist.
        """
        if user_id not in self.users:
            return None

        user = self.users[user_id]
        del self.users[user_id]
        return user

    def has_user(self, user_id: int):
        """
        Checks if a user exists in the cache.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return user_id in self.users

    def match_step(self, user_id: int, step: str):
        """
        Checks if a user's last step matches a given step.

        Args:
            user_id (int): The ID of the user.
            step (str): The step to match.

        Returns:
            bool: True if the user's last step matches the given step, False otherwise.
        """
        if user_id not in self.users:
            return False
        return self.users[user_id].last_step == step.strip().lower()

    def has_permission(
        self, user_id: int, min_permission: int = 1, max_permission: int = 3
    ):
        """
        Checks if a user has a permission level within a given range.

        Args:
            user_id (int): The ID of the user.
            min_permission (int): The minimum permission level. Default is 1.
            max_permission (int): The maximum permission level. Default is 3.

        Returns:
            bool: True if the user has a permission level within the given range, False otherwise.
        """
        if user_id not in self.users:
            return False
        return self.users[user_id].has_permission(min_permission, max_permission)

    def get_last_step(self, user_id: int):
        """
        Returns the last step of a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            str: The last step performed by the user.
        """
        return self.users[user_id].last_step

    def __repr__(self):
        return f"UserCache with {len(self.users)} users"
