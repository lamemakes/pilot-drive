"""
Exceptions of the Vehicle service
"""


class FailedObdConnectionException(Exception):
    """
    Exception raised when an invalid connection is detected, either from an invalid port string, or
    a Python OBD connection failure.
    """


class InvalidQueryException(Exception):
    """
    Exception raised when an query field is detected as specified in the QUERIED_FIELDS
    constants.py.
    """
