..Installation docs for PILOT Drive

Installation
====================


Quick Start
--------------------

Requirements
^^^^^^^^^^^^^^^^^^^^

- Raspberry Pi 4 or other Linux SBC
- Python > 3.10
- (Optional) `python-OBD <https://github.com/brendan-w/python-OBD>`_ To use OBD connectivity features
- (Optional) `ancs4linux <https://github.com/pzmarzly/ancs4linux>`_ For iOS notification integration
- (Optional) `ADB https://developer.android.com/studio/command-line/adb`_ For Android notification integration

Install
^^^^^^^^^^^^^^^^^^^^

To quick start your installation of PILOT Drive, first confirm the dependency requirements are met, then pull & install it from PyPi

.. code-block:: sh
   :caption: PILOT Drive Quick Install

   python3 -m pip install pilot-drive  # Install from PyPi
   pilot-drive                         # starts the service
   

Manual install
--------------------

Requirements
^^^^^^^^^^^^^^^^^^^^

- Raspberry Pi 4 or other Linux SBC
- Python > v3.10
- node > v16.16.0
- npm > v8.11.0
- yarn > v1.22.19
- (Optional) `python-OBD <https://github.com/brendan-w/python-OBD>`_ To use OBD connectivity features
- (Optional) `ancs4linux <https://github.com/pzmarzly/ancs4linux>`_ For iOS notification integration
- (Optional) `ADB https://developer.android.com/studio/command-line/adb`_ For Android notification integration

Install
^^^^^^^^^^^^^^^^^^^^
To manually build & install PILOT Drive:

.. code-block:: sh
   :caption: PILOT Drive Manual Install

   git clone https://github.com/lamemakes/pilot-drive.git   # Clone the repo
   cd pilot-drive/                                      
   make                                                     # Run the Makefile to build the frontend & backend
   cd dist/
   python3 -m pip install pilot-drive-<version>.whl         # Install the newly built wheel file
