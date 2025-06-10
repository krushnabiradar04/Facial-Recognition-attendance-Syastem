# Face Recognition Attendance System

This is a Python-based attendance system that uses face recognition to mark attendance. It uses a webcam to detect and recognize student faces and stores attendance records in a SQLite database.

## 🧠 Features

- Real-time face detection and recognition using webcam
- Text-to-speech greeting on successful recognition
- Automatic attendance marking with roll number and name
- SQLite database for storing and retrieving attendance records
- Supports weekly and monthly attendance retrieval

## 🛠️ Tech Stack

- Python
- OpenCV
- face_recognition
- SQLite
- pyttsx3 (text-to-speech)

## 📁 Project Structure


├── face.py # Main Python script for running the system
├── attendance.db # SQLite database file
├── student_images/ # Folder containing student images named as <roll_number>_<name>.jpg
├── data.db # (Optional) Another DB if used
└── attendance.sqbpro # (Optional) SQLite project file for DB browsing


## 🖼️ Student Images Format

Place all student images in a folder called `student_images`.  
**Image naming format:**  
`rollnumber_name.jpg`  
**Example:**  
`101_John.jpg`

## 🚀 How to Run

1. Install required libraries:

```bash
pip install opencv-python face_recognition pyttsx3


2. Place student images in the student_images folder.

3. Run the script:
                  python face.py

4. Press q to quit the webcam view.

📊 View Attendance
The script supports retrieving attendance from the last week or month by calling:
         retrieve_attendance(conn, period='week')  # or 'month'

📌 Notes
Make sure your webcam is connected.

Ensure images are clear and faces are well-lit.

Avoid duplicate roll numbers.

📄 License
This project was created as a final year project for academic purposes at [Your College Name].

You are free to:

View and use the code for educational and non-commercial purposes.

Modify the code with proper attribution.

Copyright © [Krushna Biradar], [2025]

For permissions or questions, contact: [krushnabiradar9637@gmail.com]








