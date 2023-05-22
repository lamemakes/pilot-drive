.. PILOT Drive documentation master file, created by
   sphinx-quickstart on Tue Mar 28 12:11:54 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PILOT Drive's documentation
=======================================

Welcome to PILOT Drive!

PILOT Drive is an open source vehicle radio/headunit/infotainment system. 
The aim is to create an in-vehicle system that can display media, car, and phone info, all while allowing for easy hackability & tweaking. 
Most of the headunits around currently are either OEM/proprietary or claim to be open, but are only open to a certain threshold.

What can it do?
----------------------
In it's current implementation, PILOT Drive can:

- Play, display, and control audio from sources like bluetooth
- Display live data from their vehicle
- Show notifications from connected iOS & Android devices
- Control and display connected backup cameras
- Tailor the UI to their own tastes with fully customizable themes and display settings.
- Integrate with the PILOT Drive HAT for a seamless in-vehicle experience.

Designed to be hacked
----------------------
PILOT Drive was built with tweaking and hacking in mind, via:

- **Common languages/frameworks**: Python is one of the most common & easy to learn languages, while the UI uses easy to read Vue Single File Components. Both of these make all current functionality easily tweakable.
- **Modularity**: The main features of PILOT Drive are contained as modular "services" that can be almost plug-and-play.
- **Fully open source codebase**: While some alternatives claim openness, most don't actually deliver after a certain threshold. PILOT Drive will always be open and free to use.


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   tutorials/index
   how-to/index
   explanatory
   API Reference <api/pilot_drive>
   Roadmap/Contribution Ideas <roadmap>