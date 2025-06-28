import tkinter as tk
from tkinter import messagebox
import os
import cv2
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import pyttsx3
import threading

import show_attendance
import takeImage
import trainImage

# --- Subject Attendance Module ---
def subjectChoose(text_to_speech, frame):
    def FillAttendance():
        sub = tx.get()
        if sub == "":
            text_to_speech("Please enter the subject name!!!")
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read(trainimagelabel_path)
                face_cascade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                attendance = pd.DataFrame(columns=["Enrollment", "Name"])
                start_time = time.time()

                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                        if conf < 70:
                            name = df.loc[df["Enrollment"] == Id]["Name"].values[0]
                            attendance.loc[len(attendance)] = [Id, name]
                            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)
                            cv2.putText(im, f"{Id}-{name}", (x, y-10), font, 0.75, (0, 255, 0), 2)
                        else:
                            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 0, 255), 2)
                            cv2.putText(im, "Unknown", (x, y-10), font, 0.75, (0, 0, 255), 2)

                    cv2.imshow("Filling Attendance", im)
                    if time.time() - start_time > 20:
                        break
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

                cam.release()
                cv2.destroyAllWindows()

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                attendance[date] = 1
                subject_path = os.path.join(attendance_path, sub)
                os.makedirs(subject_path, exist_ok=True)
                fileName = os.path.join(subject_path, f"{sub}_{date}_{Hour}-{Minute}-{Second}.csv")
                attendance.drop_duplicates(["Enrollment"], keep="first", inplace=True)
                attendance.to_csv(fileName, index=False)
                text_to_speech(f"Attendance Filled Successfully for {sub}")

                msg_label.configure(text=f"Attendance Filled Successfully for {sub}", fg="green")
            except Exception as e:
                msg_label.configure(text="Error: Unable to process attendance", fg="red")
                text_to_speech("No face found or model not trained properly")
                cv2.destroyAllWindows()

    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Enter Subject Name", font=("Segoe UI", 20), bg="white", fg="#2E3B55").pack(pady=20)
    tx = tk.Entry(frame, font=("Segoe UI", 16), width=30, relief="solid", bd=2)
    tx.pack(pady=10)

    style = {"font": ("Segoe UI", 14), "bg": "#2E3B55", "fg": "white", "width": 20, "relief": "flat", "bd": 0}

    tk.Button(frame, text="Fill Attendance", command=FillAttendance, **style).pack(pady=10)
    msg_label = tk.Label(frame, text="", font=("Segoe UI", 14), bg="white")
    msg_label.pack(pady=10)

# Set paths
base_path = "D:\\INTERN PROJECT\\Attendance-Management-system-using-face-recognition-master"
haarcasecade_path = os.path.join(base_path, "haarcascade_frontalface_default.xml")
trainimagelabel_path = os.path.join(base_path, "TrainingImageLabel\\Trainner.yml")
trainimage_path = os.path.join(base_path, "TrainingImage")
studentdetail_path = os.path.join(base_path, "StudentDetails\\studentdetails.csv")
attendance_path = os.path.join(base_path, "Attendance")

for path in [trainimage_path, attendance_path]:
    os.makedirs(path, exist_ok=True)

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

window = tk.Tk()
window.title("Face Recognition Attendance System")
window.state("zoomed")
window.configure(bg="#F4F6F8")

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)

sidebar = tk.Frame(window, bg="#2E3B55", width=220)
sidebar.grid(row=0, column=0, sticky="ns")

main_frame = tk.Frame(window, bg="white")
main_frame.grid(row=0, column=1, sticky="nsew")
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

logo_path = os.path.join(base_path, "UI_Image", "0002.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    logo = logo.resize((50, 47), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(main_frame, image=logo_img, bg="white")
    logo_label.image = logo_img
    logo_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)

title_label = tk.Label(
    main_frame,
    text="Welcome to VINAYAKA MISSION",
    font=("Segoe UI", 28, "bold"),
    bg="white",
    fg="#2E3B55"
)
title_label.grid(row=0, column=1, sticky="w", padx=10, pady=20)

content_frame = tk.Frame(main_frame, bg="white")
content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=40, pady=20)

def clear_content_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

def load_register_frame():
    clear_content_frame()

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        if l1 == "" or l2 == "":
            messagebox.showerror("Error", "Enrollment and Name required")
            return
        takeImage.TakeImage(l1, l2, haarcasecade_path, trainimage_path, msg_label, messagebox.showerror, text_to_speech)
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    def train_image():
        trainImage.TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, msg_label, text_to_speech)

    tk.Label(content_frame, text="Enrollment No", font=("Segoe UI", 16), bg="white", anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    txt1 = tk.Entry(content_frame, font=("Segoe UI", 16), width=30, relief="solid", bd=2)
    txt1.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(content_frame, text="Name", font=("Segoe UI", 16), bg="white", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    txt2 = tk.Entry(content_frame, font=("Segoe UI", 16), width=30, relief="solid", bd=2)
    txt2.grid(row=1, column=1, padx=10, pady=10)

    msg_label = tk.Label(content_frame, text="", font=("Segoe UI", 14), bg="white", fg="green")
    msg_label.grid(row=2, column=0, columnspan=2, pady=10)

    style = {"font": ("Segoe UI", 14), "bg": "#2E3B55", "fg": "white", "width": 15, "relief": "flat", "bd": 0}
    tk.Button(content_frame, text="Take Image", command=take_image, **style).grid(row=3, column=0, pady=20)
    tk.Button(content_frame, text="Train Image", command=train_image, **style).grid(row=3, column=1, pady=20)

def load_attendance_frame():
    clear_content_frame()
    subjectChoose(text_to_speech, frame=content_frame)

def load_view_frame():
    clear_content_frame()
    show_attendance.subjectchoose(text_to_speech)

btn_style = {"font": ("Segoe UI", 14), "bg": "#2E3B55", "fg": "white", "bd": 0,
             "activebackground": "#1C2538", "pady": 15, "anchor": "w"}

tk.Button(sidebar, text="Register Student", command=load_register_frame, **btn_style).pack(fill="x")
tk.Button(sidebar, text="Take Attendance", command=load_attendance_frame, **btn_style).pack(fill="x")
tk.Button(sidebar, text="View Attendance", command=load_view_frame, **btn_style).pack(fill="x")
tk.Button(sidebar, text="Exit", command=window.quit, **btn_style).pack(fill="x")

window.mainloop()
