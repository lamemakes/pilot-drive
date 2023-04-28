"""
Media service constants
"""
from enum import StrEnum


class MediaSources(StrEnum):
    """
    Enum of all possible media types
    """

    BLUETOOTH = "bluetooth"
    RADIO = "radio"
    FILES = "files"


class TrackStatus(StrEnum):
    """
    Enum used for the track status states

    Status state docs: https://github.com/bluez/bluez/blob/master/doc/media-api.txt#L271-#L275
    """

    PLAYING = "playing"
    STOPPED = "stopped"
    PAUSED = "paused"
    FORWARD_SEEK = "forward-seek"
    REVERSE_SEEK = "reverse-seek"
    ERROR = "error"


class TrackControl(StrEnum):
    """
    Enum used to handle values passed from the frontend regarding track control
    """

    PAUSE = "pause"
    PLAY = "play"
    NEXT = "next"
    PREV = "prev"


class TrackAttributes(StrEnum):
    """
    Enum used for the track attributes.

    Bluez docs: https://github.com/bluez/bluez/blob/master/doc/media-api.txt#L288-#L320
    """

    TITLE = "Title"  # Responsible for most metadata on the tracks
    ALBUM = "Album"  # Provides track state such as idle or active
    ARTIST = "Artist"
    DURATION = "Duration"
    GENRE = "Genre"
    TRACK_NUMBER = "TrackNumber"
    NUMBER_OF_TRACKS = "NumberOfTracks"
