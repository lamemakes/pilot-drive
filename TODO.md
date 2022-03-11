# Master TODO:

## General
+ Comment everything!!
+ Renaming of util files
+ Modularity - new features should be SOMEWHAT plug 'n play
+ Follow more standardization (PEP)
+ Organize into packages/sub-packages/general folders
+ Better logging
+ More getters/setters?
+ Add ADB Functionality
+ General file renaming (everything doesn't need a pilot prefix)
+ Figure out how to point to template & static folders in flask in web folder
+ Add Camera functionality
+ More debugging & TESTING
+ Package to conventional standards

## main.py
+ Add module to setup config, sloppy right now
+ Add clean JSON returns, not formatted strings
+ Pull from utils packageModule to setup config

## utils/pilot_bt_ctl.py
+ How does GLib work? Why loop?
+ Clean it up! Too convoluted, unneccesary code?
+ Comment more!

## utils/pilot_track.py
+ Should this be a part of the bt_ctl file?
+ Get rid of unneccesary variables (ie. `path`)
+ COMMENT

## utils/pilot_time.py
+ Is this neccesary? One function for a file?

## utils/pilot_sys_info.py
+ Add more than CPU useage

## utils/pilot_logger.py
+ Improve logging
+ Use logging throughout the program

## utils/pilot_car_info.py
+ Add verification to if port exists/if connection can be made
+ General functionality is not there, need to work on OBDII connection to car
+ Update so fuel is not a static test value, having emulation issues.
+ Seems convoluted

## utils/\<ADB program>.py
+ Create file
+ Get notifications from ADB
+ Pull icons
+ Send SMS?
+ Display text from notifications if any
+ Have UI-wide notifications for specific notifications, others only in the tab (prioritize notifs)
+ Phone info (Battery, cell service, etc...)

## web/templates/home.html
+ Better comments
+ Less divs!

## web/static/css/pilot_style.css
+ Add comments
+ This should be the main css file, no others
+ Organize/section based on what is being styled
+ Unnecesary elements?
+ Link font?

## web/static/css/carInfo.css
+ Remove

## web/static/js/pilot_script.js
+ Clean up / Organize
+ Comment
+ Handle JSON, no more string splitting
+ More functions


## web/static/js/carInfo.js
+ Remove

# When Done:
+ https://packaging.python.org/en/latest/tutorials/packaging-projects/



