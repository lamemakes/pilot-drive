"""
Top-level constants for PILOT Drive
"""

import os
import inspect

from pilot_drive import __version__ as VERSION


#
# Absolute filepath to the currently executed PILOT Drive
#

# Ugly and rediculous, pulls constants.py out of the path and just returns the directories
absolute_path = (
    f'{"/".join(os.path.abspath(inspect.getsourcefile(lambda:0)).split("/")[:-1])}/'
)

#
# Constants for the static frontend
#

STATIC_WEB_PORT = 8002
# A relative filepath from the root project directory
STATIC_WEB_PATH = "web/files/"

#
# Constants for the websocket server
#
WS_PORT = 8000

#
# Constants for logging
#

# Logging defaults
LOG_PATH = "/etc/pilot-drive/logging/"
LOG_FILE_NAME = "pilot_drive.log"
DEFAULT_LOG_SETTINGS = {
    "logLevel": 20,
    "logToFile": True,
    "logPath": f"{LOG_PATH}{LOG_FILE_NAME}",
}


#
# Constants for PILOT Drive Settings & it's defaults
#

SETTINGS_PATH = "/etc/pilot-drive/config/"
SETTINGS_FILE_NAME = "settings.json"
# The attribute of the webSettings in the JSON
WEB_SETTINGS_ATTRIBUTE = "webSettings"

DEFAULT_WEB_SETTINGS = {
    "tfHourTime": False,
    "metricUnits": False,
    "selectedTheme": "sherbet",
    "themes": [
        {
            "name": "dark",
            "accent": [131, 52, 45],
            "primary": [28, 30, 33],
            "secondary": [215, 208, 200],
        },
        {
            "name": "light",
            "accent": [221, 113, 98],
            "primary": [236, 241, 250],
            "secondary": [112, 121, 137],
        },
        {
            "name": "sherbet",
            "accent": [182, 215, 168],
            "primary": [234, 153, 153],
            "secondary": [249, 203, 156],
        },
    ],
}

DEFAULT_VEHICLE_STATS = [
    {"name": "Speed", "command": "SPEED", "interval": 0.5, "unit": "MPH"},
    {"name": "RPM", "command": "RPM", "interval": 0.5, "unit": "RPMs"},
    {"name": "Fuel Level", "command": "FUEL_LEVEL", "interval": 10, "unit": "percent"},
    {
        "name": "Voltage",
        "command": "CONTROL_MODULE_VOLTAGE",
        "interval": 3,
        "unit": "V",
    },
]

DEFAULT_BACKEND_SETTINGS = {
    "updates": {
        "projectUrl": "https://pypi.org/pypi/pilot-drive/json",
        "downloadPath": "/tmp/",
    },
    "vehicle": {"enabled": False, "port": None, "stats": DEFAULT_VEHICLE_STATS},
    "phone": {"enabled": False, "type": None},
    "logging": {**DEFAULT_LOG_SETTINGS},
    "camera": {"enabled": False, "buttonPin": 0},
}
