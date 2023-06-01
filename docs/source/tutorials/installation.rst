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
      lzma lzma-dev tk-dev uuid-dev zlib1g-dev libdbus-glib-1-dev \
      libgirepository1.0-dev libcairo2-dev


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

To quick start your installation of PILOT Drive, you can pip via:

.. code-block:: sh

   sudo python3.11 -m pip install pilot-drive         # Install from PyPi
   sudo python3.11 -m pilot_drive                     # Start PILOT Drive


From here, you can navigate to ``http://localhost:8002`` in your browser to access the UI.

Manual install
----------------------
Requirements
^^^^^^^^^^^^^^^^^^^^

- python >= v3.11
- node   >= v16.16.0
- npm    >= v8.11.0
- yarn   >= v1.22.19
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
   sudo python3.11 -m pip install pilot-drive-<ver>.whl     # Install the newly built wheel file


*(Optional)* Install python-OBD:

.. code-block:: sh

   sudo python3.11 -m pip install \
      git+https://github.com/brendan-w/python-OBD#egg=obd