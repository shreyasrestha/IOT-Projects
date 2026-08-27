# Gesture Controlled Robot 🤖

A real-time **gesture-controlled robotic system** that allows users to control the robot's operation and speed using hand gestures. The project uses a **Raspberry Pi, camera, Python, and OpenCV** to recognize predefined hand gestures and convert them into commands for the robot.

## 🚀 Features

* Real-time hand gesture recognition
* Contactless control of the robot
* Four predefined gestures:

  *  **Stop** – Stops the robot
  *  **Start** – Starts the robot
  *  **Speed** – Increases the robot's speed
  *  **Slow** – Decreases the robot's speed
* Camera-based gesture detection
* Raspberry Pi-based hardware control
* Real-time processing using OpenCV

## 🛠️ Technologies Used

* **Python**
* **OpenCV**
* **Raspberry Pi**
* **GPIO**
* **Camera Module**
* **Motor Driver**
* **DC Motors**

## ⚙️ How It Works

1. The camera captures the user's hand gestures in real time.
2. **OpenCV** processes the captured frames and analyzes the hand configuration.
3. The detected gesture is classified as **Start, Stop, Speed, or Slow**.
4. The corresponding command is sent to the Raspberry Pi.
5. The Raspberry Pi controls the robot through GPIO signals and the motor driver.
6. The robot responds to the gesture in real time by starting, stopping, increasing speed, or decreasing speed.


## 🔮 Future Improvements

The current prototype successfully demonstrates real-time gesture-based robot control. It can be further improved by enhancing **gesture recognition accuracy, performance under different lighting conditions, response time, and the number of supported gestures**.

## 👩‍💻 Project Overview

This project combines **computer vision and embedded systems** to create a contactless method of controlling a robotic system. It demonstrates the integration of Python-based image processing with Raspberry Pi hardware and motor control.
