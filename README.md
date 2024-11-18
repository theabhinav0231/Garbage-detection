Smart Garbage Detection System
A real-time object detection system specifically designed for garbage detection and monitoring, built with Flask, OpenCV, and YOLOv8. The system provides live video analysis, detection statistics, and recording capabilities.
Features

Real-time object detection using YOLOv8
Live video feed processing
Detection statistics and analytics
Recording capabilities
Screenshot capture
Customizable detection settings
Interactive web interface
Detection history tracking
Real-time confidence scoring
Dynamic detection visualization

Prerequisites

Python 3.8+
pip (Python package manager)
Web browser with JavaScript enabled
Webcam or video input device (optional - can use video files)

Installation

Clone the repository:

bashCopygit clone https://github.com/yourusername/smart-garbage-detection.git
cd smart-garbage-detection

Create and activate a virtual environment (recommended):

bashCopypython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install required packages:

bashCopypip install -r requirements.txt
Required Packages
textCopyflask
opencv-python
ultralytics
cvzone
numpy

Download the YOLOv8 model:
Place your trained YOLOv8 model file (best.pt) in the project root directory.

Project Structure
Copysmart-garbage-detection/
├── static/
│   └── captures/         # Screenshot and recording storage
├── templates/
│   └── index.html        # Web interface template
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
Configuration
Model Settings
The system is configured to detect the following classes:

Garbage
Bird
Cat
Dog
Horse
Sheep
Cow
Elephant
Bear
Zebra
Giraffe

You can modify the target classes and confidence threshold in the application settings.
Video Source
By default, the system uses "garbage_test_2.mp4" as the video source. To use a different video source:

For webcam: Change cv.VideoCapture("garbage_test_2.mp4") to cv.VideoCapture(0)
For different video file: Replace "garbage_test_2.mp4" with your video file path

Usage

Start the Flask server:

bashCopypython app.py

Open a web browser and navigate to:

Copyhttp://localhost:5000
Web Interface Features

Live Feed: Displays real-time video with detection overlays
Screenshot: Capture current frame
Recording: Start/stop video recording
Settings: Adjust detection parameters

Confidence threshold
Target classes selection


Statistics Panel:

Total detections
Average confidence
Detection history
Real-time charts



Keyboard Shortcuts

ESC: Close settings modal
Space: Start/Stop recording (when video feed is focused)

API Endpoints

/: Main web interface
/video_feed: Streams processed video feed
/get_stats: Returns current detection statistics
/capture_screenshot: Captures current frame
/toggle_recording: Toggles video recording
/update_settings: Updates detection settings

Customization
Styling
The interface uses a custom CSS framework with variables for easy customization:
cssCopy:root {
    --primary-color: #2ecc71;
    --secondary-color: #27ae60;
    --accent-color: #e74c3c;
    --dark-color: #2c3e50;
    --light-color: #ecf0f1;
}
Detection Parameters
Default confidence threshold: 0.3
To modify:

Open settings in web interface
Adjust slider
Save changes

Troubleshooting
Common issues and solutions:

Video feed not loading

Check video source path
Verify camera permissions
Ensure OpenCV is properly installed


Recording fails

Check write permissions in captures directory
Verify available disk space
Ensure video codec support


Detection not working

Verify model file presence
Check CUDA/GPU support
Adjust confidence threshold



Performance Optimization
For better performance:

Use GPU acceleration if available
Adjust frame processing resolution
Optimize confidence threshold
Limit target classes to necessary ones

Contributing

Fork the repository
Create feature branch
Commit changes
Push to branch
Create Pull Request

License
MIT License
Contact
Your Name - your.email@example.com
Project Link: https://github.com/yourusername/smart-garbage-detection
Acknowledgments

YOLOv8 Team
OpenCV Community
Flask Framework
Chart.js Team

Future Improvements

 Multiple camera support
 Cloud storage integration
 Advanced analytics dashboard
 Email/SMS alerts
 Mobile app integration
 Custom model training interface
