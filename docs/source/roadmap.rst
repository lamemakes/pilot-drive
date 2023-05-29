Roadmap
====================

"Big picture" features
----------------------

| ☐ More media integration!
|    ☐ Software Defined Radio
|    ☐ Local audio files
|    ☐ Videos
|    ☐ Run DOOM!
| ☐ Navigation implementations
|    ☐ Utilize external GPS module
|    ☐ Implement OpenStreetMap, allow for offline navigation.
| ☐ More Bluetooth features
|    ☐ Pull bluetooth audio album cover from connected device (via BIP)
|    ☐ Take calls
|    ☐ Send texts
|    ☐ Display other potentially useful connvected device info (cell service, battery, etc)
|    ☐ Allow for enabling/pairing/discovery within the UI
| ☐ Extended CAN bus functionality
|    ☐ More vehicle disagnostic options (ie. reset monitors/clear codes, warn about troubling stats like DTCs)
|    ☐ Customizable dial display
|    ☐ Calculate stats on data (ie. MPG, fuel injector efficencies)
| ☐ Documentation refinement
|    ☐ Implement more documentation that follows the `Diátaxis framework <https://diataxis.fr/>`_, such as better tutorials and how-to's
| ☐ Support Android Debug Bridge (ADB) over Wi-Fi rather than purely USB
| ☐ Potentially remove StrEnums to allow for Python 3.10 compatibility?

Frontend/UI
----------------------

| ☐ Implement a color picker to allow for custom theme creation in settings
| ☐ Add widgets/drag and drop UI components (needs to be saveable)
| ☐ More intuitive and quick-access menus (drag down, small buttons in info bar, etc)
| ☑ Refactor Vue SFC to organize components based on feature/function
| ☐ Initial implementation of `vitest <https://vitest.dev/>`_ unit tests
| ☐ Better "quick glance" info in top bar (connected bluetooth/usb devices, wifi connectivity, etc)
| ☐ Support for dark/tinted mode. Allowing setting for automatic detection (using PILOT Drive HAT headlight detection), and manual enabling.
| ☐ Better state management/stores, implementing Vuex
| ☐ Documentation & API reference. So far only the backend has gotten documentation love
| ☐ "snackbar" notifications, small windows that pop up with informational messages/prompts

Backend
----------------------

| ☐ Refactor Bluetooth Service to allow for less complexity betweet ANCS & Bluetooth Media
| ☑ Initial implementation of Pytest unit tests, along with github actions implementation
| ☐ Full implementation of typing via mypy, along with github actions implementation
| ☑ Implement dasbus to replace the depreciated python-dbus
| ☐ Optimization of multiprocessing Processes. Currently processes are not neccesarily exiting properly or cleaning up when done.
| ☑ Remote updates. When connected to wifi, PILOT Drive should be able to self-update. This was previously supported in earlier PILOT versions, but not reliably.

| **Have a specific feature/improvement in mind that you don't see here? Not sure how to get started on an existing roadmap item?**
|
| **Start a new** `discussion <https://github.com/lamemakes/pilot-drive/discussions/new?category=ideas>`_ **outlining (in detail) your idea!**
