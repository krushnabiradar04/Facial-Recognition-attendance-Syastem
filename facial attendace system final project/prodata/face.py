import cv2
import numpy as np
import face_recognition as face_rec
import os
import pyttsx3 as textSpeech
from datetime import datetime, timedelta
import sqlite3

# Initialize text-to-speech engine
engine = textSpeech.init()

# Resize function for images
def resize(img, size):
    width = int(img.shape[1] * size)
    height = int(img.shape[0] * size)
    dimension = (width, height)
    return cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)

# Database connection setup
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return conn

# Create attendance table
def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_number TEXT NOT NULL,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while creating the table")

# Insert attendance record
def insert_attendance(conn, roll_number, name):
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')
    sql = "INSERT INTO attendance (roll_number, name, date, time) VALUES (?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(sql, (roll_number, name, date_str, time_str))
    conn.commit()

# Retrieve attendance records from the last week or month
def retrieve_attendance(conn, period='week'):
    cursor = conn.cursor()
    if period == 'week':
        date_from = (datetime.now() - timedelta(weeks=1)).strftime('%Y-%m-%d')
    elif period == 'month':
        date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    else:
        print("Invalid period specified. Use 'week' or 'month'.")
        return

    cursor.execute("SELECT * FROM attendance WHERE date >= ?", (date_from,))
    records = cursor.fetchall()
    for record in records:
        print(record)

# Initialize and connect to the database
db_path = 'attendance.db'
conn = create_connection(db_path)
create_table(conn)

# Load student images and extract names and roll numbers
path = 'student_images'
studentImg = []
studentData = {}  # Dictionary to hold roll numbers and names
myList = os.listdir(path)
for cl in myList:
    curimg = cv2.imread(f'{path}/{cl}')
    studentImg.append(curimg)
    roll_number, name = os.path.splitext(cl)[0].split('_')  # Split filename into roll number and name
    studentData[roll_number] = name

# Function to find encodings
def findEncoding(images):
    imgEncodings = []
    for img in images:
        img = resize(img, 0.50)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeimg = face_rec.face_encodings(img)[0]
        imgEncodings.append(encodeimg)
    return imgEncodings

# Function to mark attendance in the database
def markAttendance(roll_number):
    name = studentData[roll_number]  # Get the name from the roll number
    today = datetime.now().strftime('%Y-%m-%d')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance WHERE roll_number = ? AND date = ?", (roll_number, today))
    result = cursor.fetchone()
    if not result:  # If not already marked
        insert_attendance(conn, roll_number, name)
        statement = f'Welcome to class, {name}'
        engine.say(statement)
        engine.runAndWait()

# Encoding images
EncodeList = findEncoding(studentImg)

# Capture video
vid = cv2.VideoCapture(0)
while True:
    success, frame = vid.read()
    Smaller_frames = cv2.resize(frame, (0, 0), None, 0.25, 0.25)

    facesInFrame = face_rec.face_locations(Smaller_frames)
    encodeFacesInFrame = face_rec.face_encodings(Smaller_frames, facesInFrame)

    for encodeFace, faceloc in zip(encodeFacesInFrame, facesInFrame):
        matches = face_rec.compare_faces(EncodeList, encodeFace)
        facedis = face_rec.face_distance(EncodeList, encodeFace)
        matchIndex = np.argmin(facedis)

        if matches[matchIndex]:
            roll_number = list(studentData.keys())[matchIndex]  # Get roll number by index
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.rectangle(frame, (x1, y2 - 25), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, roll_number, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(roll_number)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on pressing 'q'
        break

vid.release()
cv2.destroyAllWindows()

# Example of retrieving records from today
retrieve_attendance(conn, period='week')
# Example of retrieving records from the last month
retrieve_attendance(conn, period='month')

# Close the database connection
conn.close()
