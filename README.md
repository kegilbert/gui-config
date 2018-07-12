# Mbed OS GUI Config

First fast pass at a GUI configuration menu for Mbed OS.

Unchecking the top level module markers will add that module to the `.mbedignore` file, removing it from compilation. The settings below are for manual configuraiton of the OS.

## Use

Run the script from the root directory of an Mbed OS clone to load the mbed_lib.json files from:

1. Platform
2. Drivers
3. Events
4. RTOS

Select save to update the .mbedignore and mbed_app.json file with your settings.

## Notes

You may need to run `sudo apt-get install python3-tk` in some environments (Linux distrubutions in particular it seems like) for Python3 support.
