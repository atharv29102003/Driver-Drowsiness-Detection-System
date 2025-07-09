
# Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
# face_utils for basic operations of conversion
from imutils import face_utils
import serial
import time
import threading

#s = serial.Serial('COM7',9600)

# Initializing the face detector and landmark detector
hog_face_detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# status marking for current state
sleep = 0
drowsy = 0
active = 0
status=""
color=(0,0,0)

def compute(ptA,ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist

def blinked(a,b,c,d,e,f):
    up = compute(b,d) + compute(c,e)
    down = compute(a,f)
    ratio = up/(2.0*down)

    # Checking if it is blinked
    if(ratio>0.25):
        return 2
    elif(ratio>0.21 and ratio<=0.25):
        return 1
    else:
        return 0

# Function to continuously track the eye's position
def track_eye_position(landmarks):
    # Calculate the eye's position using the landmarks
    eye_position = (landmarks[36] + landmarks[39]) // 2
    return eye_position

# Function to draw a layout around the eyes
def draw_eye_layout(landmarks, frame):
    # Draw a polygon around the left eye
    left_eye_points = landmarks[36:42]
    cv2.polylines(frame, [left_eye_points], True, (0, 255, 0), 1)

    # Draw a polygon around the right eye
    right_eye_points = landmarks[42:48]
    cv2.polylines(frame, [right_eye_points], True, (0, 255, 0), 1)

# Multithreaded VideoCapture class
class VideoCapture:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

# Replace your existing VideoCapture instance with the new class
cap = VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = hog_face_detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_blink = blinked(landmarks[36],landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42],landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # Call the new function to track the eye's position
        eye_position = track_eye_position(landmarks)
        print(f"Eye Position: {eye_position}")

        # Call the new function to draw the eye layout
        draw_eye_layout(landmarks, frame)

        # Now judge what to do for the eye blinks
        if(left_blink==0 or right_blink==0):
            sleep+=1
            drowsy=0
            active=0
            if(sleep>6):
                #s.write(b'a')
                time.sleep(2)
                status="SLEEPING !!!"
                color = (0,0,255)

        elif(left_blink==1 or right_blink==1):
            sleep=0
            active=0
            drowsy+=1
            if(drowsy>6):
                #s.write(b'a')
                time.sleep(2)
                status="Drowsy !"
                color = (0,0,255)

        else:
            drowsy=0
            sleep=0
            active+=1
            if(active>6):
                #s.write(b'b')
                time.sleep(2)
                status="Active :)"
                color = (0,0,255)

        cv2.putText(frame, status, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)

        # Now, also show the eye's position on the frame
        cv2.putText(frame, f"Eye Position: {eye_position}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        for n in range(0, 68):
            (x,y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.cap.release()
cv2.destroyAllWindows()
