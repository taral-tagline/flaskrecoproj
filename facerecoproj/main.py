from flask import Flask, render_template, Response,request,redirect,flash,url_for
from .facereco import gen_frames
import os
from pathlib import Path

PEOPLE_FOLDER = os.path.join(Path(__file__).resolve().parent, 'static/capture_image')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route("/")
def index():
    static_url = "capture_image/taral.jpeg"
    return render_template("index.html", static_url = static_url)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/upload",methods = ['POST','GET'])
def upload():
    static_url = "capture_image/taral.jpeg"
    if request.method == 'POST':  
        uname=request.form['input_name']
        upload_file = request.files['input_file']
        filename = upload_file.filename
        # # Store Form Data into table
        # upload = Upload(name=uname , data = upload_file.read())
        # db.session.add(upload)
        # db.session.commit()

        # Store image in folder
        upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # upload_image = cv2.imread(PEOPLE_FOLDER + upload_file.filename)
        simple_msg = f'File Uploaded name : {filename} and your name is %s' %uname

        return render_template('upload.html',simple_msg = simple_msg, static_url = static_url)
    else:
        return render_template('upload.html', static_url = static_url)

@app.route('/display/<filename>')
def display_image():
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='capture_image/taral.jpeg'), code=301)