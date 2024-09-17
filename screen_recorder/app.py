from flask import Flask, jsonify, render_template
import cv2
import numpy as np
import pyautogui
import threading
import time

app = Flask(__name__)

# Global variables for controlling the recording state
is_recording = False
video_writer = None
FRAME_RATE = 10

# Define screen resolution
SCREEN_SIZE = pyautogui.size()

# Video writer settings
fourcc = cv2.VideoWriter_fourcc(*"XVID")


def start_recording():
    global is_recording, video_writer
    video_writer = cv2.VideoWriter("screen_recording.avi", fourcc, FRAME_RATE, SCREEN_SIZE)
    while is_recording:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video_writer.write(frame)
        time.sleep(1 / FRAME_RATE)
    video_writer.release()


@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend HTML


@app.route('/start', methods=['GET'])
def start():
    global is_recording
    if not is_recording:
        is_recording = True
        threading.Thread(target=start_recording).start()
        return jsonify({"status": "Recording started."})
    else:
        return jsonify({"status": "Already recording."})


@app.route('/stop', methods=['GET'])
def stop():
    global is_recording
    if is_recording:
        is_recording = False
        return jsonify({"status": "Recording stopped and video saved."})
    else:
        return jsonify({"status": "Not recording."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
