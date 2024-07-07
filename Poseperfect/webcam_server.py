# from flask import Flask, render_template, Response
# import cv2
# import pyttsx3
# import threading
# import mediapipe as mp
# import numpy as np
# import queue


# app = Flask(__name__)

# # Initialize MediaPipe Pose and drawing utilities
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

# # Initialize speech engine
# voice = pyttsx3.init()
# voice.setProperty('rate', 150)

# # Initialize global variables
# alert_queue = queue.Queue()
# prev_alert = None
# lock = threading.Lock()

# # Speech synthesis worker
# def speak_worker():
#     while True:
#         alert = alert_queue.get()
#         if alert is None:  # Stop signal
#             break
#         with lock:
#             voice.say(alert)
#             voice.runAndWait()

# speech_thread = threading.Thread(target=speak_worker)
# speech_thread.daemon = True
# speech_thread.start()

# # Function to calculate angle between three points
# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)
#     radians = np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)
#     return angle

# # Generate frames for video feed
# def generate_frames():
#     global prev_alert

#     cap = cv2.VideoCapture(0)
#     with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 print("Failed to capture image")
#                 continue

#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False

#             results = pose.process(image)

#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             try:
#                 if results.pose_landmarks is None:
#                     print("No pose landmarks detected")
#                     continue

#                 landmarks = results.pose_landmarks.landmark
#                 Lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
#                 Lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
#                 Lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
#                 Lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
#                 Lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
#                 Lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

#                 Rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
#                 Relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
#                 Rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
#                 Rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
#                 Rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
#                 Rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

#                 angle1 = 180 - calculate_angle(Lshoulder, Lelbow,0)
#                 angle2 = calculate_angle(Rshoulder, Relbow,0)
#                 angle3 = calculate_angle(Lhip, Lknee,0)
#                 angle4 = 90 + calculate_angle(Rhip, Rknee,0)

#                 alert = None

#                 if angle1 > 20 or angle2 > 20:
#                     alert = 'Please, raise your hands upwards'
#                 elif angle4 > 135:
#                     alert = 'Please, bend your right knee.'
#                 else:
#                     alert = 'Perfect, you are doing great.'

#                 if alert != prev_alert:
#                     alert_queue.put(alert)
#                     prev_alert = alert

#                 cv2.putText(image, alert, (24, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

#                 cv2.putText(image, str(angle1), tuple(np.multiply(Lshoulder, [850, 480]).astype(int)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#                 cv2.putText(image, str(angle2), tuple(np.multiply(Rshoulder, [850, 480]).astype(int)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#                 cv2.putText(image, str(angle3), tuple(np.multiply(Lankle, [850, 480]).astype(int)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#                 cv2.putText(image, str(angle4), tuple(np.multiply(Rknee, [850, 480]).astype(int)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

#             except Exception as e:
#                 print(f"Error: {e}")

#             mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                       mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
#                                       mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=4, circle_radius=3))
#             ret, buffer = cv2.imencode('.jpg', image)
#             frame = buffer.tobytes()

#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     cap.release()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, Response
import cv2
import pyttsx3
import threading
import mediapipe as mp
import numpy as np
import queue


app = Flask(__name__)

# Initialize MediaPipe Pose and drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize speech engine
voice = pyttsx3.init()
voice.setProperty('rate', 150)

# Initialize global variables
alert_queue = queue.Queue()
prev_alert = None
lock = threading.Lock()

# Speech synthesis worker
def speak_worker():
    while True:
        alert = alert_queue.get()
        if alert is None:  # Stop signal
            break
        with lock:
            voice.say(alert)
            voice.runAndWait()

speech_thread = threading.Thread(target=speak_worker)
speech_thread.daemon = True
speech_thread.start()

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return angle

# Generate frames for video feed
def generate_frames():
    global prev_alert

    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                continue

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                if results.pose_landmarks is None:
                    print("No pose landmarks detected")
                    continue

                landmarks = results.pose_landmarks.landmark
                Lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                Lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                Lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                Lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                Lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                Lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                Rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                Relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                Rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                Rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                Rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                Rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                angle1 = 180 - calculate_angle(Lshoulder, Lelbow,0)
                angle2 = calculate_angle(Rshoulder, Relbow,0)
                angle3 = calculate_angle(Lhip, Lknee,0)
                angle4 = 90 + calculate_angle(Rhip, Rknee,0)

                alert = None

                if angle1 > 20 or angle2 > 20:
                    alert = 'Please, raise your hands upwards'
                elif angle4 > 135:
                    alert = 'Please, bend your right knee.'
                else:
                    alert = 'Perfect, you are doing great.'

                if alert != prev_alert:
                    alert_queue.put(alert)
                    prev_alert = alert

                cv2.putText(image, alert, (24, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

                cv2.putText(image, str(angle1), tuple(np.multiply(Lshoulder, [850, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(angle2), tuple(np.multiply(Rshoulder, [850, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(angle3), tuple(np.multiply(Lankle, [850, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(angle4), tuple(np.multiply(Rknee, [850, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            except Exception as e:
                print(f"Error: {e}")

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=4, circle_radius=3))
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
