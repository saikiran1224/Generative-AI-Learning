# importing flask library
from flask import Flask, render_template, url_for, Response

# importing opencv
import cv2

# creating object
app = Flask(__name__)

# to access webcam
camera = cv2.VideoCapture(0)

# function to generate frames
def generate_frames():

    while True:

        # reading the camera frame
        success, frame = camera.read() # returns two parameters - bool (success or fail), frame

        # checking if success is false means camera is unable to read
        if not success: # not getting frames so we are breaking the while loop here.
            break
        else:

            # importing required classifiers - clone it from OpenCV repository in github
            detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')
            
            # detecting faces - returns the face coordinates (X, y, width, height)
            faces=detector.detectMultiScale(frame,1.1,7)
            
            # converting color image into graycascale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Draw the rectangle around each face found in the faces object
            for (x, y, w, h) in faces:

                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) # red color frame

                # converting color image into gray scale
                roi_gray = gray[y:y+h, x:x+w] 

                roi_color = frame[y:y+h, x:x+w]

                # passing the converted grayscale into eye_cascade to detect the eyes in the face.
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)

                # applying green colored rectangle on eyes.
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            
            # converting to bytes
            frame = buffer.tobytes()

        # yield functions will set the content type and 
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# creating index route
@app.route('/')
def index():
    return render_template('index.html')

# creating video
@app.route('/video')
def video():
    # passing the video frames to HTML
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)