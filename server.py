

import cv2
import numpy as np
from flask import Flask
from flask_socketio import SocketIO, emit
import base64
from PIL import Image
import io

# Initialize 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Configuration ---
LOWER_ORANGE = np.array([5, 150, 150])
UPPER_ORANGE = np.array([15, 255, 255])
print("Python server is starting...")

def base64_to_cv2_image(base64_string):
    if "," in base64_string:
        base64_string = base64_string.split(',')[1]
    img_bytes = base64.b64decode(base64_string)
    pil_image = Image.open(io.BytesIO(img_bytes))
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

@socketio.on('connect')
def handle_connect():
    print('Client connected!')

@socketio.on('update_hsv')
def handle_hsv_update(data):
    global LOWER_ORANGE, UPPER_ORANGE
    LOWER_ORANGE = np.array([data['lh'], data['ls'], data['lv']])
    UPPER_ORANGE = np.array([data['uh'], data['us'], data['uv']])

@socketio.on('image')
def handle_image(data):
    frame = base64_to_cv2_image(data)

    # Analysis Logic (same as analysis_headon.py)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_ORANGE, UPPER_ORANGE)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    found_coords = None

    if len(contours) > 0:
        best_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(best_contour)

        if area > 100:
            M = cv2.moments(best_contour)
            if M["m00"] != 0:
                cX = (M["m10"] / M["m00"])  #keeping it as float for more precision
                cY = (M["m01"] / M["m00"])
                found_coords = {'x': cX, 'y': cY}

    # Encode the mask to send to the frontend 
    # 1. Encode the mask image as a JPEG in memory
    _, buffer = cv2.imencode('.jpg', mask)
    # 2. Convert the buffered image to a Base64 string
    mask_base64 = base64.b64encode(buffer).decode('utf-8')

    # Send BOTH the coordinates and the mask back
    # The response is now a dictionary
    emit('response', {'coords': found_coords, 'mask': mask_base64})


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)