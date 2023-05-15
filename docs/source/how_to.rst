How do I...
====================

Add new themes
----------------------

This how-to assumes PILOT Drive has been installed, and a settings file was created.

#. In your favorite text editor, open the ``settings.json`` (default path is ``/etc/pilot-drive/config/settings.json``)
#. Once in the settings file, navigate to the ``webSettings`` → ``themes`` section
#. Add the desired theme in the `below format`_, adding a name for the theme along with a primary, secondary, and accent color in an integer RGB format. `color-hex <https://www.color-hex.com/color-palettes/>`_ has some cool user made palettes.
#. Save ``settings.json`` and restart PILOT Drive
#. Once restarted, in the UI navigate to the settings tab and your new theme should be there!

.. _below format:
.. code-block:: json
    :caption: Theme format

    {
        "name": "<name>",
        "accent": [
            <Red Int>,
            <Green Int>,
            <Blue Int>
        ],
        "primary": [
            <Red Int>,
            <Green Int>,
            <Blue Int>
        ],
        "secondary": [
            <Red Int>,
            <Green Int>,
            <Blue Int>
        ]
    }
