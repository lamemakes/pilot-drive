from __init__ import __version__ as VERSION


'''
Constants for the static frontend
'''
STATIC_WEB_PORT = 8002
STATIC_WEB_PATH = "./web/files/"

'''
Constants for the websocket server
'''
WS_PORT = 8000 

'''
Constants for PILOT Drive Settings & it's defaults
'''
SETTINGS_PATH = "/etc/pilot-drive/config/"
SETTINGS_FILE_NAME = "settings.json"
WEB_SETTINGS_ATTRIBUTE = "webSettings"  # The attribute of the webSettings in the JSON

DEFAULT_WEB_SETTINGS = {
    "tfHourTime" : False,
    "metricUnits": False,
    "phoneEnabled" : False,
    "vehicleEnabled" : False,
    "selectedTheme" : "sherbet",
    "themes": [
        {
            "name": "dark",
            "accent": [ 131, 52, 45 ],
            "primary": [ 28, 30, 33 ],
            "secondary": [ 215, 208, 200 ]
        },
        {
            "name": "light",
            "accent": [ 221, 113, 98 ],
            "primary": [ 236, 241, 250 ],
            "secondary": [ 112, 121, 137 ]
        },
        {
            "name": "sherbet",
            "accent": [ 182, 215, 168 ],
            "primary": [ 234, 153, 153 ],
            "secondary": [ 249, 203, 156 ]
        },
    ]
}

DEFAULT_BACKEND_SETTINGS = {
    "updates": {
      "projectUrl": "https://pypi.org/pypi/pilot-drive/json",
      "downloadPath": "/tmp/"
    },
    "vehicle": {
      "enabled": False,
      "port": None
    },
    "phone": {
      "enabled": False
    },
    "logging": {
      "logLevel": 20,
      "logToFile": True,
      "logPath": ""
    },
    "camera": {
      "enabled": False,
      "buttonPin": 0
    },
}