Who, What & Why...
====================

Explanatory material for PILOT Drive

Why does PILOT Drive have "services"?
-------------------------------------

Different services within PILOT Drive are used serve a functionality/tasks within the application.
Services are frequently relaying real time data to the UI and for that reason need to be ran
asynchronously. This is currently done via the use of
`multiprocessing Processes <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process>`_ 
but this may be changed moving forward. All of a service's events that need to be conveyed to 
the UI are pushed via a "Master Event Queue", which is a multiprocessing queue that is available to 
all processes, as it is provided at service creation (This same Queue concept is used for logging). 
It's important to note that not *all* services utilize the service they're provided, like the settings
service. This returns shortly after sending the settings to the frontend.

Services also can provide optional callbacks for when the UI sends data. For example, the UI sends
the command to pause the current song, in which the media service's callback is passed the command.

For better visualization of the flow of PILOT Drive, see `the basic data flow diagram`_

Examples of services are:
 - **Vehicle**: Provides live OBD data on the connected vehicle
 - **Phone**: Displays phone notifications and information in real time
 - **Media**: Manages the A/V of the head unit


What type of host should I run PILOT Drive on?
----------------------------------------------

The original vision for PILOT Drive back in 2018 was to be fully ran and built around the Raspberry 
Pi, so much of this functionality is catered toward usage on the Pi. Though, the long term goal is 
to extend compatibility for a wide array of Single Board Computers and other linux-based machines.
As it stands, PILOT Drive can run (and has been tested) on Debian (Ubuntu, Raspberry Pi OS), and 
Fedora.

The UI is also currently built with the assumption that the user will be using a touchscreen.

So, the TDLR here is **PILOT Drive can run on any host that runs Debian/Fedora, has a (touch) display, 
Python 3.11 and a reasonable amount of memory**.


.. _the basic data flow diagram:

What does an overview of PILOT Drive look like?
-----------------------------------------------

.. figure:: diagrams/PILOT_Drive_Overview.drawio.svg
    :scale: 75%
    :alt: A diagram showing the basic data flow of PILOT Drive
