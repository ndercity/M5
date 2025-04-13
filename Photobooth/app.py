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

@app.route('/edit')
def edit():
    return render_template('edit.html')

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


@app.route('/capture_snapshot')
def capture_snapshot():
    # Call the capture_snapshot method from the Camera class
    snapshot = camera.capture_snapshot()
    if snapshot:
        # Send the snapshot to the client as a response
        return Response(snapshot, mimetype='image/jpeg')
    return 'Failed to capture snapshot', 500

@app.route('/save_casual', methods=['POST'])
def save_casual():
    if request.method == 'POST':
        # Implement your save logic here
        # Could save to filesystem or database
        return jsonify({"status": "success", "message": "Photos saved"})
    
    return jsonify({"status": "error", "message": "Invalid request"})

@app.route('/save_casual_layout', methods=['POST'])
def save_casual_layout():
    if request.method == 'POST':
        try:
            # Get the image data from the request
            images = request.files.getlist('images[]')
            layout_type = request.form.get('layout_type')
            
            # Process and save the images according to layout
            saved_paths = []
            for i, image in enumerate(images):
                filename = f"casual_{layout_type}_{i+1}_{int(time.time())}.jpg"
                save_path = os.path.join('static', 'saved', filename)
                image.save(save_path)
                saved_paths.append(save_path)
            
            # You could also create a combined image here
            return jsonify({
                'status': 'success',
                'message': 'Layout saved successfully',
                'paths': saved_paths
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

if __name__ == '__main__':
    app.run(debug=True)
