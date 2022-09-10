# Class to manage the backup camera, shoutout to 
# https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/ 
# for sweet button tips

import logging
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import picamera
import time

class CameraManager:
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

    def __init__(self, btn_pin):
        self.log = logging.getLogger()

        # Create initial state of button
        self.camera_state = False

        # Set button pin to be an input pin and set initial value to be pulled low (off)
        GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Create GPIO event for the backup camera, debounce is needed for the button in my experience.
        GPIO.add_event_detect(btn_pin, GPIO.RISING, callback=self.show_camera, bouncetime=400)

        # Initialize the camera
        try:
            self.camera = picamera.PiCamera()
        except PiCameraError as e:
            self.log.error("Failed to initialize PiCamera!: " + e)

    def show_camera(self, channel):
        self.camera_state = not self.camera_state
        self.log.debug("Camera state set to: " + str(self.camera_state))
        if self.camera_state:
            self.camera.start_preview()
        else:
            self.camera.stop_preview()


if __name__ == "__main__":
    backup_cam = CameraManager(16)
    input("Press Enter to Exit.")