# Driver-Drowsiness-Detection-System
This project is a real-time Driver Drowsiness Detection System developed using Python, OpenCV, Dlib, and optionally integrated with Arduino for alert mechanisms. It monitors eye blinks and behavior to detect whether a driver is sleeping, drowsy, or active, and can trigger physical alerts like a buzzer via Arduino. 
This project implements a real-time driver monitoring system that uses facial landmark detection to determine levels of drowsiness based on eye blinks, yawning patterns, and head position.

Two versions of the detection algorithm are provided:

🔹 old_Code.py
Detects eye blinks using Dlib’s facial landmark predictor.

Sends commands via serial (e.g., b'a' for "sleeping") to alert hardware systems such as a buzzer.

Classifies states into: Active, Drowsy, and Sleeping.

Runs continuous real-time analysis from a webcam.

🔹 new_Code.py
An improved version with:

Multithreaded camera capture for better performance.

Eye tracking position estimation and overlay on video.

Optional drawing of eye polygons for visualization.

Serial code commented for testing without hardware.

More modular with reusable functions and real-time status display.

🔹 Driver_Sleep_Detection_System_Arduino_Proteus.ino
Arduino sketch designed to interface with the Python system via serial.

Likely triggers actuators (e.g., buzzer or vibration motor) when drowsiness is detected.

🧠 Technologies Used
Python, OpenCV, Dlib, imutils

Serial Communication (PySerial/Arduino)

Webcam or USB camera

Proteus Simulation + Arduino

🚘 Use Case
This system can be integrated into vehicle dashboards to help reduce road accidents by monitoring drivers' eye activity and alerting them if signs of fatigue are detected.
