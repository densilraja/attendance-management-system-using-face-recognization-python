import tkinter as tk
from tkinter import messagebox
import os
import cv2
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import pyttsx3

import show_attendance
import takeImage
import trainImage
import automaticAttedance

# Set paths
base_path = "D:\INTERN PROJECT\Attendance-Management-system-using-face-recognition-master"
haarcasecade_path = os.path.join(base_path, "haarcascade_frontalface_default.xml")
trainimagelabel_path = os.path.join(base_path, "TrainingImageLabel\Trainner.yml")
trainimage_path = os.path.join(base_path, "TrainingImage")
studentdetail_path = os.path.join(base_path, "StudentDetails\studentdetails.csv")
attendance_path = os.path.join(base_path, "Attendance")

# Ensure required folders exist
for path in [trainimage_path, attendance_path]:
    os.makedirs(path, exist_ok=True)

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

# --- Window setup ---
window = tk.Tk()
window.title("Face Recognition Attendance System")
window.state("zoomed")
window.configure(bg="#F4F6F8")

# --- Layout Configuration ---
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)

# --- Sidebar ---
sidebar = tk.Frame(window, bg="#2E3B55", width=220)
sidebar.grid(row=0, column=0, sticky="ns")

# --- Main Frame ---
main_frame = tk.Frame(window, bg="white")
main_frame.grid(row=0, column=1, sticky="nsew")
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# --- Header ---
logo_path = os.path.join(base_path, "UI_Image", "0004.png")
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

# --- Content Frame ---
content_frame = tk.Frame(main_frame, bg="white")
content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=40, pady=20)

# --- Functions ---
def load_register_frame():
    clear_content_frame()
    highlight_button("Register Student")

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
    txt1 = tk.Entry(content_frame, font=("Segoe UI", 16), width=30, bd=2, relief="solid")
    txt1.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(content_frame, text="Name", font=("Segoe UI", 16), bg="white", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    txt2 = tk.Entry(content_frame, font=("Segoe UI", 16), width=30, bd=2, relief="solid")
    txt2.grid(row=1, column=1, padx=10, pady=10)

    msg_label = tk.Label(content_frame, text="", font=("Segoe UI", 14), bg="white", fg="green")
    msg_label.grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(content_frame, text="Take Image", command=take_image, font=("Segoe UI", 14), bg="#2E3B55", fg="white", width=15).grid(row=3, column=0, pady=20)
    tk.Button(content_frame, text="Train Image", command=train_image, font=("Segoe UI", 14), bg="#2E3B55", fg="white", width=15).grid(row=3, column=1, pady=20)

def load_attendance_frame():
    clear_content_frame()
    highlight_button("Take Attendance")
    automaticAttedance.subjectChoose(text_to_speech, frame=content_frame)

def load_view_frame():
    clear_content_frame()
    highlight_button("View Attendance")
    show_attendance.subjectchoose(text_to_speech, frame=content_frame)

def clear_content_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

# --- Sidebar Buttons ---
buttons = {}
active_button = None

def highlight_button(name):
    global active_button
    for btn_name, btn in buttons.items():
        if btn_name == name:
            btn.configure(bg="#1C2538")
            active_button = btn_name
        else:
            btn.configure(bg="#2E3B55")

btn_style = {"font": ("Segoe UI", 14), "bg": "#2E3B55", "fg": "white", "bd": 0,
             "activebackground": "#1C2538", "pady": 15, "anchor": "w"}

buttons["Register Student"] = tk.Button(sidebar, text="Register Student", command=load_register_frame, **btn_style)
buttons["Register Student"].pack(fill="x")

buttons["Take Attendance"] = tk.Button(sidebar, text="Take Attendance", command=load_attendance_frame, **btn_style)
buttons["Take Attendance"].pack(fill="x")

buttons["View Attendance"] = tk.Button(sidebar, text="View Attendance", command=load_view_frame, **btn_style)
buttons["View Attendance"].pack(fill="x")

buttons["Exit"] = tk.Button(sidebar, text="Exit", command=window.quit, **btn_style)
buttons["Exit"].pack(fill="x")

# Start the app
window.mainloop()
