# herd_tracking_system

Thep rogram presents a simplified simultation of the synthetic sheep movement. It also provides an anomaly detector such as outputs of the protected territory and death. 

It was developed in Python3.11.8 and its executable was prepared using PyInstaller for Linux and Windows, respectively. The Linux distibution in which the PyInstaller command was used was Debian 12.5. 

In case any of the executables cannot be opened on your machine, you can install the external libraries of the requirements.txt file and run the main.py script.

# About the program
The first screen is a graphical interface where the user can enter the number of sheep they want to simulate.
Once the start button is pressed, a new window is displayed in which a graphic simplification of the scenario of a flock of sheep seen from above is observed. The sheep are represented with white triangles. The light green land is the protected area or area over which the farmer has control. The dark green area is the area that should not be accessed by sheep.
Every 5 seconds in the terminal that opens along with the program, sheep that are outside the protected area or those that have been immobile for a long time, or have been determined to be dead, are printed.

Pressing the U key opens a small GUI to resize the sheep, make their number labels visible or disappear, and cause deaths. These will be, after a certain time, detected by the program, in the same way as the exits from the protected area.

By closing the simulation window, a new numerical input can be entered to start another simulation. Additionally, a csv file will have been created with records of the sheep's positions every 5 seconds during the simulation.
