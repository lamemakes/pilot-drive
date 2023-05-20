<p align="center">
  <img src="docs/source/images/pilot_icon.png" alt="PILOT Drive logo" height="120px" width="120px"/>
</p> 
<p align="center">
  <a href="https://pilot-drive.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/pilot-drive/badge/?version=latest" alt="docs status" />
  </a>&nbsp;
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="code style black" />
  </a>&nbsp;
  <a href="https://github.com/lamemakes/pilot-drive/actions/workflows/ci.yml">
    <img src="https://github.com/lamemakes/pilot-drive/actions/workflows/ci.yml/badge.svg" alt="Pilot Drive CI" />
  </a>
</p>

## What is PILOT Drive?

PILOT Drive is a fully open-source head unit/infotainment system built in Python 3.11 + Vue 3. It is intended to be ran on a Single Board Computer (SBC), such as the Raspberry Pi 4.


## Why PILOT Drive?

### Consider yourself a hacker?

PILOT Drive is for you! Designed to be hackable, through means of:
- **Common languages/frameworks**: Python is one of the most common & easy to learn languages, while the UI uses easy to read Vue [Single File Components](https://vuejs.org/guide/scaling-up/sfc.html). Both of these make all current functionality easily tweakable.
- **Modularity**: The main features of PILOT Drive are contained as modular "services" that can be almost plug-and-play.
- **Fully open source codebase**: While some alternatives claim openness, most don't actually deliver after a certain threshold. PILOT Drive will always be open and free to use.

### Privacy! 

"Big Data" has specifically been working to target the automotive industry lately. This is _gross_ to say the least
- In a stock Android Auto/Apple CarPlay headunit, a plethora of data is collected and sold such as:
    - Personal identifiers
    - Biometrics
    - Location data and driving habits
    - Data synced from a connected device
- PILOT Drive will never collect or sell any of your information, and will always be open source to ensure this.

### Features

Utilizing PILOT Drive, a user can:
- Play, display, and control audio from sources like bluetooth
- Display live data from their vehicle
- Show notifications from connected iOS & Android devices
- Control and display connected backup cameras
- Tailor the UI to their own tastes with fully customizable themes and display settings.
- Integrate with the [PILOT Drive HAT](https://github.com/lamemakes/pilot-drive-HAT) for a seamless in-vehicle experience.


## Documentation

The _WIP_ documentation can be found [here](https://pilot-drive.readthedocs.io/en/latest/). 


## Want to contribute?

The project can always use an assist! You can contribute via...
1. **Bug reports/feature suggestions**: Let your voice be heard! Help refine the project by finding bugs and giving your ideas on where the project should go.
2. **Sponsor the project**: Use PILOT Drive? Want to provide the project with more resources? Sponsor the project to ensure it can continue to be developed. Any and all amounts help!
3. **Contribute code**: Put your name on PILOT Drive and get your beautiful code merged into the codebase! For ideas on what to work on, check out the [issues](https://github.com/lamemakes/pilot-drive/issues) or [roadmap](https://pilot-drive.readthedocs.io/en/latest/roadmap.html)!

**_For more info on contributing, see the [contribution guidelines](https://github.com/lamemakes/pilot-drive/blob/master/.github/CONTRIBUTING.md)_**


## Notes
- __Version__: PILOT Drive _is_ version 0.2.0, but in my heart it's v2.0. This is because I jumped the gun on my previous iteration - labeling a totally unstable and unorganized PILOT Drive v1. This version is the definition of a second iteration, but [semver](https://github.com/semver/semver) says different because of how much it will still likely change and be refactored.
- __Stability__: It's likely there's quite a few bugs within this release of PILOT Drive. A lot will change as features are added and existing ones are refined. Please have patience with all of this, and if there is something you want fixed or added, feel free to take a stab at adding it!
- __Legal Disclaimer__: Be aware of your local laws regarding in-vehicle entertainment/infotainment. Be safe! lamemakes and any other PILOT Drive contributors are **not** responsible for any unsafe driving due to the headunit.
