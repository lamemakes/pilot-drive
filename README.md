# PILOT Drive ✨v(0.)2.0✨    
[![Documentation Status](https://readthedocs.org/projects/pilot-drive/badge/?version=latest)](https://pilot-drive.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pylint](https://github.com/lamemakes/pilot-drive/actions/workflows/pylint.yml/badge.svg)](https://github.com/lamemakes/pilot-drive/actions/workflows/pylint.yml)

## What is PILOT Drive?
PILOT Drive is a fully open-source head unit/infotainment system built in Python 3.11 + Vue 3. It is intended to be ran on a Single Board Computer (SBC), such as the Raspberry Pi 4.

## What can it do? 
Utilizing PILOT Drive, a user can:
- Play, display, and control audio from sources like bluetooth
- Display live data from their vehicle
- Show notifications from connected iOS & Android devices
- Control and display connected backup cameras
- Tailor the UI to their own tastes with fully customizable themes and display settings.
- Integrate with the [PILOT Drive HAT](https://github.com/lamemakes/pilot-drive-HAT) for a seamless in-vehicle experience.

## Consider yourself a hacker?
PILOT Drive is for you! Designed to be hackable, through means of:
- __Common languages/frameworks__: Python is one of the most common & easy to learn languages, while the UI uses easy to read Vue [Single File Components](https://vuejs.org/guide/scaling-up/sfc.html). Both of these make all current functionality easily tweakable.
- __Modularity__: The main features of PILOT Drive are contained as modular "services" that can be almost plug-and-play.
- __Fully open source codebase__: While some alternatives claim openness, most don't actually deliver after a certain threshold. PILOT Drive will always be open and free to use.

## Documentation
The _WIP_ documentation can be found [here](https://pilot-drive.readthedocs.io/en/latest/). 

## Want to contribute?
- Found a bug or have an idea for an improvement? Raise a new [issue](https://github.com/lamemakes/pilot-drive/issues)!
- Want to contribute to the codebase? Create a fork and make a PR when you're all said and done!
- Contribution ideas/PILOT Drive roadmap:
    - [ ]__Testing__: More unit testing & E2E testing could be used at any level of the stack!
    - [ ]__Documentation__: Current docs are very immature, and can better implement the the [tutorials, guides, explanations & references](https://www.writethedocs.org/conf/eu/2017/speakers/#speaker-daniele-procida) of docs.
    - [ ]__Media types__: More media integration! (ie. Software Defined Radio, local audio files, videos, and DOOM!)
    - [x]__Migration from [dbus-python](https://dbus.freedesktop.org/doc/dbus-python/index.html)__: to [dasbus](https://dasbus.readthedocs.io/en/latest/) for more reliable and clean DBus interfacing
    - [ ]__Bluetooth features__: More in-depth bluetooth implementations, giving the user access to more functionality to the connected device. (ie. Transferring of playing album cover via BIP, taking/making calls, sending texts, etc)
    - [ ]__UI enhancements__: More intuitive and interactive vehicle interfacing. Currently this is only data guages, but the scope is vehicle diagnostics and other useful features. Also more UI customizability would be a plus.
    - [ ]__Navigation__: GPS & OpenStreetMap integration.
    - [ ]__Optimizations__: More efficiencies & better resource management. (ie. multiprocessing processes cleanly exit)
    
## Notes
- __Version__: PILOT Drive _is_ version 0.2.0, but in my heart it's v2.0. This is because I jumped the gun on my previous iteration - labeling a totally unstable and unorganized PILOT Drive v1. This version is the definition of a second iteration, but [semver](https://github.com/semver/semver) says different because of how much it will still likely change and be refactored. 
