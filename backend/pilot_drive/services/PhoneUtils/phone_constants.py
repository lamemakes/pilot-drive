"""
Constants for the phone service
"""

from dataclasses import dataclass, field
from enum import Enum, StrEnum
from typing import List, Optional


SETTINGS_PATH = "/etc/pilot-drive/config/"
ADB_PACKAGE_NAMES = "adb_packages.json"


# Set of phone types
class PhoneTypes(Enum):
    """
    The phone types for the phone service
    """

    @classmethod
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

    IOS = "ios"
    ANDROID = "android"


class PhoneStates(Enum):
    """
    All of the PILOT Drive phone states
    """

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    LOCKED = "locked"  # For ADB, device cannot be accessed if locked
    UNTRUSTED = "untrusted"  # For ADB, when the device hasn't trusted the host.
    BLUETOOTH_DISABLED = "bluetooth-disabled"


@dataclass
class Notification:
    """
    Data class used to store a phone notification
    """

    id: int  # pylint: disable=invalid-name
    device: str
    app_id: str
    app_name: str
    title: str
    time: int
    body: Optional[str] = None

    def __eq__(self, other):
        if not isinstance(other, Notification):
            return NotImplemented
        return (
            self.id == other.id
            and self.device == other.device
            and self.app_id == other.app_id
            and self.app_name == other.app_name
            and self.title == other.title
            and self.body == other.body
            and self.time == self.time
        )


@dataclass
class PhoneContainer:
    """
    Data class used to store phone info
    """

    enabled: bool
    type: Optional[str] = None
    state: Optional[PhoneStates] = PhoneStates.DISCONNECTED
    notifications: Optional[List[Notification]] = field(default_factory=lambda: [])


class AdbCommands(StrEnum):
    """
    The commands that are used by ADB
    """

    ADB = "adb"
    ADB_GET_STATE = "adb get-state"
    ADB_DUMP_NOTIFICATIONS = "adb shell dumpsys notification --noredact"
    ADB_GET_PACKAGE_PATH = (
        "adb shell pm path "  # Combined with the package hence the space
    )
    ADB_PULL_PACKAGE = (
        "adb pull "  # Intended to be combined with the package path hence the space
    )
    ADB_DEVICE_NAME = "adb shell dumpsys bluetooth_manager"
    AAPT_HELP = "aapt2 -h"  # Used to test and see if aapt is installed
    AAPT_DUMP_BADGING = (
        "aapt2 dump badging "  # Combine with the package path, hence the space
    )


class AdbState(StrEnum):
    """
    The different ADB responses to determine state
    """

    ADB_NOT_TRUSTED = "error: device unauthorized."
    ADB_NO_PERMISSIONS = "error: insufficient permissions for device"
    ADB_NOT_CONNECTED = "error: no devices/emulators found"
    ADB_DEVICE = "device"
    ADB_OFFLINE = "offline"
    ADB_BOOTLOADER = "bootloader"


class AdbNotificationAttributes(Enum):
    """
    The prefixes of the notification dump
    """

    UID = "^ {6}uid="
    OP_PACKAGE = "^ {6}opPkg="
    TITLE = "^ {16}android.title="
    TEXT = "^ {16}android.text="
    TIME = "^ {6}mRankingTimeMs="
