import os
import csv
import cv2
import numpy as np
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from datetime import datetime

# ================= CONFIG =================
KNOWN_DIR = "known_faces"
ATTENDANCE_CSV = "attendance.csv"
FACE_SIZE = (200, 200)
RECOG_THRESHOLD = 60

# Auto-load Haar Cascade from OpenCV
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# ==========================================

face_cascade = None
recognizer = None
known_faces = []
labels = []
label_to_name = {}

# ---------- INITIALIZATION ----------
def initialize_modules():
    global face_cascade, recognizer

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    if face_cascade.empty():
        raise RuntimeError(f"Failed to load Haar cascade from {CASCADE_PATH}")

    recognizer = cv2.face.LBPHFaceRecognizer_create()

def ensure_known_dir():
    os.makedirs(KNOWN_DIR, exist_ok=True)

def load_known_faces():
    global known_faces, labels, label_to_name

    ensure_known_dir()
    known_faces.clear()
    labels.clear()
    label_to_name.clear()

    files = [f for f in os.listdir(KNOWN_DIR)
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not files:
        print("⚠️ No known faces found")
        return

    name_to_label = {}
    next_label = 0

    for file in files:
        path = os.path.join(KNOWN_DIR, file)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        img = cv2.resize(img, FACE_SIZE)
        name = file.split("_")[0]

        if name not in name_to_label:
            name_to_label[name] = next_label
            label_to_name[next_label] = name
            next_label += 1

        known_faces.append(img)
        labels.append(name_to_label[name])

    if known_faces:
        recognizer.train(known_faces, np.array(labels))
        print("✅ Trained faces:", label_to_name)

# ---------- ATTENDANCE ----------
def initialize_attendance_file():
    if not os.path.exists(ATTENDANCE_CSV):
        with open(ATTENDANCE_CSV, "w", newline="") as f:
            csv.writer(f).writerow(["Name", "Date", "Time"])

def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")

    with open(ATTENDANCE_CSV, "r") as f:
        rows = list(csv.reader(f))

    for r in rows[1:]:
        if r[0] == name and r[1] == date:
            return

    with open(ATTENDANCE_CSV, "a", newline="") as f:
        csv.writer(f).writerow(
            [name, date, now.strftime("%H:%M:%S")]
        )

    print("✅ Attendance marked:", name)

def get_attendance_records():
    if not os.path.exists(ATTENDANCE_CSV):
        return []
    with open(ATTENDANCE_CSV, "r") as f:
        return list(csv.reader(f))

# ---------- CAMERA ----------
def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Cannot access camera")
        return None
    return cap

# ---------- ADD FACE ----------
def add_new_face():
    name = simpledialog.askstring("New Face", "Enter Name:")
    if not name:
        return

    cap = open_camera()
    if cap is None:
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Add Face | SPACE = Capture | ESC = Exit", frame)
        key = cv2.waitKey(1)

        if key == 27:
            break

        if key == 32 and len(faces) > 0:
            x, y, w, h = faces[0]
            face = gray[y:y + h, x:x + w]
            face = cv2.resize(face, FACE_SIZE)

            filename = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            cv2.imwrite(os.path.join(KNOWN_DIR, filename), face)
            break

    cap.release()
    cv2.destroyAllWindows()
    load_known_faces()
    messagebox.showinfo("Success", "Face added successfully")

# ---------- ATTENDANCE MODE ----------
def start_attendance():
    if not known_faces:
        messagebox.showwarning("Warning", "Add faces first!")
        return

    cap = open_camera()
    if cap is None:
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face = cv2.resize(face, FACE_SIZE)

            label, conf = recognizer.predict(face)

            if conf < RECOG_THRESHOLD:
                name = label_to_name[label]
                mark_attendance(name)
                color = (0, 255, 0)
            else:
                name = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                frame, name, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2
            )

        cv2.imshow("Attendance | ESC to Exit", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------- GUI ----------
def run_thread(func):
    threading.Thread(target=func, daemon=True).start()

def show_attendance():
    records = get_attendance_records()
    if len(records) <= 1:
        messagebox.showinfo("Attendance", "No records")
        return

    win = tk.Toplevel()
    win.title("Attendance Records")

    text = scrolledtext.ScrolledText(win, width=50, height=20)
    text.pack()

    for r in records:
        text.insert(tk.END, f"{r}\n")

    text.config(state=tk.DISABLED)

def gui_main():
    initialize_modules()
    load_known_faces()
    initialize_attendance_file()

    root = tk.Tk()
    root.title("Face Attendance System")
    root.geometry("400x400")

    tk.Label(
        root,
        text="FACE ATTENDANCE SYSTEM",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    tk.Button(
        root,
        text="Start Attendance",
        width=25,
        command=lambda: run_thread(start_attendance)
    ).pack(pady=10)

    tk.Button(
        root,
        text="Add New Face",
        width=25,
        command=lambda: run_thread(add_new_face)
    ).pack(pady=10)

    tk.Button(
        root,
        text="View Attendance",
        width=25,
        command=show_attendance
    ).pack(pady=10)

    tk.Button(
        root,
        text="Exit",
        width=25,
        command=root.destroy
    ).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    gui_main()
