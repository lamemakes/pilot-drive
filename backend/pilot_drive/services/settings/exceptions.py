"""
Exceptions of the Settings service
"""


class InvalidAttributeException(Exception):
    """
    Raised when an invalid attribute is used in the set_setting or get_setting methods
    """


class FailedToReadSettingsException(Exception):
    """
    Raised when the settings could not be read
    """
