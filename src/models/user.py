from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_id, username, first_name, last_name, role):
        self._user_id = user_id
        self._username = username
        self._first_name = first_name
        self._last_name = last_name
        self._role = role

    @property
    def user_id(self):
        return self._user_id

    @property
    def username(self):
        return self._username

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    @property
    def role(self):
        return self._role

    @abstractmethod
    def get_permissions(self):
        pass

class Receptionist(User):
    def get_permissions(self):
        return ["manage_vehicles", "manage_users", "view_all_reservations"]

class Worker(User):
    def get_permissions(self):
        return ["update_logs", "view_returns"]

class Member(User):
    def get_permissions(self):
        return ["search_vehicles", "reserve_vehicle", "view_my_reservations"]

class Admin(User):
    def get_permissions(self):
        return ["all_access"]
