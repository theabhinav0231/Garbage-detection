from flask import Flask, Response, render_template, jsonify, request
from ultralytics import YOLO
import cv2 as cv
import cvzone
from collections import deque
import time
import json
import os
import numpy as np
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Load YOLOv8 model and define class names
model = YOLO("best.pt")
class_names = model.names

# Define classes of interest and confidence threshold
target_classes = ["garbage", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"]
confidence_threshold = 0.3

# Global statistics object to keep track of detections
class DetectionStats:
    def __init__(self):
        # Total detections count
        self.total_detections = 0
        
        # Queue to store the last 10 detection events
        self.detection_history = deque(maxlen=10)
        
        # Count of detections per class
        self.class_counts = {cls: 0 for cls in target_classes}
        
        # Average confidence score
        self.avg_confidence = 0
        
        # Recording-related variables
        self.is_recording = False
        self.video_writer = None
        self.recording_start_time = None
        
        # Counter for screenshots
        self.screenshot_counter = 0

# Create an instance of the detection statistics
stats = DetectionStats()

# Directory for saving media (screenshots, recordings)
UPLOAD_FOLDER = 'static/captures'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to update detection statistics
def update_detection_stats(detection_class, confidence):
    stats.total_detections += 1
    stats.class_counts[detection_class] = stats.class_counts.get(detection_class, 0) + 1

    # Add the detection to history with a timestamp
    timestamp = datetime.now().strftime("%H:%M:%S")
    stats.detection_history.appendleft({
        'class': detection_class,
        'confidence': confidence,
        'timestamp': timestamp
    })
    
    # Calculate the average confidence score
    confidences = [d['confidence'] for d in stats.detection_history]
    stats.avg_confidence = sum(confidences) / len(confidences) if confidences else 0

# Function to generate video frames for the live stream
def generate_frames():
    # Open the video file
    video_capture = cv.VideoCapture("./video/garbage_test_2.mp4")
    frame_counter = 0
    
    while True:
        success, image = video_capture.read()
        if not success:
            break
            
        frame_counter += 1
        current_frame = image.copy()

        # Run YOLOv8 inference on the current frame
        results = model(current_frame, stream=True)
        frame_detections = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Extract bounding box coordinates and confidence
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w, h = x2 - x1, y2 - y1
                confidence = round(float(box.conf[0]), 2)
                class_id = int(box.cls[0])
                current_class = class_names[class_id]

                # Check if the detection meets the criteria
                if current_class in target_classes and confidence >= confidence_threshold:
                    # Draw bounding box and label on the frame
                    cvzone.putTextRect(current_frame, f"{current_class} | {confidence}",
                                     (max(0, x1), max(35, y1)), scale=1, thickness=1, offset=3)
                    cvzone.cornerRect(current_frame, (x1, y1, w, h), l=9)
                    
                    # Update detection statistics
                    update_detection_stats(current_class, confidence)
                    frame_detections.append({
                        'class': current_class,
                        'confidence': confidence
                    })

        # Record video if recording is enabled
        if stats.is_recording and stats.video_writer:
            stats.video_writer.write(current_frame)

        # Encode the frame as a JPEG image
        _, buffer = cv.imencode('.jpg', current_frame)
        frame = buffer.tobytes()

        # Yield the frame to be served in the response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video_capture.release()
    if stats.video_writer:
        stats.video_writer.release()

# Define the main index route
@app.route('/')
def index():
    return render_template('index.html')

# Route for the live video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to fetch detection statistics
@app.route('/get_stats')
def get_stats():
    return jsonify({
        'total_detections': stats.total_detections,
        'detection_history': list(stats.detection_history),
        'class_counts': stats.class_counts,
        'avg_confidence': round(stats.avg_confidence * 100, 1),
        'is_recording': stats.is_recording
    })

# Route to capture a screenshot
@app.route('/capture_screenshot', methods=['POST'])
def capture_screenshot():
    video_capture = cv.VideoCapture("./video/garbage_test_2.mp4")
    success, frame = video_capture.read()
    if success:
        stats.screenshot_counter += 1
        filename = f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        cv.imwrite(filepath, frame)
        video_capture.release()
        return jsonify({'success': True, 'filename': filename})
    video_capture.release()
    return jsonify({'success': False, 'error': 'Failed to capture screenshot'})

# Route to toggle video recording
@app.route('/toggle_recording', methods=['POST'])
def toggle_recording():
    if not stats.is_recording:
        # Start recording
        filename = f'recording_{datetime.now().strftime("%Y%m%d_%H%M%S")}.avi'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        video_capture = cv.VideoCapture("./video/garbage_test_2.mp4")
        frame_width = int(video_capture.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_capture.get(cv.CAP_PROP_FRAME_HEIGHT))
        video_capture.release()
        
        stats.video_writer = cv.VideoWriter(
            filepath,
            cv.VideoWriter_fourcc(*'XVID'),
            20.0, (frame_width, frame_height)
        )
        stats.is_recording = True
        stats.recording_start_time = time.time()
        return jsonify({'success': True, 'action': 'started'})
    else:
        # Stop recording
        if stats.video_writer:
            stats.video_writer.release()
            stats.video_writer = None
        stats.is_recording = False
        return jsonify({'success': True, 'action': 'stopped'})

# Route to update detection settings
@app.route('/update_settings', methods=['POST'])
def update_settings():
    global confidence_threshold
    data = request.get_json()
    
    if 'confidence_threshold' in data:
        confidence_threshold = float(data['confidence_threshold'])
    
    if 'target_classes' in data:
        target_classes = data['target_classes']
    
    return jsonify({
        'success': True,
        'current_settings': {
            'confidence_threshold': confidence_threshold,
            'target_classes': target_classes
        }
    })

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
