import os


class UserRecord:

    permission_values = {"Admin": 3, "Editor": 2, "Ordinary": 1}

    def __init__(
        self, user_id: int, permission, last_step: str, achieved_likes: int = 0
    ):
        self.user_id = user_id
        self.update_permission(permission)
        self.last_step = last_step.strip().lower() if last_step else ""
        self.achieved_likes = achieved_likes

    def update_permission(self, permission):
        if permission in self.permission_values.keys():
            self.permission = self.permission_values[permission]
        else:
            self.permission = permission

    def has_permission(self, min_permission: int = 1, max_permission: int = 3):
        return self.permission >= min_permission and self.permission <= max_permission

    def __repr__(self):
        return str(
            {
                "id": self.user_id,
                "permission": self.permission,
                "last_step": self.last_step,
            }
        )


# -----------------------------------------------------------------------


class UserCache:
    def __init__(self):
        self.users = {}  # int id -> UserRecord

    def add_user(self, user_id: int, permission, last_step: str):
        user = UserRecord(user_id, permission, last_step)

        self.users[user_id] = user

    def update_user_permission(self, user_id: int, permission):
        if user_id not in self.users:
            return

        self.users[user_id].update_permission(permission)

    def update_user_step(self, user_id: int, last_step: str):
        if user_id not in self.users:
            return

        self.users[user_id].last_step = last_step.strip().lower()

    def increase_achieved_likes(self, user_id: int, amount: int = 1):
        if user_id not in self.users:
            return
        self.users[user_id].achieved_likes += amount

    def decrease_achieved_likes(self, user_id: int, amount: int = 1):
        if user_id not in self.users:
            return
        self.users[user_id].achieved_likes -= amount

    def get_achieved_likes(self, user_id: int):
        if user_id not in self.users:
            return 0
        return self.users[user_id].achieved_likes

    @property
    def total_users(self):
        return len(self.users)

    def remove_user(self, user_id: int):
        if user_id not in self.users:
            return None

        user = self.users[user_id]
        del self.users[user_id]
        return user

    def has_user(self, user_id: int):
        return user_id in self.users

    def match_step(self, user_id: int, step: str):
        if user_id not in self.users:
            return False
        return self.users[user_id].last_step == step.strip().lower()

    def has_permission(
        self, user_id: int, min_permission: int = 1, max_permission: int = 3
    ):
        if user_id not in self.users:
            return False
        return self.users[user_id].has_permission(min_permission, max_permission)

    def get_last_step(self, user_id: int):
        return self.users[user_id].last_step

    def __repr__(self):
        return f"UserCache with {len(self.users)} users"
