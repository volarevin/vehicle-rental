class User:
    def __init__(self, user_id, username, first_name, last_name, role):
        self._user_id = user_id
        self._username = username
        self._first_name = first_name
        self._last_name = last_name
        self._role = role

    def get_user_id(self):
        return self._user_id

    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    def get_first_name(self):
        return self._first_name

    def set_first_name(self, first_name):
        self._first_name = first_name

    def get_last_name(self):
        return self._last_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def get_full_name(self):
        return str(self._first_name) + " " + str(self._last_name)

    def get_role(self):
        return self._role

    def set_role(self, role):
        self._role = role

    def update_profile_info(self, username, first_name, last_name):
        self.set_username(username)
        self.set_first_name(first_name)
        self.set_last_name(last_name)

    def get_permissions(self):
        raise NotImplementedError("Child class must implement get_permissions")

    user_id = property(get_user_id)
    username = property(get_username, set_username)
    full_name = property(get_full_name)
    role = property(get_role, set_role)

class Receptionist(User):
    def get_permissions(self):
        return ["manage_vehicles", "manage_users", "view_all_reservations", "update_logs", "view_returns"]

class Member(User):
    def get_permissions(self):
        return ["search_vehicles", "reserve_vehicle", "view_my_reservations"]

class Admin(User):
    def get_permissions(self):
        return ["all_access"]
