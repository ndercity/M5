from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from camera import Camera
from color_filter import Color_Filter
import os
app = Flask(__name__)
camera = Camera()
color_filter = Color_Filter()

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

@app.route('/get_image_edit',  methods=['POST'])
def get_image_edit():
    image_file = request.files.get('image')

    if not image_file:
        print("error 1")
        return jsonify({"error": "No image file received"}), 400
    try:
        color_filter.set_image_to_edit(image_file)
        print("good ito")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("may mali")
        return jsonify({"status": "error", "message": str(e)}), 500
   
@app.route('/get_raw')
def get_raw():
    raw_image = color_filter.return_raw()
    if raw_image:
        return Response(raw_image, mimetype='image/jpeg')
    return 'Failed to capture raw', 600

@app.route('/get_grayscaled')
def get_grayscale():
    grayscale = color_filter.grayscale_image()
    if grayscale:
        return Response(grayscale, mimetype='image/jpeg')
    return 'Failed to capture grayscale', 600

@app.route('/get_sepia')
def get_sepia():
    sepia = color_filter.sepia_image()
    if sepia:
        return Response(sepia, mimetype='image/jpeg')
    return 'Failed to capture sepia', 600

@app.route('/get_inverted')
def get_inverted():
    inverted = color_filter.inverted_image()
    if inverted:
        return Response(inverted, mimetype='image/jpeg')
    return 'Failed to capture inverted', 600

@app.route('/get_sketched')
def get_sketched():
    sketched = color_filter.sketch_image()
    if sketched:
        return Response(sketched, mimetype='image/jpeg')
    return 'Failed to capture sketched', 600

@app.route('/get_warm')
def get_warm():
    warm = color_filter.warm_image()
    if warm:
        return Response(warm, mimetype='image/jpeg')
    return 'Failed to capture warm', 600

@app.route('/get_blue')
def get_blue():
    blue = color_filter.cool_blue_image()
    if blue:
        return Response(blue, mimetype='image/jpeg')
    return 'Failed to capture blue', 600

@app.route('/get_bright')
def get_bright():
    bright = color_filter.bright_image()
    if bright:
        return Response(bright, mimetype='image/jpeg')
    return 'Failed to capture bright', 600

@app.route('/get_cartoon')
def get_cartoon():
    cartoon = color_filter.cartoon_image()
    if cartoon:
        return Response(cartoon, mimetype='image/jpeg')
    return 'Failed to capture cartoon', 600

@app.route('/get_green')
def get_green():
    green = color_filter.green_vibe_image()
    if green:
        return Response(green, mimetype='image/jpeg')
    return 'Failed to capture green vibe', 600

# Test Dynamic stickers
@app.route("/api/stickers")
def get_stickers():
    sticker_dir = os.path.join(app.static_folder, 'stickers')
    sticker_files = [f for f in os.listdir(sticker_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return jsonify(sticker_files)

if __name__ == '__main__':
    app.run(debug=True)
