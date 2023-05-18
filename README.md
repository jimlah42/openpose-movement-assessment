# openpose-movement-assessment


## Installation


OpenPose installation

Follow installation guide on OpenPose github page
Make sure you follow the additional steps for the Python API
Unfortunately these instructions can be quite confusing and it can be very hard to troubleshoot errors. 

https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md#compiling-and-running-openpose-from-source



Follow the steps here:
https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/03_python_api.md

Firstly test that the examples work which means everything is setup properly.
Then move the required folders into the “openpose” directory of the app (instructions under the “Export OpenPose” heading

Install all required dependencies using
Pip install requirements.txt
If you are planning to develop the app it is recommended that you set up a virtual python environment
To start program use python MainWindow.py

## Development guide
This guide is designed to give you a quick overview of how the program is structured and how to go about developing it. For more technical usage all widgets and functions are documented and typed. 

Formating
I have tried to follow the PEP 8 python style and naming conventions for this project. To upkeep code readability please try to follow this style.

https://peps.python.org/pep-0008/

Also all functions have used type hints and docstrings to help with usage so any new development should also include this


## Basic Program Overview

1. Raw videos are processed in `openpose/process_video.py` (OpenPose parameters can be configured in `openpose/opParams.json` see https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/include/openpose/flags.hpp for parameters)
2. This will create a JSON and video ouput with OpenPose keypoint data in the `output/{video_file_name}` directory
3. Then user can create measurements on the measurement window and these are processed in `measurements/calculate_measurements.py`
4. This will append the keypoints JSON file to include the calculated measurements
5. If the user opts to draw the measurements this is processed in `draw/draw_tools.py`
6. This will create a new output video (`output_with_measurements.avi`) with the measurements draw onto it
7. Users can then also either plot or create csv output using `data/data_tools.py` with `generate_plot()` and `generate_csv()`


## User Interface

The user interface is built using the PyQt5 framework. I recommend becoming familiar with this framework before working on the app.

This article is a good starting point:
https://www.pythonguis.com/tutorials/creating-your-first-pyqt-window/


The user interface stems from the MainWindow widow widget which is the parent of all the major pages inside each tab.
Each major page contains widgets and for more complex components is broken into custom widgets to reduce complexity of each file and allow widgets to be reused

The current pages are:
1. `ProcessWindow`
2. `MeasurementsWindow`
3. `ViewWindow`
4. `AnalyseWindow`

Each custom widget follows the following structure

#Widgets\
widget definition\
widget configuration\
widget connections\
\
widget definition\
widget configuration\
widget connections\
…\
\
#Layout\
layout \
…\
\
#Connections\
connection functions\

Custom widgets are organised inside the “widgets” directory. If a widget is only used on one page it goes inside that page's corresponding folder (e.g. `widgets/process` for the process page). If a custom widget is used across multiple pages it is put inside the widgets/general folder.



## Measurements

A major part of this platform is to allow for the easy development of new measurements

Measurement types are made to import the Measurement class inside ./measurements/Measurement.py

This class is designed to represent an instance of a measurement type created by the user.
Abstracting the class like this allows the program to simply loop through `Measurements` in and ask the object to perform the task how it is supposed to, removing the need for excess logic required to check measurement types everytime they are required to perform a task.

Each new measurement class has 4 main functions that it needs to perform:

1. `calculate()` - Calculate measurement value from keypoints\
This function takes the keypoint data for a given frame and returns the calculated value
2. `draw()` - Draw visual representation of measurement on video\
This function takes a video frame and draws a visual representation of the measurement onto it\
3. `get_info_readable()` - Give a human readable description of the measurement\
This function uses the values of the measurement to give a human readable description of the measurement
4. `params()` - Return parameters to be written to JSON to allow it to be rebuilt\
This function returns all the parameters of the measurement

For a simple example see DistanceMeasurement.py

Once you have created a new measurement type you will need to create a parameters widget for the UI. 
This is a form widget that collects the required parameters to build the measurement object
You can use the PointComboBox custom widget to create a Labelled drop down menu that contains all of the Openpose keypoints.

This widget then needs to be added to the AddMeasurementForm widget and set to disabled.
Then in the type_changed function set up a new else if statement to enable it when the corresponding type is selected.


