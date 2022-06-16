from flask import Flask, render_template, Response, request, flash
from .facereco import gen_frames
import os
from pathlib import Path
from .pickle_measurements import add_into_pickle


PEOPLE_FOLDER = os.path.join(Path(__file__).resolve().parent, "static/capture_image")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = PEOPLE_FOLDER
app.config["SECRET_KEY"] = "dev"

@app.route("/")
def index():
    static_url = "capture_image/Frame0.jpg"
    return render_template("index.html", static_url=static_url)

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/content')
def content():
    with open("face_capture_log.txt", "r") as f:
        data = f.read()
    return Response(data, mimetype='text/plain')

@app.route('/person_details')
def person_details():
    with open("face_capture_log.txt", "r") as f:
        data = f.read()
        last_face_details = data.splitlines()[-1]
    return Response(last_face_details, mimetype='text/plain')

@app.route("/upload", methods=["POST", "GET"])
def upload():
    static_url = "capture_image/Frame0.jpg"
    if request.method == "POST":
        name = request.form["name"]
        image = request.form["my_image"]
        add_into_pickle(name, image.split("/")[1])

        flash(f"File Uploaded name : {image.split('/')[1]} and your name is %s" % name)
    return render_template("upload.html", static_url=static_url)
