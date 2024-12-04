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
            # encodes the image into a buffer
            ret, buffer = cv2.imencode('.jpg', frame)

            # converting the buffer back to bytes
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