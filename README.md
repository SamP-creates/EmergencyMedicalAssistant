# **🏆 WRO 2025 Future Innovators: 6th Place International Champions**
**Project Name:** *E.M.A: Emergency Medical Assistant*
**Team Name:** *RoboCare Innovations*
**Event:** *World Robot Olympiad (WRO) 2025 – Future Innovators Category*
**Location:** *Ljubljana, Slovenia*
**Rank:** *6th Place (Top 10 Global Finalists)*
**Year:** *2024-2025*

---

## **🌍 About WRO Future Innovators**
The **World Robot Olympiad (WRO)** is an international robotics competition that challenges young minds to develop creative solutions to real-world problems. The **Future Innovators** category is designed for teams of **1–3 members** to design, build, and program **autonomous robots** that address global challenges.

### **🎯 WRO 2024–2025 Season Theme: *The Future of Robots***
The theme for the 2024–2025 season was **"The Future of Robots"** Teams were encouraged to create robots that contribute to society through **one or more of the 17 UN SDGs**, such as:
- **SDG 3:** Good Health and Well-Being *(Our project aligns with this goal by improving emergency room efficiency and patient care.)*
- **SDG 9:** Industry, Innovation, and Infrastructure
- **SDG 10:** Reduced Inequalities

**E.M.A (Emergency Medical Assistant)** directly supports **SDG 3** by **reducing wait times, improving documentation accuracy, and enabling nurses to focus primarily on patient care rather than paperwork**.

---

