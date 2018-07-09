# Drone-Log-Formatter
Experimental Python based Drone Log Analyser which does the following functions,

1. Analyzes Pixhawk/APM autopilot logs and calculates flight data like endurance, wind speed, max. current and other parameters.
2. Generate Google Earth compatible KML file to get a bird's eye view of all the camera triggers.
3. Geotag photos with the correct gps coordinates

## Todo

1. Pre-flight checklist (D-Day, All Systems Go)
2. In-Flight checklist
3. Dropbox Integration
4. Sqlite local storage
5. Lots more to do ....

## Python Library Dependencies

1. simplekml - Generate KML files for Google Earth using a simple API
2. piexif - Read/Write Exif tags
3. dateutil - Timezone conversions
4. pyqt5 - Python bindings for Qt GUI Library

## Usage

```bash
$ python droneloganalyser.py
```

## Building resource file

Whenever a new image asset is added locally, the resource file needs to be updated and rebuilt. This ensures that the newly added image asset
is available in the distributed executable. Here are the steps to rebuild the resource file,

```bash
$ pyrcc5 -o images.py images.qrc
```

## Building windows executable

Windows executables are being generated using Pyinstaller. Open windows command prompt and enter into the project root directory. Then execute,

```bash
$ pyinstaller -w -F dronecubatormissioncontrol.py
```

The 'w' argument is to ensure that the application is opened in a windowed mode and does not show any consoles. The 'F' argument is to output
a single .exe file instead of a host of files that need to then be installed on all machines using a installer.


