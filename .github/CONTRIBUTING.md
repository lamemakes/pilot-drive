# Contributing to PILOT Drive

## How to contribute

There are three primary mediums for contributions to PILOT Drive.

1. Suggestions & bug reports.
    - Have a feature in mind you'd like to see? Found a problem with the latest package cut? Pop over to the [issues](https://github.com/signalapp/Signal-Desktop/issues) tab and follow the template based on your request.
1. Donations!
    - Are you enjoying PILOT Drive? Want to see it really blosom into something beautiful? You can donate via [Github Sponsors](https://github.com/sponsors/lamemakes) to ensure that I can continue to dedicate time and resources to this entirely free and open source project. 
1. Code contributions!
    - Enjoy Python/TypeScript? Hop in! You can pickup a new bug/feature, work on a [roadmap](https://pilot-drive.readthedocs.io/en/latest/roadmap.html) goal, or (after raising a feature proposal in issues) develop your own feature!


## Setting up your environment

So far, PILOT Drive has only been tested and developed on Linux (Raspberry Pi OS, Ubuntu, and Fedora) so these instructions are strictly for Linux users. (But a good contribution idea is to provide some cross platform abilities to Windows/MacOS users!)

### Clone PILOT Drive
- `git clone git@github.com:lamemakes/pilot-drive.git` (or your own fork of the repo)

### Install PILOT Drive & required dependencies
1. Install Python v3.11+
1. Install Node.js v16.16.0, or use nvm
1. Install npm v8.11.0
1. Install yarn v1.22.19
1. Install the needed pip packages
    - `sudo python3 -m pip install pilot-drive/backend/`
    - `sudo python3 -m pip install black pylint`
1. _(Optional)_ Use [my fork of lukasjapan's bt-speaker](https://github.com/lamemakes/bt-speaker/blob/master/install.sh) to install bt-speaker for bluetooth audio. **Raspberry Pi Only!**
1. _(Optional)_ Install [ancs4linux](https://github.com/pzmarzly/ancs4linux#running) for iOS notification integration
1. _(Optional)_ Install [Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb) and [Android Asset Packaging Tool 2 (AAPT2)](https://developer.android.com/tools/aapt2) for Android notification integration

**NOTE: PILOT Drive needs to be installed as root, along with it's pip dependencies!**

### Build PILOT Drive
1. Enter the PILOT Drive directory
    - `cd pilot-drive/`
1. The entire Python package can be built via the Makefile in the root directory
    - `make`
1. Alternatively, the frontend OR package can be chosen for build
    - `make web`
    - `make package`
1. After a successful package build, install the package
    - `sudo python -m pip uninstall pilot-drive`
    - `sudo python -m pip install ./dist/pilot_drive-X.X.X-py3-none-any.whl` (replace "X.X.X" with PILOT Drive version)
1. Confirm the install was successful
    - `sudo pilot-drive`

## Ready to merge your changes?
1. First, make sure your changes are ready to be integrated and pass tests/linting.
    - `cd pilot-drive                                           # enter the repo yet again`
    - `python3 -m black backend/pilot_drive                     # format the backend with black`
    - `python3 -m pylint backend/pilot_drive                    # confirm code passes pylint`
    - `sphinx-apidoc ./backend/pilot_drive -o ./docs/source/    # generate api docs` 
2. Put up a Pull Request referencing the issue/feature being fixed

## Thank you!

Your contributions to PILOT Drive are what makes it great. From reporting a small typo of a bug, to a major feature contibution - every ounce helps to create more of a privacy oriented, open source alternative to the norm.