## **📌 Table of Contents**
| **Section**                     | **Description**                                                                 |
|----------------------------------|---------------------------------------------------------------------------------|
| [📜 Project Overview](#-project-overview) | Introduction, objectives, and problem statement.                                |
| [🎯 Problem Statement](#-problem-statement) | The challenge we addressed and its real-world impact.                           |
| [🛠️ Technical Specifications](#-technical-specifications) | Hardware, software, AI models, and security features.                           |
| [📂 Folder Structure](#-folder-structure) | Detailed breakdown of all project folders and their contents.                   |
| [🚀 How E.M.A Works](#-how-ema-works) | Step-by-step explanation of the robot’s functionality.                          |

---

## **📜 Project Overview**
### **🏥 The Challenge**
Emergency rooms (ERs) worldwide face **critical inefficiencies**:
- **Nurses spend ~30% of their time** on **documentation** instead of patient care.
- **Long wait times** lead to **delayed treatments** and **reduced patient satisfaction**.
- **Manual data collection** increases the risk of **errors and miscommunication**.
- **Patients with disabilities** often face **difficulty** in accessing triage services.

### **💡 Our Solution: E.M.A (Emergency Medical Assistant)**
We designed **E.M.A**, an **autonomous robot** that:
1. **Collects patient data** in the triage area, reducing paperwork for nurses.
2. **Adjusts its height** to accommodate patients of all ages and mobility levels.
3. **Performs urine tests** using **test strips** to detect early signs of health issues (e.g., UTIs, diabetes, kidney problems).
4. **Uses AI-powered facial recognition** (via **CompreFace**) to **securely verify patient identity** and store data.
5. **Organizes patient records** in **secure, searchable folders** for doctors to access instantly.

### **🎯 Objectives**
✅ **Reduce wait times** by **automating data collection**.
✅ **Free up nurses** to focus on **patient care**.
✅ **Improve accuracy** in triage documentation.
✅ **Enhance accessibility** for all patients.
✅ **Ensure data security** with **AI-powered identity verification**.

---

## **🎯 Problem Statement**
### **The Emergency Room Bottleneck**
- **Overcrowded ERs** lead to **long wait times**, which can be **life-threatening** in critical cases.
- **Nurses are overwhelmed** with **administrative tasks**, leaving less time for **direct patient care**.
- **Manual data entry** is **error-prone** and **time-consuming**.
- **Patients with disabilities** often face **difficulty** in accessing triage services.

### **How E.M.A Solves It**
| **Problem**                     | **Our Solution**                                                                 |
|----------------------------------|---------------------------------------------------------------------------------|
| Long wait times                  | **Automates data collection**, reducing nurse workload and speeding up triage.  |
| Paperwork burden                 | **Eliminates manual documentation** by recording patient data directly into the system. |
| Accessibility                    | **Adjustable height** and **user-friendly interface** for all patients.         |
| Identity verification            | **CompreFace facial recognition** ensures **secure and accurate patient matching**. |

---

## **🛠️ Technical Specifications**
### **🤖 Hardware Components**
| **Component**               | **Model/Type**                     | **Purpose**                                                                 |
|-----------------------------|------------------------------------|-----------------------------------------------------------------------------|
| **Primary Microcontroller** | Raspberry Pi 5                     | Main processing unit for AI, facial recognition, and data storage.         |
| **Movement Controller**     | Arduino Mega 2560                  | Handles motor control, height adjustment, and sensor data.                  |
| **Camera**                  | Logitech C920 Webcam (720p)        | Captures facial data for **CompreFace** identity verification.              |
| **ToF Sensors**             | VL53L0X (x6)                       | Detects **motion and hand gestures** for user interaction.                 |
| **Adjustable Height Mechanism** | VEX EDR 2-Wire Motors          | Modifies robot height from **2' to 4.5'** for accessibility.           |
| **Urine Testing Arm**       | Custom 3D-printed robotic arm      | Collects urine samples and analyzes test strips.                            |
| **Test Strip Reader**       | RGB sensor array                   | Detects color changes using camera vision to identify health issues.       |
| **Touchscreen Interface**   | 7-inch HDMI LCD Touchscreen        | Allows patients to input data and interact with the robot.                 |
| **Battery**                 | 12V & 5V Dual Battery Pack         | Powers the robot for **6+ hours** of continuous operation.                  |
| **Chassis**                 | Aluminium Frame                    | Lightweight, durable, and modular.                                          |

### **💻 Software & AI Models**
| **Technology**              | **Purpose**                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| **Primary OS**              | Raspberry Pi OS (64-bit)                                                   |
| **Movement Control**        | Arduino IDE (C++) for motor control and sensor integration.                 |
| **Facial Recognition**      | **CompreFace** (Open-source facial recognition library) for **secure identity verification**. |
| **Color Detection**         | **OpenCV (Python)** for detecting colors (e.g., urine test strip analysis). |
| **Data Storage**            | **Secure folder system** (patient records stored under unique IDs).         |
| **Communication**           | **UART Serial** between Raspberry Pi 5 and Arduino Mega for command passing. |

---

## **📂 Folder Structure**
```bash
EmergencyMedicalAssistant/
│
├── WRO_2024-2025_Report.pdf           # Project documentation
│
├── **/Code**                          # Source code
│   ├── /RaspberryPi                   # Raspberry Pi 5 code (Python)
│   │   ├── Face_Recognition.py        # Face recognition cross-checking code (compreface)
│   │   └── Color_Detection.py         # RGB array detection (opencv)
│   |
|   ├── /UserInterface
│   │   ├── User_Interface.py          # User interface to collect data from patients
│   │   └── Photos.png                 # Graphics utilized throughout the user interface
|   |
│   └── /Arduino                       # Arduino Mega code (C++)
│       ├── MovementCode.ino           # Controls movement and height adjustment using sensor feedback
│       └── UrineTest.ino              # Controls motion sequence for urine testing procedure
│
├── **/Diagrams**                      # Flow charts and circuit diagrams 
│   ├── Procedural_Flowchart.pdf                 
│   └── Circuit_Diagram.pdf        
│
├── **/Robot**                         # Photos and videos
│   ├── Height_Sensing.mp4             # Height changing and robot movement
│   ├── Robot_Motion.mp4
│   ├── Robot.jpg
│   ├── Test_Strip_Arm_Back_View.mp4   # Urine testing arm 
│   └── Test_Strip_Arm_Side_View.mp4
|
└── **README.md**                      # This file!

---
## **🚀 How E.M.A Works**

### **System Workflow Overview**
E.M.A operates through **four primary phases** to streamline emergency room triage:

---

### **📌 Phase 1: Patient Interaction & Data Collection**
**Objective:** Initiate contact, verify identity, and gather preliminary patient data.

1. **🚨 Motion/Gesture Detection**
   - The **VL53L0X ToF sensors** (x4) scan the environment for motion or hand gestures.
   - **Trigger:** Patient waves hand or steps within **1.5m** of E.M.A.

2. **↕️ Height Adjustment**
   - The **linear actuator** adjusts E.M.A’s height from **120cm to 180cm** based on:
     - **Patient input** (via touchscreen)
     - **Default settings** (average adult height: 160cm)
   - *Code snippet (Arduino):*
     ```cpp
     void adjustHeight(int targetHeight) {
       while (currentHeight != targetHeight) {
         if (currentHeight < targetHeight) {
           digitalWrite(heightUpPin, HIGH);
           delay(50);
           digitalWrite(heightUpPin, LOW);
         } else {
           digitalWrite(heightDownPin, HIGH);
           delay(50);
           digitalWrite(heightDownPin, LOW);
         }
         currentHeight = readHeightSensor(); // VL53L0X
       }
     }
     ```

3. **👤 Facial Recognition & Identity Verification**
   - The **Logitech C920 webcam** captures a **frontal face image**.
   - **CompreFace API** matches the image against a pre-registered database:
     - **Success:** Patient ID confirmed → Proceed to data collection.
     - **Failure:** Prompt patient to re-position or verify manually.
   - *Python snippet (Raspberry Pi):*
     ```python
     import compreface
     from compreface.service import RecognitionService

     def verify_identity(image_path):
       service = RecognitionService(
         api_key="YOUR_COMPREFACE_API_KEY",
         url="http://localhost:8000"
       )
       result = service.recognize(image_path)
       return result["verified"]
     ```

4. **🗣️ Patient Interaction**
   - **Touchscreen Interface:**
     - Displays a **symptom questionnaire** (e.g., "Do you have a fever?").
     - Allows selection of **pain levels (1–10)** or **body part icons**.
   - **Voice Commands (OpenCV + Google Speech-to-Text):**
     - Captures audio via **USB microphone**.
     - Converts speech to text and extracts **key symptoms** (e.g., "I have a headache").
   - *OpenCV color detection example:*
     ```python
     import cv2
     import numpy as np

     def detect_redness(frame):
       hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
       lower_red = np.array([0, 120, 70])
       upper_red = np.array([10, 255, 255])
       mask = cv2.inRange(hsv, lower_red, upper_red)
       return cv2.countNonZero(mask) > 5000  # Threshold for redness
     ```

---

### **📌 Phase 2: Urine Sample Collection & Analysis**
**Objective:** Automate urine testing to detect early signs of health issues.

1. **🧪 Sample Collection**
   - Patient provides urine in a **disposable cup** placed on a **weight sensor tray**.
   - E.M.A’s **3D-printed arm** deploys a **sterile pipette** to extract **5mL of sample**.
   - *Mechanical arm code (Arduino):*
     ```cpp
     void collectSample() {
       servoGripper.write(45);  // Open gripper
       delay(1000);
       servoArm.write(90);      // Move to sample
       delay(2000);
       servoPipette.write(180); // Activate pipette
       delay(3000);
       servoPipette.write(0);   // Retract pipette
     }
     ```

2. **🔬 Test Strip Analysis**
   - The sample is applied to a **standard urine test strip** (e.g., Siemens Multistix).
   - **RGB sensor array** scans the strip at **T+30 seconds** (wait time for reactions).
   - **OpenCV** analyzes color changes in **7 parameters**:
     | **Parameter**  | **Color Detection Range**       | **Threshold**               |
     |----------------|----------------------------------|-----------------------------|
     | pH             | 5.0 (red) to 8.0 (blue)          | Hue: 100–140               |
     | Protein        | Trace (yellow) to 3+ (green)     | Saturation > 80             |
     | Glucose        | Negative (tan) to 3+ (dark green)| Value > 150                 |
     | Ketones        | Negative (beige) to Large (purple)| RGB(150, 0, 150)           |
     | Blood          | Negative (yellow) to 3+ (green)  | Green channel > 100         |
     | Leukocytes     | Negative (white) to 3+ (purple)  | Hue: 270–330               |
     | Nitrites       | Negative (beige) to Positive (pink)| R > 200, G < 100, B < 100  |

   - *Python snippet (OpenCV analysis):*
     ```python
     def analyze_strip(image_path):
       strip = cv2.imread(image_path)
       hsv = cv2.cvtColor(strip, cv2.COLOR_BGR2HSV)

       results = {
         "ph": detect_pH(hsv),
         "protein": detect_protein(strip),
         "glucose": detect_glucose(strip),
         # ... other parameters
       }
       return results
     ```

3. **📊 Results Logging**
   - Data is stored in the patient’s folder:
     ```json
     {
       "patient_id": "PATIENT_001",
       "timestamp": "2025-07-20T20:00:00Z",
       "urine_test": {
         "ph": 6.5,
         "protein": "Trace",
         "glucose": "Negative",
         "ketones": "Small",
         "blood": "Negative",
         "leukocytes": "Negative",
         "nitrites": "Positive"
       }
     }
     ```

---

### **📌 Phase 3: Data Storage & Doctor Access**
**Objective:** Securely store and retrieve patient data for healthcare providers.

1. **🔒 Encrypted Data Storage**
   - Patient folders are **SHA-256 encrypted** and stored in:
     ```
     /data_storage/patient_records/
     └── PATIENT_001/
         ├── personal_info.json.enc
         ├── urine_test_results.json.enc
         └── facial_recognition_data.json.enc
     ```
   - *Encryption snippet (Python):*
     ```python
     import hashlib
     from Crypto.Cipher import AES

     def encrypt_data(data, key):
       cipher = AES.new(key, AES.MODE_EAX)
       ciphertext, tag = cipher.encrypt_and_digest(data)
       return cipher.nonce + tag + ciphertext
     ```

2. **👨‍⚕️ Doctor Dashboard Access**
   - **Secure Web Interface:**
     - Doctors log in via **biometric authentication** (CompreFace).
     - View **real-time patient queues**, test results, and alerts.
   - **Print Summary Option:**
     - E.M.A prints a **QR code** linking to the encrypted patient folder.
   - *Example dashboard API endpoint:*
     ```python
     @app.route('/api/patient/<patient_id>', methods=['GET'])
     def get_patient_data(patient_id):
       if not verify_doctor_identity(request.headers['auth_token']):
         return {"error": "Unauthorized"}, 403
       data = decrypt_patient_data(patient_id)
       return {"data": data, "access_time": datetime.now()}
     ```

---

### **📌 Phase 4: Autonomous Operation**
**Objective:** Ensure seamless, battery-efficient, and obstacle-free operation.

1. **🤖 Hardware Control (Arduino Mega)**
   - **Motor Control:**
     - **DC motors** (for base movement) and **servos** (for arm/height adjustment).
     - PID control for **precise positioning**.
   - **Sensor Integration:**
     - **VL53L0X ToF sensors** detect obstacles (**<30cm** triggers rerouting).
     - **Battery monitoring** via voltage divider (shuts down at **<11.1V**).
   - *Full motor control loop:*
     ```cpp
     void loop() {
       int distance = tofSensor.readRangeSingleMillimeter();
       if (distance < 300) {  // 30cm threshold
         navigateAroundObstacle();
       }
       updateBatteryStatus();
       delay(100);
     }
     ```

2. **💻 AI & Data Processing (Raspberry Pi 5)**
   - Runs **CompreFace**, **OpenCV**, and **data encryption** in parallel.
   - **UART Communication** with Arduino:
     ```python
     import serial
     ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

     def send_command(command):
       ser.write(command.encode())
       return ser.readline().decode().strip()
     ```

3. **⚡ Power Management**
   - **Battery:** 11.1V LiPo (5000mAh) with **low-power mode** (sleeps when idle).
   - **Charging:** Automatic switch to **12V power adapter** when docked.
   - *Power monitoring code:*
     ```python
     def check_battery():
       voltage = read_voltage()  # Analog pin on Arduino
       if voltage < 11.1:
         send_command("SHUTDOWN")
     ```

---
### **📊 System Communication Flow**
```mermaid
graph TD
    A[Patient Approaches] --> B[VL53L0X Sensors Detect Motion]
    B --> C[Arduino: Adjust Height]
    C --> D[Raspberry Pi: Capture Face Image]
    D --> E[CompreFace: Verify Identity]
    E --> F[Patient Interacts via Touchscreen/Voice]
    F --> G[Arduino: Activate Urine Arm]
    G --> H[Raspberry Pi: Analyze Test Strip]
    H --> I[Store Results in Encrypted Folder]
    I --> J[Doctor Accesses Data via Dashboard]
    J --> K[System Monitors Battery & Obstacles]
    K --> A
