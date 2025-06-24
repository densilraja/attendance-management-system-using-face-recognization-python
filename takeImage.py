import csv
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time
import threading

# Safe text-to-speech wrapper in a separate thread
def speak_threaded(text, tts_func):
    threading.Thread(target=tts_func, args=(text,), daemon=True).start()

# Take Image of user
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if (l1 == "") and (l2 == ""):
        speak_threaded('Please enter your Enrollment Number and Name.', text_to_speech)
        return
    elif l1 == "":
        speak_threaded('Please enter your Enrollment Number.', text_to_speech)
        return
    elif l2 == "":
        speak_threaded('Please enter your Name.', text_to_speech)
        return

    try:
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cam.isOpened():
            speak_threaded("Cannot access the camera. Please check if it is connected or used by another app.", text_to_speech)
            return

        detector = cv2.CascadeClassifier(haarcasecade_path)
        Enrollment = l1
        Name = l2
        sampleNum = 0
        directory = Enrollment + "_" + Name
        path = os.path.join(trainimage_path, directory)

        try:
            os.mkdir(path)
        except FileExistsError:
            speak_threaded("Student data already exists.", text_to_speech)
            return

        print("Camera started. Press 'q' to quit.")

        while True:
            ret, img = cam.read()
            if not ret:
                print("Failed to capture frame")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                sampleNum += 1

                # Save the image in a thread to avoid UI freezing
                face_img = gray[y:y + h, x:x + w]
                img_filename = f"{Name}_{Enrollment}_{sampleNum}.jpg"
                save_path = os.path.join(path, img_filename)
                threading.Thread(target=cv2.imwrite, args=(save_path, face_img), daemon=True).start()

            cv2.imshow("Face Capture - Press 'q' to Quit", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if sampleNum >= 50:
                break

            # Optional: sleep a bit to reduce CPU usage
            time.sleep(0.01)

        cam.release()
        cv2.destroyAllWindows()

        # Save student record
        row = [Enrollment, Name]
        with open("StudentDetails/studentdetails.csv", "a+", newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=",")
            writer.writerow(row)

        res = f"Images saved for ER No: {Enrollment}, Name: {Name}"
        message.configure(text=res)
        speak_threaded(res, text_to_speech)

    except Exception as e:
        speak_threaded(f"An error occurred: {str(e)}", text_to_speech)
