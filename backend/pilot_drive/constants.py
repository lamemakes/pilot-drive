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
STATIC_WEB_PATH = "web/files/"  # A relative filepath from the root project directory

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
WEB_SETTINGS_ATTRIBUTE = "webSettings"  # The attribute of the webSettings in the JSON

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

DEFAULT_BACKEND_SETTINGS = {
    "updates": {
        "projectUrl": "https://pypi.org/pypi/pilot-drive/json",
        "downloadPath": "/tmp/",
    },
    "vehicle": {"enabled": False, "port": None},
    "phone": {"enabled": False, "type": None},
    "logging": {"logLevel": 20, "logToFile": True, "logPath": ""},
    "camera": {"enabled": False, "buttonPin": 0},
}

#
# Constants used for vehicle/OBD functionality
#

# Fields that are queried and pushed to the frontend.
# In the format of:
# {"name": "<name>", "command": "<python OBD command>", "interval": <int second query interval>}

# command fields pulled from python-OBD docs:
# https://python-obd.readthedocs.io/en/latest/Command%20Tables/
QUERIED_FIELDS = (
    {"name": "Speed", "command": "SPEED", "interval": 0.5},
    {"name": "RPM", "command": "RPM", "interval": 0.5},
    {"name": "Fuel Level", "command": "FUEL_LEVEL", "interval": 10},
    {"name": "Voltage", "command": "CONTROL_MODULE_VOLTAGE", "interval": 3},
)
