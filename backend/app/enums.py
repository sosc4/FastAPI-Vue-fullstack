from enum import Enum


class LogEvent(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    USER_ADDED = "user_added"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    CONFIG_UPDATED = "config_updated"


class LogStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


__all__ = ["LogEvent", "LogStatus"]
