from time import sleep
from flask import Flask, render_template, Response, flash, request, url_for, redirect
from flask_mail import Mail, Message
import cv2
import numpy as np
from keras.preprocessing.image import img_to_array
from tensorflow.keras.models import model_from_json, load_model
from tensorflow.keras.preprocessing import image
import imutils
import os

import config as config

model = load_model("epoch_15.hdf5")
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
camera = cv2.VideoCapture(0)

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
EMOTIONS = ["angry", "scared", "happy", "sad", "surprised", "neutral"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"


   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME

# use the app password created 
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gen_frames():                                       # generate frame by frame from camera
    while True:
        # Capture frame by frame
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = imutils.resize(frame, width=700)
            gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
            rects = detector.detectMultiScale(gray,scaleFactor=1.1,
                                minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)  
            
            if len(rects) > 0:
                rect = sorted(rects, reverse=True,
                            key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
                (fX, fY, fW, fH) = rect

                roi = gray[fY:fY + fH, fX:fX + fW]
                roi = cv2.resize(roi, (48, 48))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                preds = model.predict(roi)[0]
                label = EMOTIONS[preds.argmax()]

                for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                    text = "{}: {:.2f}%".format(emotion, prob * 100)
                    w = int(prob * 200)
                    #print(emotion, ": ", prob*100)
                    cv2.rectangle(frame, (5, (i * 35) + 5), (w, (i * 35) + 35), (0, 0, 255), -1)
                    cv2.putText(frame, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
                
                cv2.putText(frame, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)
        
            resized_img = cv2.resize(frame, (1000, 700))  
            
            ret, buffer = cv2.imencode('.jpg', frame)
            
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('Нет файловой части')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('Не выбрано изображение для загрузки')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Изображение успешно загружено')

        img = cv2.imread(app.config["UPLOAD_FOLDER"] + filename)
        img = imutils.resize(img, width=700)
        gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = detector.detectMultiScale(gray,scaleFactor=1.1,
                            minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
        
        if len(rects) > 0:
            rect = sorted(rects, reverse=True,
                        key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = rect

            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = model.predict(roi)[0]
            label = EMOTIONS[preds.argmax()]

            emo = dict()
            for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                text = "{}: {:.2f}%".format(emotion, prob * 100)
                w = int(prob * 200)
                emo[emotion] = prob*100
                            
            cv2.putText(img, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.rectangle(img, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)

            cv2.imwrite(app.config["UPLOAD_FOLDER"] + filename, img)

            return render_template('3rd_section.html', filename=filename, percent=emo)
        else:
            flash('Без лица')
            return redirect(request.url)
    else:
        flash('Допустимые типы изображений: - png, jpg, jpeg')
        return redirect(request.url)

@app.route('/contact', methods=['POST'])
def send_mail():
    #getting the html inputs and referencing them
    name = request.form['name']
    email = request.form['email']
    recipients = app.config['MAIL_USERNAME'] 
    content = "Name:" + name + "\nEmail:" + email + "\nContent:" + request.form['content']
    subject = "Mail from web"
    
    # inputing the message in the correct order
    msg = Message(subject, sender=email, recipients = [recipients] )
    msg.body = content
    mail.send(msg)
    flash("Почта успешно отправлена")
    return redirect(url_for("contact"))


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/')
def index():
    return render_template('1st_section.html')

@app.route('/video')
def video():
    return render_template('2nd_section.html')

@app.route('/image')
def image():
    return render_template("3rd_section.html", percent=0)

@app.route('/teams')
def teams():
    return render_template("4th_section.html")   

@app.route('/contact')
def contact():
    return render_template("5th_section.html")

if __name__ == '__main__':
    app.run(debug=True)