import cv2
import os
import face_recognition
import pickle
import numpy as np
from flask import Flask, render_template, request, Response
from pathlib import Path

PEOPLE_FOLDER = os.path.join(Path(__file__).resolve().parent, "static/capture_image")
knownEncodings = []
knownNames = []

# store masurments in pickle file
def add_into_pickle(uname, image_path):
    upload_image = cv2.imread(PEOPLE_FOLDER+f"/{image_path}")
    rgb = cv2.cvtColor(upload_image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,model='cnn')
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(uname)

    new_encodings = []
    new_names = []
    if os.path.getsize("face_enc.pickle") > 0:
        file = open("face_enc.pickle",'rb') 
        old_data = pickle.load(file)

        new_encodings = old_data['encodings']
        new_names = old_data['names']

    for item in range(0,len(knownEncodings)):
        new_encodings.append(knownEncodings[item])
        new_names.append(knownNames[item])


    # save emcodings along with their names in dictionary data
    data = {"encodings": new_encodings, "names": new_names}

    # use pickle to save data into a file for later use
    with open("face_enc.pickle", "wb") as wfp:
        pickle.dump(data, wfp)