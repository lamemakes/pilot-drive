"""
Exceptions of the Bluetooth service
"""


class NoAdapterException(Exception):
    """
    Raised when there is no BlueZ adapter found on DBus
    """


class NoPlayerException(Exception):
    """
    Raised when there is no BlueZ media player found on DBus
    """
