import time

from pilot_drive.master_logging.MasterLogger import MasterLogger
from pilot_drive.services import AbstractService, ServiceExceptions
from pilot_drive.master_queue.MasterEventQueue import MasterEventQueue, EventType


class CameraManager(AbstractService):
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
            import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
            import picamera
        except ModuleNotFoundError as err:
            raise ServiceExceptions.FailedToInstatiateCamera(
                f"Failed to find a required module, camera service will not be started: {err}"
            )

        self.__GPIO = GPIO

        self.__GPIO.setwarnings(False)  # Ignore warning for now
        self.self.__GPIO.setmode(self.__GPIO.BOARD)  # Use physical pin numbering

        # Create initial state of button
        self.camera_state = False

        # Set button pin to be an input pin and set initial value to be pulled low (off)
        self.__GPIO.setup(btn_pin, self.__GPIO.IN, pull_up_down=self.__GPIO.PUD_DOWN)

        # Create GPIO event for the backup camera, debounce is needed for the button in my experience.
        self.__GPIO.add_event_detect(
            btn_pin, GPIO.RISING, callback=self.show_camera, bouncetime=400
        )

        # Initialize the camera
        try:
            self.camera = picamera.PiCamera()
        except picamera.PiCameraError as err:
            raise ServiceExceptions.FailedToInstatiateCamera(
                f"Failed to open PiCamera: {err}"
            )

    def main(self):
        pass

    def refresh(self):
        pass

    def terminate(self):
        try:
            self.__GPIO.cleanup()
        except AttributeError:  # Most likely indicating that the camera failed to start
            return

    def show_camera(self, channel):
        self.camera_state = not self.camera_state
        self.log.debug("Camera state set to: " + str(self.camera_state))
        if self.camera_state:
            self.camera.start_preview()
        else:
            self.camera.stop_preview()
