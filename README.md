# herd_tracking_system

The program presents a simplified simultation of the synthetic sheep movement. It also provides an anomaly detector such as outputs of the protected territory and death. 

It was developed in Python3.11.8 and its executable was prepared using PyInstaller for Linux and Windows, respectively. The Linux distibution in which the PyInstaller command was used was Debian 12.5. 

In case any of the executables cannot be opened on your machine, you can install the external libraries of the requirements.txt file and run the main.py script. 
The demo presentation was carried out in Windows, so that the greatest number of scenarios for this operating system has been explored.

# About the files
assets: Contains icons accessed from main.py during simulation.
LinuxExecutable: contains the linux executable in the dist folder, it is the file called main.
WindowsExecutable: this is the Windows executable, it is also in dist/main.
constants.py, matrix.py, tools.py, ui.py, uiParameters.py: define important methods and variables used in the simulation, both by the simulating program and by the GUI.
environment.py: Contains the definitions of the Sheep, Wolf and Hole classes.
readingData.py: contains the csv reading routines to generate the images at the end of the main program execution.
recover.csv: csv with example data to load a sheep position from the GUI.
requirements.txt: information about the python libraries used in the program.
Sheeps_Eng_V2.pdf, TechTalk_Slides.pdf: paper and program presentation, respectively.
The 2024-... folders: relevant examples of simulation results

# Important: 
Copy assets folder inside dist folder in WindowsExecutable or LinuxExecutable, without it, icons of sheeps could not be load

# About the program
The first screen is a graphical interface where the user can enter the number of sheep they want to simulate.

# PD:
Errors were found when running the program on Linux, especially due to the management of different windows for the simulation. It occasionally happens that after generating images, the program closes. It is a considerable limitation, as it prevents new simulations from being recreated, but each of these is carried out successfully and its graphs show the result of the simulation.
