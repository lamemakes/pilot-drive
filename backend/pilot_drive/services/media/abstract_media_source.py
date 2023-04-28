"""
Abstract media managers & their data types
"""
from abc import ABC, abstractmethod
from types import NoneType
from typing import Callable, TypedDict, Union

from pilot_drive.master_logging import MasterLogger


class TrackProps(TypedDict):
    """
    A typed dict used to store Track metadata
    """

    title: Union[str, NoneType]
    artist: Union[str, NoneType]
    album: Union[str, NoneType]
    duration: Union[int, NoneType]


class BaseMediaSource(ABC):
    """
    The base class for a media manager
    """

    def __init__(self, push_to_queue_callback: Callable, logger: MasterLogger) -> None:
        """
        Initialize the media manager

        :param push_to_queue_callback: method that pushes new events to the queue
        :param logger: an instance of the MasterLogger
        """
        self.push_to_queue = push_to_queue_callback
        self.logger = logger

    def push_media_to_queue(self) -> None:
        """
        Pushes media info to the queue utilizing the callback provided in initializer
        """
        track = self.track
        media_event = {
            "title": track.get("Title"),
            "artist": track.get("Artist"),
            "album": track.get("Album"),
            "duration": self.track.get("Duration"),
            "position": self.position,
            "playing": self.playing,
            "cover": None,
        }
        self.push_to_queue(media_event)

    @property
    @abstractmethod
    def track(self) -> TrackProps:
        """
        Get the track metadata

        :return: a dict of Title, Artist, Album, and Duration with corresponding values.
        """

    @property
    @abstractmethod
    def playing(self) -> bool:
        """
        Get whether the current track is playing

        :return: a boolean of True if playing and False if not playing
        """

    @property
    @abstractmethod
    def position(self) -> int:
        """
        Get the track position

        :return: track position in milliseconds
        """

    @abstractmethod
    def main(self) -> None:
        """
        The main method to be implemented by media managers
        """
