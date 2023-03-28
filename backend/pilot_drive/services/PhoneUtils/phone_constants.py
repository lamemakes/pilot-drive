from dataclasses import dataclass, field
from enum import Enum, StrEnum
from typing import List, Optional


SETTINGS_PATH = "/etc/pilot-drive/config/"
ADB_PACKAGE_NAMES = "adb_packages.json"


# Set of phone types
class PHONE_TYPES(Enum):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

    IOS = "ios"
    ANDROID = "android"


class PHONE_STATES(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    LOCKED = "locked"  # This state is currently for ADB, as if a locked device is connected ADB can't access it.
    UNTRUSTED = (
        "untrusted"  # This is also for ADB, when the device hasn't trusted the host.
    )


@dataclass
class Notification:
    id: int
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
    enabled: bool
    type: Optional[str] = None
    state: Optional[PHONE_STATES] = PHONE_STATES.DISCONNECTED
    notifications: Optional[List[Notification]] = field(default_factory=lambda: [])


class ADB_COMMANDS(StrEnum):
    ADB = "adb"
    ADB_GET_STATE = "adb get-state"
    ADB_DUMP_NOTIFICATIONS = "adb shell dumpsys notification --noredact"
    ADB_GET_PACKAGE_PATH = "adb shell pm path "  # Intended to be combined with the package, hence the space
    ADB_PULL_PACKAGE = (
        "adb pull "  # Intended to be combined with the package path, hence the space
    )
    ADB_DEVICE_NAME = "adb shell dumpsys bluetooth_manager"
    AAPT_HELP = "aapt2 -h"  # Used to test and see if aapt is installed
    AAPT_DUMP_BADGING = "aapt2 dump badging "  # Intended to be combined with the package path, hence the space


class ADB_STATE(StrEnum):
    ADB_NOT_TRUSTED = "error: device unauthorized."  #  Occurs when the adb host hasn't been trusted by the android system.
    ADB_NO_PERMISSIONS = "error: insufficient permissions for device"  # Occurs when the device is locked and ADB persmissions havent been granted
    ADB_NOT_CONNECTED = "error: no devices/emulators found"
    ADB_DEVICE = "device"  # The only state that indicated an actual connection
    ADB_OFFLINE = "offline"
    ADB_BOOTLOADER = "bootloader"


class ADB_NOTIFICATION_ATTRIBUTES(Enum):
    UID = "^ {6}uid="
    OP_PACKAGE = "^ {6}opPkg="
    TITLE = "^ {16}android.title="
    TEXT = "^ {16}android.text="
    TIME = "^ {6}mRankingTimeMs="
