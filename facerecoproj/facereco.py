from datetime import datetime
import face_recognition
import cv2
import numpy as np
import os
from pathlib import Path
import pickle
from .pickle_measurements import add_into_pickle

# os.path.join(Path(__file__).resolve().parent, "static/capture_image/face_video.mp4")
camera = cv2.VideoCapture(0)
LESS_THAN_50_ACC = False

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
known_face_encodings = []
known_face_names = []



def variance_of_laplacian(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()

def gen_frames():

    if os.path.getsize("face_enc.pickle") > 0:
        data = pickle.loads(open('face_enc.pickle', "rb").read())
        known_face_encodings = data['encodings']
        known_face_names = data['names']
    
    image_capture = 0
    process_this_frame = True
    persons = []
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition process
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # convert image from BGR (which OpenCV uses) to Rgb Color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # only process every other frame of video of save time
            if process_this_frame:
                # find all the face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                if face_locations == []:
                    persons = []

                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                face_names = []
                for face_encoding in face_encodings:
                    # see if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding, tolerance=0.5
                    )
                    name = "Unknown"

                    # or instead, use the known face with the smallest distence
                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding
                    )

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]


                    # person not identify capture the image
                    if name == "Unknown":
                        # Save Frame into disk using imwrite method
                        if image_capture == 0:
                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            fm = variance_of_laplacian(gray)
                            if fm < 100 :
                                continue
                            cv2.imwrite(os.path.join(Path   (__file__).resolve().parent,"static/capture_image/Unknown.jpg",),frame,)
                            image_capture += 1
                    else:
                        if name not in persons :
                            persons.append(name)
                            # dd/mm/YY H:M:S
                            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            f=open('face_capture_log.txt','a')
                            f.write(f"{name} : {dt_string} <br> \n")
                            f.close()
                        
                        # if accuracy less then 60 percent but get accurate name store name and masurments.
                        if face_distances[best_match_index] > 0.4 :
                            global LESS_THAN_50_ACC
                            if not LESS_THAN_50_ACC:
                                LESS_THAN_50_ACC = not LESS_THAN_50_ACC
                                cv2.imwrite(os.path.join(Path   (__file__).resolve().parent,"static/capture_image/Accuracy_image.jpg",),frame,)
                                add_into_pickle(known_face_names[best_match_index], "Accuracy_image.jpg")
                                img_path = os.path.join(Path(__file__).resolve().parent, "static/capture_image/Accuracy_image.jpg")
                                os.remove(img_path)

                    face_names.append(name)

            process_this_frame = not process_this_frame
            
            # display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box arround the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(
                    frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
                )
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(
                    frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
                )

            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (
                b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )  # concat frame one by one and show result
            
            # if face_names == []:
            #     pass
            # elif "Unknown" not in face_names :
            #     break