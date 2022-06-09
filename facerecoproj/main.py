import cv2
from flask import Flask, render_template, Response, request,flash
from .facereco import gen_frames
from .pickle_mesurments import add_into_pickle
import os
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy


PEOPLE_FOLDER = os.path.join(Path(__file__).resolve().parent, "static/capture_image")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = PEOPLE_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev"

db = SQLAlchemy(app)
db.init_app(app)


PEOPLE_FOLDER = os.path.join(Path(__file__).resolve().parent, "static/capture_image")
knownEncodings = []
knownNames = []
capture = 0


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = PEOPLE_FOLDER


@app.route("/")
def index():
    static_url = "capture_image/capture.jpg"
    return render_template("index.html", static_url=static_url)


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/upload", methods=["POST", "GET"])
def upload():
    static_url = "capture_image/capture.jpg"
    if request.method == "POST":
        name = request.form["name"]
        dept = request.form["department"]
        gender = request.form["gender"]
        user = User(name=name, dept=dept, gender=gender)
        db.session.add(user)
        db.session.commit()
        upload_file = request.files["file"]
        filename = upload_file.filename
        upload_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # store masurments in pickle file
        add_into_pickle(name)

        flash(f"File Uploaded name : {filename} and your name is %s" % name)
    return render_template("upload.html", static_url=static_url)

from .db import *