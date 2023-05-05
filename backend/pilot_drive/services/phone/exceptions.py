"""
The exceptions of the phone service
"""


class NoANCSDeviceConnectedException(Exception):
    """
    Raised when a property of an ANCS device is requested that doesn't exist
    """
