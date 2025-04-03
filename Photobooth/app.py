from flask import Flask, render_template, Response, redirect, url_for
from camera import Camera

app = Flask(__name__)
camera = Camera()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mode')
def mode():
    return render_template('mode.html')

@app.route('/formal')
def formal():
    return render_template('formal.html')

@app.route('/casual')
def casual():
    return render_template('casual.html')

@app.route('/stop_camera')
def stop_camera():
    """ Stop the camera when leaving the capture page """
    camera.stop()
    return redirect(url_for('home'))  # Redirect to home or mode selection

def generate_frames():
    """ Generator function to stream video frames """
    camera.start()  # Make sure the camera starts before streaming
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    """ Route to stream the video feed """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
