..Installation docs for PILOT Drive

Installation
====================

Installing Python 3.11 On Debian
--------------------

Due to the latest Python features being implemented, Python 3.11 is required. See the following guide to install it on Debian:

.. code-block:: sh
   :caption:

   wget https://www.python.org/ftp/python/3.11.2/Python-3.11.2.tgz
   sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev git
   tar -xzvf Python-3.11.2.tgz
   cd Python-3.11.2/
   ./configure --enable-optimizations
   sudo make altinstall


Quick Start
--------------------

Requirements
^^^^^^^^^^^^^^^^^^^^

- Raspberry Pi 4 or other Linux SBC
- Python > 3.11
- (Optional) `python-OBD <https://github.com/brendan-w/python-OBD>`_ To use OBD connectivity features
- (Optional) `ancs4linux <https://github.com/pzmarzly/ancs4linux>`_ For iOS notification integration
- (Optional) `ADB https://developer.android.com/studio/command-line/adb`_ For Android notification integration

Install
^^^^^^^^^^^^^^^^^^^^

To quick start your installation of PILOT Drive, first confirm the dependency requirements are met, then pull & install it from PyPi

.. code-block:: sh
   :caption:

   python3 -m pip install pilot-drive  # Install from PyPi
   pilot-drive                         # starts the service
   

Manual install
--------------------

Requirements
^^^^^^^^^^^^^^^^^^^^

- Raspberry Pi 4 or other Linux SBC
- Python > v3.11
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
   :caption:

   git clone https://github.com/lamemakes/pilot-drive.git   # Clone the repo
   cd pilot-drive/                                      
   make                                                     # Run the Makefile to build the frontend & backend
   cd dist/
   python3 -m pip install pilot-drive-<version>.whl         # Install the newly built wheel file
