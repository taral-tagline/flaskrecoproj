import face_recognition
import cv2
import numpy as np
import os
from pathlib import Path

camera = cv2.VideoCapture(os.path.join(Path(__file__).resolve().parent, "static/capture_image/face_video.mp4"))

my_image = face_recognition.load_image_file(os.path.join(Path(__file__).resolve().parent, "static/capture_image/taral.jpeg"))
my_encodings = face_recognition.face_encodings(my_image)[0]

known_face_encodings = [my_encodings]
known_face_names = ["taral"]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def gen_frames():  
    count = 0
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
                    
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings :
                    # see if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # or instead, use the known face with the smallest distence
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index] :
                        name = known_face_names[best_match_index]
                    
                    # person not identify capture the image
                    if name == "Unknown":
                    # Save Frame into disk using imwrite method
                        if count == 0 :
                            cv2.imwrite(os.path.join(Path(__file__).resolve().parent, 'static/capture_image/Frame'+str(count)+'.jpg'), frame)
                            count += 1
                    
                    face_names.append(name)

            # display the results
            for (top, right, bottom, left), name in zip(face_locations,face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box arround the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left,bottom - 35),(right,bottom),(0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result