Developer Environment Setup
===========================

**This setup has only been tested on Linux (Fedora & Ubuntu)**

Windows & MacOS will likely have to hack together their own developer setup (and report back here!)


Install PILOT Drive & Friends
-----------------------------
#. Clone PILOT Drive:

    .. code-block:: sh

        git clone git@github.com:lamemakes/pilot-drive.git
        cd pilot-drive

#. Install `Python 3.11 <https://pilot-drive.rtfd.org/en/latest/tutorials/installation.html#installing-python-3-11>`_
#. Install `Node.js >= 16.16.0 & npm >= v8.11.0 <https://docs.npmjs.com/downloading-and-installing-node-js-and-npm>`_, `nvm <https://github.com/nvm-sh/nvm#installing-and-updating>`_ is highly recommended.
#. Install `yarn >= 1.22.19 <https://yarnpkg.com/>`_ via:

    .. code-block:: sh

        npm install --global yarn

#. Install the needed pip packages:

    .. code-block:: sh

        sudo python3.11 -m pip install backend/ pylint black pytest
        sudo python3.11 -m pip install ELM327-emulator  # emulates OBD functionality

#. Install the needed Node packages:


    .. code-block:: sh

        yarn --cwd ui/ install --frozen-lockfile

#. *(Optional)* Use `my fork of lukasjapan's bt-speaker <https://github.com/lamemakes/bt-speaker/blob/master/install.sh>`_ to install bt-speaker for bluetooth audio. **Raspberry Pi Only!**
#. *(Optional)* Install `ancs4linux <https://github.com/pzmarzly/ancs4linux#running>`_ for iOS notification integration
#. *(Optional)* Install `Android Debug Bridge (ADB) <https://developer.android.com/studio/command-line/adb>`_ and `Android Asset Packaging Tool 2 (AAPT2) <https://developer.android.com/tools/aapt2>`_ for Android notification integration


**NOTE: PILOT Drive needs to be installed as root, along with it's pip dependencies!**


Build PILOT Drive
-----------------

#. Enter the PILOT Drive directory:

    .. code-block:: sh

        cd pilot-drive/

#. The entire Python package can be built via the Makefile in the root directory:

    .. code-block:: sh
        
        make

#. Alternatively, the frontend OR package can be chosen for build:

    .. code-block:: sh

        make web        # Build ONLY the frontend
        make package    # Build ONLY the Python package

#. After a successful package build, install the package:

    .. code-block:: sh

        sudo python3.11 -m pip uninstall pilot-drive
        sudo python3.11 -m pip install ./dist/pilot_drive-X.X.X-py3-none-any.whl    # replace "X.X.X" with current version


Run it!
-----------

#. Start the backend:

    .. code-block:: sh
        
        sudo python3.11 backend/pilot_drive

#. Start the frontend (in a new terminal):

    .. code-block:: sh
        
        yarn --cwd ui/ dev

#. In your browser, navigate to the address indicated by the previous step - likely ``http://localhost:5173``

Ready to merge your changes?
----------------------------

#. First, make sure your changes are ready to be integrated and pass tests/linting:

    .. code-block:: sh

        cd pilot-drive
        python3.11 -m black backend/pilot_drive
        python3.11 -m pylint backend/pilot_drive
        sphinx-apidoc ./backend/pilot_drive -o ./docs/source/api/

#. Put up a `Pull Request <https://github.com/lamemakes/pilot-drive/pulls>`_ referencing the issue/feature being fixed


Thank you!
-----------

Your contributions to PILOT Drive are what makes it great. From reporting a small typo of a bug, to a major feature contibution - every ounce helps to create more of a free, privacy oriented, and open source alternative to the norm.