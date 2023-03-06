import json
import os
import constants
import logging

from services import AbstractService
from MasterEventQueue import MasterEventQueue, EventType


class InvalidAttributeException(Exception):
    '''
    Exception raised when an invalid attribute is used in the set_setting or get_setting methods
    '''
    pass

class Settings(AbstractService):
    '''
    The service that manages the settings of PILOT Drive, both web and overarching app wise. 
    '''
    def __init__(self, master_event_queue:MasterEventQueue, service_type:EventType):
        '''
        Initialize the settings service, and create a new settings file/load in a current one.

        :param master_event_queue: the master event queue (message bus) that handles new events
        :param service_type: the EvenType enum that indicated what the service will appear as on the event queue
        '''
        super().__init__(master_event_queue, service_type)

        self.__settings_lock = False    # Lock is utilized to prevent an invalid settings file from being overwritten

        self.__full_settings_path = constants.SETTINGS_PATH + constants.SETTINGS_FILE_NAME

        # If a settings file doesn't exist, provide a set of default settings and write the settings file.
        if not os.path.exists(self.__full_settings_path):
            self.__initialize_default_settings()
        else:
            try:
                with open(self.__full_settings_path, 'r') as fp:
                    # If the content of the settings file is empty, initialize a new settings file with default values.
                    if fp.readlines() == []:
                        self.__initialize_default_settings()
                    else:
                        fp.seek(0)  # Reset pointer
                        self.__settings = json.load(fp=fp)
            except json.JSONDecodeError as err:
                print("Failed to load JSON from settings file, using defaults! Any modified settings will not be written. " + str(err)) # TODO: Add logging !
                self.__settings_lock = True
                self.__settings = {**constants.DEFAULT_BACKEND_SETTINGS, constants.WEB_SETTINGS_ATTRIBUTE:{**constants.DEFAULT_WEB_SETTINGS}}
        

    def __initialize_default_settings(self):
        '''
        Initialize a boilerplate settings file based on the constants.py file.
        '''
        self.__settings = {**constants.DEFAULT_BACKEND_SETTINGS, constants.WEB_SETTINGS_ATTRIBUTE:{**constants.DEFAULT_WEB_SETTINGS}}
        os.makedirs(name=constants.SETTINGS_PATH, exist_ok=True)
        self.write_settings()


    def main(self):
        '''
        A do-nothing main method. This will be utilized eventually to detect changes to the settings.json file, but is just for abstract method purposes now.
        '''
        pass


    def get_web_settings(self):
        '''
        Gets the settings for the UI, and adds the version info.
        '''
        # The UI expects the version in the settings object, but there is no reason to store this in the backend.
        return {"version":constants.VERSION, **self.__settings.get(constants.WEB_SETTINGS_ATTRIBUTE)}


    def set_web_settings(self, web_settings:dict):
        '''
        Setter for web settings. Removes the unneccesary version info, updates the local web settings, and saves the new settings.json

        :param web_settings: The web settings returned from the UI, in dict form (JSON parsed)
        '''
        setting_changed = False
        for key in web_settings.keys():
            if key != "version":
                try:
                    self.set_setting(attribute=key, value=web_settings[key], web=True)
                    setting_changed = True
                except InvalidAttributeException as err:
                    print("Invalid web setting used: " + err)
        
        if setting_changed:
            self.write_settings()


    def write_settings(self):
        '''
        Writes the local settings to the settings.json file based on the path specified in constants.py
        '''
        if not self.__settings_lock:
            with open(self.__full_settings_path, 'w') as fp:
                json.dump(obj=self.__settings, fp=fp, indent=4)


    def __validate_attribute(self, attribute:str, web:bool):
        '''
        Validates that an attribute exists in either web or general settings.

        :param attribute: the intended attribute to check
        :param web: check web settings OR general.
        :raises InvalidAttributeException: When the specified attribute does not exist in settings.
        '''
        if (not web and (not attribute in self.__settings.keys() or attribute == constants.WEB_SETTINGS_ATTRIBUTE) or (web and not attribute in self.__settings.get(constants.WEB_SETTINGS_ATTRIBUTE).keys())):
            raise InvalidAttributeException('Attribute: "' + attribute + '" does not exist on settings!')


    def get_setting(self, attribute:str, web:bool = False):
        '''
        Get the value of a specific attribute from the settings

        :param attribute: the intended attribute to get
        :param web: get from web settings OR general
        '''
        self.__validate_attribute(attribute=attribute, web=web)
        
        try:
            if web:
                return self.__settings[constants.WEB_SETTINGS_ATTRIBUTE][attribute]
            else:
                return self.__settings[attribute]
        except InvalidAttributeException:   # The attribute doesn't exist
            print('Invalid attribute to get: "' + attribute + '"')  # TODO: Replace with logging!
            return
        
    
    def set_setting(self, attribute:str, value, web:bool=False):
        '''
        Set the value of a specific attribute from the settings

        :param attribute: the intended attribute to get
        :param value: the value to be set
        :param web: set an attribute from web settings OR general
        '''
        self.__validate_attribute(attribute=attribute, web=web)

        try:
            if web:
                self.__settings[constants.WEB_SETTINGS_ATTRIBUTE][attribute] = value
            else:
                self.__settings[attribute] = value
        except InvalidAttributeException:   # The attribute doesn't exist
            print('Invalid attribute to get: "' + attribute + '"')  # TODO: Replace with logging!
            return


    def refresh(self):
      '''
      Push the web settings onto the bus again. When the UI is refreshed, it expects a new settings event on the bus.
      '''
      self.push_to_queue(self.get_web_settings())




        