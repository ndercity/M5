from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from camera import Camera
from color_filter import Color_Filter
from sticker_filter import Sticker_Filter
import os
import time
import uuid
from db_functions import get_db, init_db, close_connection, insert_photo_session, update_photo_blob
import base64
import io
from session_flow import start_photo_session, finalize_session

app = Flask(__name__)
#---------
with app.app_context():
    init_db()
app.teardown_appcontext(close_connection)
#---------
camera = Camera()
color_filter = Color_Filter()
sticker_filter = Sticker_Filter()

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
        
#################################################################
@app.route('/capture_image')
def capture_image():
    camera.start()
    image = camera.capture_frame()
    return Response(image, mimetype='image/jpeg')

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


@app.route('/get_image_sticker' , methods=['POST'])
def get_sticker_filter():
    image_file = request.files.get('image')

    if not image_file:
        print("error 1")
        return jsonify({"error": "No image file received"}), 400
    try:
        sticker_filter.get_image_sticker(image_file)
        print("good ito")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("may mali sa sticker")
        return jsonify({"status": "error", "message": str(e)}), 500   
         
@app.route('/set_face_boxes')
def set_face_boxes():
    boxes, image = sticker_filter.set_face_boxes()
    return jsonify({
        "boxes": boxes,
    })

@app.route('/clear_boxes')
def clear_boxes():
    sticker_filter.clear_all()
    return jsonify({"status": "cleared"}), 200

@app.route('/set_face_index', methods=['POST'])
def set_face_index():
    index = request.form.get('faceIndex')
    sticker_type = request.form.get('stickerType')
    if not index or not sticker_type:
        return jsonify({"status": "error", "message": "No Index Received"}), 400
    sticker_filter.set_face_index(index, sticker_type)
    return jsonify({"status": "cleared"}), 200

@app.route('/get_warped_sticker')
def get_warped_sticker():
    overlay = sticker_filter.warp_image()
    if overlay is not None:
        x, y, w, h = sticker_filter.get_overlay_bounding_box()
        base64_sticker = base64.b64encode(overlay).decode('utf-8')
        print("data sent: ", x, y, w, h)
        return jsonify({
            "sticker": base64_sticker,
            "x": x,
            "y": y,
            "width": w,
            "height": h        
        })

    return jsonify({"status": "error", "message": "No overlay given"}), 500


# For the page before proceeding to tutorial [ email confirmation ]
@app.route('/start_session', methods=['POST'])
def start_session():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"error": "Email is required"}), 400

    email = data['email']
    session_id = start_photo_session(email)
    return jsonify({"session_id": session_id})

# Finalization
@app.route('/finalize_session', methods=['POST'])
def finalize_session_route():
    session_id = request.form.get('session_id')
    if not session_id:
        return jsonify({"status": "error", "message": "Session ID required"}), 400
    
    success = finalize_session(session_id)
    if success:
        return jsonify({"status": "sent"}), 200
    else:
        return jsonify({"status": "failed"}), 500
    
#Upload photo to db
@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    session_id = request.form.get('session_id')
    photo_file = request.files.get('photo')

    if not session_id or not photo_file:
        return jsonify({"error": "Missing session_id or photo file"}), 400

    photo_blob = photo_file.read()

    try:
        update_photo_blob(session_id, photo_blob)
        return jsonify({"message": "Photo saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#TEST insert
@app.route('/test_insert_session')
def test_insert_session():
    email = "testuser@example.com"
    pdf_data = b"%PDF-1.4 dummy pdf binary data"
    session_id = str(uuid.uuid4())

    inserted_session_id = insert_photo_session(email, pdf_data, status="pending", session_id=session_id)

    # Verify insertion by querying DB
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT email, status, session_id FROM photo_sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()

    if row:
        return jsonify({
            "message": "Test session inserted successfully",
            "email": row[0],
            "status": row[1],
            "session_id": row[2]
        })
    else:
        return jsonify({"message": "Failed to retrieve inserted session"}), 500

#if using python app.py
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

