# 🎓 Smart Attendance System using Face Recognition

A desktop-based **Face Recognition Attendance System** developed in **Python** using **OpenCV and Tkinter**.  
The system automatically identifies registered individuals via webcam and records their attendance in a CSV file with date and time.

This project is developed as a **Python Mini Project** for academic purposes.

---

## 📌 Project Overview

Traditional attendance systems are time-consuming and prone to errors and proxy attendance.  
This project provides a **contactless, automated, and reliable solution** using **computer vision and machine learning** techniques.

The system:

- Detects faces in real time using **Haar Cascade**
- Recognizes faces using **LBPH (Local Binary Patterns Histogram)**
- Logs attendance automatically in a **CSV file**
- Provides a simple **GUI-based interface** using Tkinter

---

## ✨ Features

- 📷 Real-time face detection via webcam
- 🧠 Face recognition using LBPH algorithm
- 🧾 Automatic attendance logging (Name, Date, Time)
- ➕ Add new faces directly using webcam
- 👁️ View attendance records inside the application
- 🚫 Prevents duplicate attendance for the same day
- 🖥️ Simple and user-friendly Tkinter GUI

---

## 🛠️ Technologies Used

- Python
- OpenCV (opencv-contrib-python)
- NumPy
- Tkinter
- CSV File Handling

---

## ⚙️ Installation

1. Clone or download the project.
2. Navigate to the project directory:
   ```bash
   cd face_attendance_project
   ```
3. Install required dependencies:
   pip install -r requirements.txt

## ⚠️ Important:

Use Python 3.10 or Python 3.11 for best compatibility with OpenCV.
OpenCV may be unstable with Python 3.13.

---

## ▶️ How to Run

python main.py

-The GUI window will open with the following options:
-Start Attendance
-Add New Face
-View Attendance
-Exit

---

## ➕ Adding a New Face (Enrollment)

1. Click **Add New Face**
2. Enter the person’s name when prompted
3. Webcam window opens
4. Position the face properly inside the frame
5. Press **SPACE** to capture the face
6. The face image is saved in `known_faces/`
7. The recognizer retrains automatically

---

## ✅ Marking Attendance

1. Click **Start Attendance**
2. Webcam opens and detects faces in real time
3. Recognized faces are highlighted in **green**
4. Unknown faces are highlighted in **red**
5. Attendance is recorded automatically in `attendance.csv`
6. Duplicate entries for the same day are prevented
7. Press **ESC** to exit attendance mode

---

## 📊 Viewing Attendance Records

1. Click **View Attendance**
2. Attendance records are displayed in a scrollable window
3. Each record includes:
   - Name
   - Date
   - Time

---

## 🧠 System Workflow

1. Load face images from `known_faces/`
2. Convert images to grayscale and resize
3. Train the LBPH face recognizer
4. Capture live video from webcam
5. Detect faces using Haar Cascade
6. Recognize faces using LBPH
7. Log attendance in CSV file

---

## 📄 Attendance File Format (`attendance.csv`)

Name, Date, Time
Pritesh, 2025-10-08, 10:12:35
Jalmesh, 2025-10-08, 10:13:02
Siddhesh, 2025-10-08, 10:14:10

---

## 🚀 Future Enhancements

- Deep learning-based recognition (FaceNet / CNN)
- Multiple face recognition in a single frame
- Cloud database integration
- Web-based or mobile-based attendance system
- Analytics dashboard and reports
- Anti-spoofing (photo/video detection)
- Admin authentication system

---

## 🎓 Academic Details

**Project Title:**  
Smart Attendance System using Face Recognition

**Course:**  
Bachelor of Engineering – Electronics & Computer Science Engineering

**Academic Year:**  
2025 – 2026

---

## 👨‍💻 Author(s)

- Pritesh Mahajan
- Jalmesh Mhatre
- Siddhesh Murkute

---

## 📚 References

- OpenCV Documentation – https://opencv.org
- Python Official Documentation – https://www.python.org
- GeeksforGeeks – OpenCV & Tkinter Tutorials
- TutorialsPoint – Python GUI Programming
