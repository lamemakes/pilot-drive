'''
Settings Exceptions
'''


class InvalidAttributeException(Exception):
    '''
    Exception raised when an invalid attribute is used in the set_setting or get_setting methods
    '''

    pass


class FailedToReadSettingsException(Exception):
    '''
    Exception raised when the settings could not be read
    '''

    pass


'''
Camera Exceptions
'''

class FailedToInstatiateCamera(Exception):
    '''
    Exception raised when the camera service failed
    '''