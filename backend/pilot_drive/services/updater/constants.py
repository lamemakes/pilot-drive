"""
The constants of the PILOT Drive Updater
"""

from enum import StrEnum


class UpdateCommands(StrEnum):
    """
    The update commands that the UI sends to update
    """
    UPDATE = "update"
    CHECK = "check"


class PipRegex(StrEnum):
    """
    ReGex enum for pip outputs  
    """
    # RegEx string used to check if stderr if just a pip update notification
    PIP_UPDATE_REGEX = (
        r"^\\n\[notice\] A new release of pip is available: "
        r"\d{1,3}\.\d{1,3}\.\d{1,3} -> \d{1,3}\.\d{1,3}\.\d{1,3}\\n\[notice\] "
        r"To update, run: python3 -m pip install --upgrade pip\\n$"
    )
    NETWORK_ERROR_REGEX = (
        "Failed to establish a new connection: "
        r"\[Errno -3\] Temporary failure in name resolution'\)"
    )
    PACKAGE_ERROR_REGEX = "ERROR: No matching distribution found for"


UPDATE_RECORD_PATH = "/tmp/pd_update.json"
