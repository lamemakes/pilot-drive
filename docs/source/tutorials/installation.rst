Installation
====================

Installing Python 3.11
----------------------
Due to the latest Python features being implemented in PILOT Drive, Python 3.11 is required. 

Install dependencies for... 

**Debian**:

.. code-block:: sh

   sudo apt-get -y install build-essential gdb lcov pkg-config \
      libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
      libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
      lzma lzma-dev tk-dev uuid-dev zlib1g-dev


**Fedora/CentOS**

.. code-block:: sh

   sudo yum install yum-utils
   sudo yum-builddep python3


**Build and Install Python 3.11**

.. code-block:: sh

   wget https://www.python.org/ftp/python/3.11.2/Python-3.11.2.tgz
   tar -xzvf Python-3.11.2.tgz
   cd Python-3.11.2/
   ./configure --enable-optimizations
   sudo make altinstall


Quick Start
----------------------
Install
^^^^^^^^^^^^^^^^^^^^

To quick start your installation of PILOT Drive, you can use the included installer, via:

.. code-block:: sh

   python3 -m pip install pilot-drive  # Install from PyPi
   python3 -m pilot_drive --setup      # Run PILOT Drive installer
   

This will lead you through all the configuration steps to ensure PILOT Drive is configured quickly and properly based on the machine it's running on.

Manual install
----------------------
Requirements
^^^^^^^^^^^^^^^^^^^^

- python >= v3.11
- node   >= v16.16.0
- npm    >= v8.11.0
- yarn   >= v1.22.19
- (Optional) `lukasjapan's bt-speaker <https://github.com/lukasjapan/bt-speaker>`_ -> For bluetooth audio
- (Optional) `python-OBD <https://github.com/brendan-w/python-OBD>`_               -> To use OBD connectivity features
- (Optional) `ancs4linux <https://github.com/pzmarzly/ancs4linux>`_                -> For iOS notification integration
- (Optional) `ADB <https://developer.android.com/studio/command-line/adb>`_        -> For Android notification integration

Install
^^^^^^^^^^^^^^^^^^^^
To manually build & install PILOT Drive:

.. code-block:: sh

   git clone https://github.com/lamemakes/pilot-drive.git   # Clone the repo
   cd pilot-drive/                                      
   make                                                     # Run the Makefile to build the frontend & backend
   cd dist/
   python3 -m pip install pilot-drive-<version>.whl         # Install the newly built wheel file
