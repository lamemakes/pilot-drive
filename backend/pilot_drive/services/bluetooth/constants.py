"""
Constants used for Bluetooth functionality.

Most are hardcoded strings created in hopes to mitigate string typo errors (and enums are cool!)
"""
from enum import StrEnum


class PowerStates(StrEnum):
    """
    Enum used for the power states of the Adapter iface

    PowerStates docs: https://github.com/bluez/bluez/blob/master/doc/adapter-api.txt#L280-#L285
    """

    ON = "on"
    OFF = "off"
    OFF_ENABLING = "off-enabling"
    ON_DISABLING = "on-disabling"
    OFF_BLOCKED = "off-blocked"


class WSCommands(StrEnum):
    """
    Enum used to map different commands from the websocket
    """

    START_DISCOVERY = "start-discovery"
    STOP_DISCOVERY = "stop-discovery"
    POWER_OFF = "off-power"
    POWER_ON = "on-power"


# Bluetooth service & GATT UUIDs

# ANCS UUIDs pulled from:
# https://github.com/pzmarzly/ancs4linux/blob/master/ancs4linux/observer/ancs/constants.py#L6-L10
NOTIFICATION_SOURCE_CHAR = "9fbf120d-6301-42d9-8c58-25e699a21dbd"
CONTROL_POINT_CHAR = "69d1d8f3-45e1-49a8-9821-9bbdfdaad9d9"
DATA_SOURCE_CHAR = "22eac6e9-24d6-4bb5-be44-b36ace7c7bfb"
ANCS_CHARS = [NOTIFICATION_SOURCE_CHAR, CONTROL_POINT_CHAR, DATA_SOURCE_CHAR]

# Service/Profile UUIDs, as per:
# https://www.bluetooth.org/docman/handlers/downloaddoc.ashx?doc_id=457082
AUDIO_SOURCE = "0000110a-0000-1000-8000-00805f9b34fb"
AVRCP_UUID = "0000110e-0000-1000-8000-00805f9b34fb"
A2DP_UUID = "0000110d-0000-1000-8000-00805f9b34fb"
MEDIA_UUIDS = [AUDIO_SOURCE, AVRCP_UUID, A2DP_UUID]
