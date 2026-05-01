# 🏠 Smart Room Activity Monitoring System using ESP32 & Machine Learning

## 📌 Overview
This project presents an IoT-based smart room monitoring system that detects and analyzes human activities using multiple sensors and machine learning.

The system uses an ESP32 microcontroller to collect real-time data such as motion, light intensity, temperature, humidity, and distance. This data is sent to Google Sheets and later used for activity classification using machine learning.

---

## 🎯 Features
- 📡 Real-time data collection using ESP32
- 🌡️ Temperature & humidity monitoring (DHT22)
- 💡 Light intensity detection (LDR)
- 🚶 Motion detection (PIR sensor)
- 📏 Distance measurement (Ultrasonic sensor)
- ☁️ Cloud data storage using Google Sheets
- 🤖 Machine Learning-based activity prediction
- 📊 Data visualization using graphs

---

## 🧠 System Workflow

Sensors → ESP32 → WiFi → Google Sheets → Dataset → Machine Learning → Activity Prediction

---

## 🔧 Hardware Components
- ESP32 Dev Board
- PIR Motion Sensor (HC-SR501)
- LDR (Light Dependent Resistor)
- DHT22 Temperature & Humidity Sensor
- Ultrasonic Sensor (HC-SR04)
- Breadboard
- Jumper Wires
- Power Supply (USB / Power Bank)

---

## 🔌 Sensor Connections

| Sensor | VCC | GND | Signal Pin | ESP32 GPIO |
|--------|-----|-----|------------|------------|
| PIR Sensor | 5V | GND | OUT | GPIO 13 |
| DHT22 | 5V | GND | DATA | GPIO 4 |
| LDR | 3.3V | GND | Analog | GPIO 34 |
| Ultrasonic TRIG | 5V | GND | TRIG | GPIO 5 |
| Ultrasonic ECHO | 5V | GND | ECHO | GPIO 18 |

---

## ⚙️ Software & Tools
- Arduino IDE (ESP32 programming)
- Google Sheets (data storage)
- Google Apps Script (API)
- Python (Machine Learning)
- Scikit-learn (Model training)
- Matplotlib (Visualization)

---

## 🚀 Setup Instructions

### 1️⃣ Hardware Setup
- Connect all sensors to ESP32 as per the table above
- Ensure proper power supply and grounding

---

### 2️⃣ ESP32 Code Setup
- Install Arduino IDE
- Install ESP32 board package
- Upload the code to ESP32
- Update WiFi credentials and Google Script URL

---
### 3️⃣ Google Sheets Setup
- Create a new Google Sheet
- Add columns:Time, Motion, Light, Temp, Humidity, Distance

---

### 4️⃣ Google Apps Script
- Open **Extensions → Apps Script**
- Paste this code:

javascript
function doGet(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  sheet.appendRow([
    new Date(),
    e.parameter.motion,
    e.parameter.light,
    e.parameter.temp,
    e.parameter.humidity,
    e.parameter.distance
  ]);

  return ContentService.createTextOutput("Success");
}

Deploy as Web App
Copy the generated URL

5️⃣ Data Collection
Power ESP32 using power bank
Data will automatically upload to Google Sheets
6️⃣ Machine Learning
Export dataset from Google Sheets
Train model using Python (Random Forest)
Predict activities:
Bed
Chair
Kitchen
Outside
📊 Results
Real-time sensor data collected successfully
Machine learning model achieved good accuracy (~75–90%)
Graphs generated for:
Temperature vs Time
Humidity vs Time
Light vs Time
Activity vs Hour
⚠️ Challenges Faced
Sensor noise and fluctuation
Delay in data transmission
Difficulty in collecting real-world data
Similar activity classification issues
✅ Conclusion

The system successfully demonstrates how IoT and machine learning can be combined to monitor and analyze human activity in a smart environment.

🔮 Future Scope
Improve accuracy using deep learning
Add mobile/web application
Include more sensors (camera, sound)
Real-time alerts system
📁 Project Structure
├── Arduino_Code/
├── Dataset/
├── ML_Model/
├── Graphs/
├── README.md
  
