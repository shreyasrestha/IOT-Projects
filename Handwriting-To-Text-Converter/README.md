# 📝 Handwriting to Text Converter using Raspberry Pi and Tesseract OCR

## 📌 Project Overview
This project is a Raspberry Pi-based Handwriting to Text Converter that captures handwritten text using a Raspberry Pi Camera, preprocesses the captured image using OpenCV, and extracts the text using Tesseract OCR. The recognized text is displayed on the terminal as well as on a 16x2 I2C LCD display.

## ✨ Features

- Capture handwritten text using Raspberry Pi Camera
- Image preprocessing using OpenCV
- Handwritten text recognition using Tesseract OCR
- Display extracted text on the terminal
- Display recognized text on a 16x2 I2C LCD
- Real-time image capture and processing

## 🛠 Hardware Used

- Raspberry Pi 4 Model B
- Raspberry Pi Camera Module
- 16x2 I2C LCD Display
- SD Card
- Power Supply


## 💻 Software Used

- Python 3
- Raspberry Pi OS
- OpenCV
- Tesseract OCR
- PyTesseract
- NumPy
- Picamera2


## ⚙️ Working

1. The Raspberry Pi Camera captures the handwritten image.
2. The image is converted to grayscale and preprocessed using OpenCV.
3. Tesseract OCR extracts the handwritten text.
4. The recognized text is displayed in the terminal and on the LCD.

