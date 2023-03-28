# PILOT Drive ✨v2.0✨

## What is PILOT Drive?
PILOT Drive is a fully open-source head unit/infotainment system built in Python 3.10 + Vue 3. It is intended to be ran on a Single Board Computer (SBC), such as the Raspberry Pi 4.

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
- Usage of common languages/frameworks. Python 3 is one of the most common & easy to learn languages, while the UI uses easy to read [Vue Single File Components](https://vuejs.org/guide/scaling-up/sfc.html).
- Modularity. The main features of PILOT Drive are contained as modular "services" that can be almost plug-and-play.
- A fully open source codebase. While some alternatives claim openness, most don't actually deliver after a certain threshold. PILOT Drive will always be open and free to use.

## Want to contribute?
- Found a bug or have an idea for an improvement? Raise a new [issue](https://github.com/lamemakes/pilot-drive/issues)!
- Want to contribute to the codebase? Create a fork and make a PR when you're all said and done!
- Contribution ideas/PILOT Drive roadmap:
    - Software Defined Radio integration
    - Migration from [dbus-python](https://dbus.freedesktop.org/doc/dbus-python/index.html) to [dasbus](https://dasbus.readthedocs.io/en/latest/) for more reliable and clean DBus interfacing
    - More in-depth bluetooth implementations, giving the user access to more information on the connected device
    - Intuitive and interactive vehicle interfacing. Currently this is only data guages, but the scope is vehicle diagnostics and other useful features.
    - Navigation & GPS integration. Potentially integrating OpenStreetMap for these capabilities.
    - More efficiencies & better resource management. 