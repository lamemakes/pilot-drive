"""
Module doing the managing of the PILOT Drive settings
"""
import json
import os

from pilot_drive import constants
from pilot_drive.master_logging.master_logger import MasterLogger
from pilot_drive.services import AbstractService
from pilot_drive.master_queue import MasterEventQueue, EventType
from .ServiceExceptions import InvalidAttributeException, FailedToReadSettingsException


class Settings(AbstractService):
    """
    The service that manages the settings of PILOT Drive, both web and overarching app wise.
    """

    def __init__(
        self,
        master_event_queue: MasterEventQueue,
        service_type: EventType,
        logger: MasterLogger,
    ):
        """
        Initialize the settings service, and create a new settings file/load in a current one.

        :param master_event_queue: the master event queue (message bus) that handles new events
        :param service_type: the EvenType enum that indicated what the service will appear as on
        the event queue
        """
        super().__init__(master_event_queue, service_type, logger)

        # Lock is utilized to prevent an invalid settings file from being overwritten
        self.__settings_lock = False

        self.__full_settings_path = (
            f"{constants.SETTINGS_PATH}{constants.SETTINGS_FILE_NAME}"
        )

        # If a settings file doesn't exist, provide a set of default settings and write the
        # settings file.
        if not os.path.exists(self.__full_settings_path):
            self.__initialize_default_settings()
        else:
            try:
                with open(
                    self.__full_settings_path, "r", encoding="utf-8"
                ) as settings_file:
                    # If the content of the settings file is empty, initialize a new settings
                    # file with default values.
                    if settings_file.readlines() == []:
                        self.__initialize_default_settings()
                    else:
                        settings_file.seek(0)  # Reset pointer
                        self.__settings = json.load(fp=settings_file)
            except json.JSONDecodeError as err:
                self.logger.error(
                    msg=f"""Failed to load JSON from settings file, using defaults!
                     Any modified settings will not be written: {err}"""
                )
                self.__settings_lock = True
                self.__settings = {
                    **constants.DEFAULT_BACKEND_SETTINGS,
                    constants.WEB_SETTINGS_ATTRIBUTE: {
                        **constants.DEFAULT_WEB_SETTINGS
                    },
                }

    def __initialize_default_settings(self):
        """
        Initialize a boilerplate settings file based on the constants.py file.
        """
        self.__settings = {
            **constants.DEFAULT_BACKEND_SETTINGS,
            constants.WEB_SETTINGS_ATTRIBUTE: {**constants.DEFAULT_WEB_SETTINGS},
        }
        os.makedirs(name=constants.SETTINGS_PATH, exist_ok=True)
        self.write_settings()

    def main(self):
        """
        A do-nothing main method. This will be utilized eventually to detect changes to the
         settings.json file, but is just for abstract method purposes now.
        """

    @property
    def web_settings(self) -> dict:
        """
        Gets the settings for the UI, and adds the version info.
        """
        # The UI expects the version in the settings object, but there is no reason to store this
        # in the backend.
        return {
            "version": constants.VERSION,
            **self.__settings.get(constants.WEB_SETTINGS_ATTRIBUTE),
        }

    def set_web_settings(self, web_settings: dict) -> None:
        """
        Setter for web settings. Removes the unneccesary version info, updates the local web
        settings, and saves the new settings.json

        :param web_settings: The web settings returned from the UI, in dict form (JSON parsed)
        """
        setting_changed = False
        for key in web_settings.keys():
            if key != "version":
                try:
                    self.set_setting(attribute=key, value=web_settings[key], web=True)
                    setting_changed = True
                except InvalidAttributeException as err:
                    self.logger.error(msg=f"Invalid web setting used: {err}")

        if setting_changed:
            self.write_settings()

    def write_settings(self) -> None:
        """
        Writes the local settings to the settings.json file based on the path specified in
        constants.py
        """
        if not self.__settings_lock:
            with open(
                self.__full_settings_path, "w", encoding="utf-8"
            ) as settings_file:
                json.dump(obj=self.__settings, fp=settings_file, indent=4)

    def __validate_attribute(self, attribute: str, web: bool):
        """
        Validates that an attribute exists in either web or general settings.

        :param attribute: the intended attribute to check
        :param web: check web settings OR general.
        :raises InvalidAttributeException: When the specified attribute does not exist in settings.
        """
        is_valid_setting = (
            attribute not in self.__settings.keys()
            or attribute == constants.WEB_SETTINGS_ATTRIBUTE
        )
        is_web_setting = (
            web
            and not attribute
            in self.__settings.get(constants.WEB_SETTINGS_ATTRIBUTE).keys()
        )

        if (not web and is_valid_setting) or (web and is_web_setting):
            raise InvalidAttributeException(
                f'Attribute: "{attribute}" does not exist on settings!'
            )

    def get_setting(self, attribute: str, web: bool = False):
        """
        Get the value of a specific attribute from the settings

        :param attribute: the intended attribute to get
        :param web: get from web settings OR general
        """
        self.__validate_attribute(attribute=attribute, web=web)

        try:
            if web:
                return self.__settings[constants.WEB_SETTINGS_ATTRIBUTE][attribute]

            return self.__settings[attribute]
        except InvalidAttributeException as exc:  # The attribute doesn't exist
            invalid_attr_string = f"Invalid attribute to get: {attribute}"
            self.logger.error(msg=invalid_attr_string)
            raise InvalidAttributeException(invalid_attr_string) from exc

    def set_setting(self, attribute: str, value, web: bool = False):
        """
        Set the value of a specific attribute from the settings

        :param attribute: the intended attribute to get
        :param value: the value to be set
        :param web: set an attribute from web settings OR general
        """
        self.__validate_attribute(attribute=attribute, web=web)

        try:
            if web:
                self.__settings[constants.WEB_SETTINGS_ATTRIBUTE][attribute] = value
            else:
                self.__settings[attribute] = value
        except InvalidAttributeException:  # The attribute doesn't exist
            self.logger.error(msg=f"Invalid attribute to get: {attribute}")
            return

    def refresh(self):
        """
        Push the web settings onto the bus again. When the UI is refreshed, it expects a new
        settings event on the bus.
        """
        self.push_to_queue(self.web_settings)

    def terminate(self):
        """
        A do-nothing method for the time being, nothing to cleanup!
        """

    @staticmethod
    def get_raw_settings() -> dict:
        """
        Returns the settings.json in a full dict without any processing or validation. Not
        recommended for use unless you know what you're doing.
        """
        settings_path = f"{constants.SETTINGS_PATH}{constants.SETTINGS_FILE_NAME}"
        if not os.path.exists(settings_path):
            raise FailedToReadSettingsException(
                f'Failed to find settings file at: "{settings_path}"'
            )

        try:
            with open(settings_path, "r", encoding="utf-8") as raw_settings:
                return json.load(fp=raw_settings)
        except json.JSONDecodeError as exc:
            raise FailedToReadSettingsException(
                f"Failed to read settings: {exc}"
            ) from exc
