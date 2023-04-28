"""
Module that allows for utilization of PiCamera for backup camera functionality
"""

from pilot_drive.master_logging.master_logger import MasterLogger
from pilot_drive.master_queue.master_event_queue import MasterEventQueue, EventType

from ..abstract_service import AbstractService

from .exceptions import FailedToInstatiateCamera


class Camera(AbstractService):
    """
    The camera class that manages the use of the PiCamera
    """

    def __init__(
        self,
        master_event_queue: MasterEventQueue,
        service_type: EventType,
        logger: MasterLogger,
        btn_pin: int,
    ):
        super().__init__(
            master_event_queue=master_event_queue,
            service_type=service_type,
            logger=logger,
        )

        try:
            # pylint: disable=import-outside-toplevel
            from RPi import GPIO
            import picamera
        except ModuleNotFoundError as exc:
            raise FailedToInstatiateCamera(
                "Failed to find a required module, camera service will not be started."
            ) from exc

        self.gpio = GPIO

        self.gpio.setwarnings(False)  # Ignore warning for now
        self.gpio.setmode(self.gpio.BOARD)  # Use physical pin numbering

        # Create initial state of button
        self.camera_state = False

        # Set button pin to be an input pin and set initial value to be pulled low (off)
        self.gpio.setup(btn_pin, self.gpio.IN, pull_up_down=self.gpio.PUD_DOWN)

        # Create GPIO event for the backup camera, debounce is needed for the button.
        self.gpio.add_event_detect(
            btn_pin, GPIO.RISING, callback=self.show_camera, bouncetime=400
        )

        # Initialize the camera
        try:
            self.camera = picamera.PiCamera()
        except picamera.PiCameraError as exc:
            raise FailedToInstatiateCamera("Failed to open PiCamera!") from exc

    def main(self):
        pass

    def refresh(self):
        pass

    def show_camera(self, channel):
        """
        A callback or add_event_detect, open/close the camera based on the newly detected state

        :param channel: the channel the change was detected on
        """
        self.camera_state = not self.camera_state
        self.logger.debug(
            msg=f"Camera state set to: {self.camera_state}, on channel: {channel}"
        )
        if self.camera_state:
            self.camera.start_preview()
        else:
            self.camera.stop_preview()
