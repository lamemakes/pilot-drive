"""
The module that manages the media of PILOT Drive, ie. A/V metadata
"""
from typing import Dict

from pilot_drive.master_logging.master_logger import MasterLogger
from pilot_drive.master_queue import MasterEventQueue, EventType

from .bluetooth_media import BluetoothMedia
from .constants import MediaSources, TrackControl
from ..bluetooth import Bluetooth, NoPlayerException
from ..abstract_service import AbstractService


class Media(AbstractService):
    """
    The service that manages the Media information of PILOT Drive.
    """

    def __init__(
        self,
        master_event_queue: MasterEventQueue,
        service_type: EventType,
        logger: MasterLogger,
    ) -> None:
        """
        Initialize the Media service.

        :param master_event_queue: the master event queue (message bus) that handles new events
        :param service_type: the EvenType enum that indicated what the service will appear as on
        the event queue
        """
        super().__init__(master_event_queue, service_type, logger)
        self.source = MediaSources.BLUETOOTH

    def __push_media_to_queue(self, track_data: Dict[str, str]) -> None:
        media_event = {"source": self.source, "song": {**track_data}}
        self.push_to_queue(event=media_event)

    def track_control(self, action: TrackControl) -> None:
        """
        Handle track control events such as pause, play, skip, and previous.

        :param action: TrackControl enum member indicating the intended action
        """
        match self.source:
            case MediaSources.BLUETOOTH:
                bluetooth = Bluetooth(
                    master_event_queue=self.event_queue,
                    service_type=EventType.BLUETOOTH,
                    logger=self.logger,
                )
                try:
                    media_player = bluetooth.bluez_media_player
                    match action:
                        case TrackControl.PLAY:
                            media_player.Play()
                        case TrackControl.PAUSE:
                            media_player.Pause()
                        case TrackControl.NEXT:
                            media_player.Next()
                        case TrackControl.PREV:
                            media_player.Previous()
                except NoPlayerException:
                    self.logger.warning(
                        f'Track control "{action}" issued but there is no active media player!'
                    )

    def refresh(self) -> None:
        """
        Currently a do-nothing method as there are no events stored within the object to serve
        """

    def main(self) -> None:
        """
        The main method of the Media service, dictates which media manager to use based on media
            type (currently only supports Bluetooth)
        """
        source = MediaSources.BLUETOOTH

        match source:
            case MediaSources.BLUETOOTH:
                bluetooth = Bluetooth(
                    master_event_queue=self.event_queue,
                    service_type=EventType.BLUETOOTH,
                    logger=self.logger,
                )
                media = BluetoothMedia(
                    push_to_queue_callback=self.__push_media_to_queue,
                    bluetooth=bluetooth,
                    logger=self.logger,
                )
            case _:
                raise ValueError(f"Media source {source} is not supported yet!")

        media.main()
