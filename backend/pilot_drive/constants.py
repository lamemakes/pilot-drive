from enum import Enum
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

'''
Constants for bluetooth
((enums are cool!))
'''

class IFaceTypes(Enum):
    '''
    Enum used to properly address/pull different interfaces

    Bluez media API docs: https://github.com/bluez/bluez/blob/master/doc/media-api.txt
    '''
    BLUEZ = 'org.bluez'                                 # Overarching bluez DBus interface
    MEDIA_PLAYER_1 = 'org.bluez.MediaPlayer1'           # Responsible for most metadata on the tracks, provides title, artist, album, duration, postion, etc.
    MEDIA_TRANSPORT_1 = 'org.bluez.MediaTransport1'     # Provides track state such as idle or active
    MEDIA_FOLDER_1 = 'org.bluez.MediaFolder1'
    MEDIA_ITEM_1 = 'org.bluez.MediaItem1'               # Also can be a metadata provider for tracks, not used currently.
    DEVICE_1 = 'org.bluez.Device1'                      # Used to pull device info            


class MediaPlayerAttributes(Enum):
    '''
    Enum used for interacting with the bluez MediaPlayer

    Bluez media API docs: https://github.com/bluez/bluez/blob/master/doc/media-api.txt
    '''
    NAME = 'Name'
    SHUFFLE = 'Shuffle'
    REPEAT = 'Repeat'
    SCAN = 'Scan'
    STATUS = 'Status'
    POSITION = 'Position'
    TRACK = 'Track'
    TYPE = 'Type'
    SUBTYPE = 'Subtype'
    BROWSABLE = 'Browsable'
    SEARCHABLE = 'Searchable'

class MediaItemAttributes(Enum):
    METADATA = 'Metadata'


class MediaTransportAttributes(Enum):
    STATE = 'State'


class Status(Enum):
    PLAYING = 'playing'
    STOPPED = 'stopped'
    PAUSED = 'paused'
    FORWARD_SEEK = 'forward-seek'
    REVERSE_SEEK = 'reverse-seek'
    ERROR = 'error'


class TrackAttributes(Enum):
    '''
    Enum used for getting/setting different track attributes.

    Bluez docs: https://github.com/bluez/bluez/blob/master/doc/
    '''
    TITLE = 'Title'           # Responsible for most metadata on the tracks, provides title, artist, album, duration, postion, etc.
    ALBUM = 'Album'     # Provides track state such as idle or active
    ARTIST = 'Artist'
    DURATION = 'Duration'
    GENRE = 'Genre'
    TRACK_NUMBER = 'TrackNumber'
    NUMBER_OF_TRACKS = 'NumberOfTracks'


class BluetoothDevice(Enum):
    '''
    Enum used for getting device attributes

    Bluez device API docs: https://github.com/bluez/bluez/blob/master/doc/device-api.txt
    '''
    CONNECTED = 'Connected'
    ADDRESS = 'Address'
    NAME = 'Name'
    ALIAS = 'Alias'
    TRUSTED = 'Trusted'
    RSSI = 'RSSI'
    PAIRED = 'Paired'
    UUIDS = 'UUIDs'
    ICON = 'Icon'


class MediaSources(Enum):
    BLUETOOTH = 'bluetooth'
    RADIO = 'radio'
    FILES = 'files'