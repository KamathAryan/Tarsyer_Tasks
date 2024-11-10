#Used Mediapipe library for finger recognition.
import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize the Tkinter window, creating a GUI with video shown on left half and output shown on right half
root = tk.Tk()
root.title("Finger Tracking")

# Create a label for the video feed 
video_label = tk.Label(root)
video_label.pack(side="left")

# Create a canvas to display the alphabet 
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack(side="right")

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Set the resolution of the webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set the width to 640 pixels
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set the height to 480 pixels

# Finger to alphabet mapping 
finger_gestures = {
    1: "I",  # Index finger
    2: "M",  # Middle finger
    3: "R",  # Ring finger
    4: "T",  # Thumb
    5: "B",  # Pinky finger (baby finger)
}

# Function to calculate distance
def calculate_distance(p1, p2):
    return np.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

# Function to detect fingers and recognize gestures based on distance
def get_finger_gesture(landmarks):
    raised_fingers = []

    # Finger base and tip landmarks for each finger
    fingers = {
        "thumb": (landmarks[1], landmarks[4]),    # Base: 1, Tip: 4
        "index": (landmarks[5], landmarks[8]),    # Base: 5, Tip: 8
        "middle": (landmarks[9], landmarks[12]),  # Base: 9, Tip: 12
        "ring": (landmarks[13], landmarks[16]),   # Base: 13, Tip: 16
        "pinky": (landmarks[17], landmarks[20])   # Base: 17, Tip: 20
    }

    # Dictionary to store the distances and corresponding raised fingers
    finger_distances = {}

    # Calculate distances and check if fingers are raised
    for finger, (base, tip) in fingers.items():
        distance = calculate_distance(base, tip)
        if distance > 0.2: 
            # Map the finger to a number
            if finger == "thumb":
                finger_distances[4] = distance  # Thumb raised
            elif finger == "index":
                finger_distances[1] = distance  # Index finger raised
            elif finger == "middle":
                finger_distances[2] = distance  # Middle finger raised
            elif finger == "ring":
                finger_distances[3] = distance  # Ring finger raised
            elif finger == "pinky":
                finger_distances[5] = distance  # Pinky raised

    # If there are raised fingers, find the one with the maximum distance (highest confidence)
    if finger_distances:
        # Get the finger with the highest confidence (maximum distance)
        best_finger = max(finger_distances, key=finger_distances.get)
        return finger_gestures.get(best_finger, "")
    
    return ""

# Function to update the video feed and detect gestures
def update_frame():
    ret, frame = cap.read()
    if ret:
        # reduced resolution to speed up processing
        frame = cv2.resize(frame, (320, 240))  

        # Flip the frame for a mirror view
        frame = cv2.flip(frame, 1)
        
        # Convert frame to RGB (only once per frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_height, frame_width, _ = frame_rgb.shape
        
        # Process the frame with MediaPipe Hand detection
        results = hands.process(frame_rgb)

        # If hands are found, extract landmarks and detect the gesture
        gesture = ""
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                gesture = get_finger_gesture(landmarks.landmark)

                # Draw the hand landmarks on the frame
                mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the finger
        canvas.delete("all")
        canvas.create_text(200, 200, text=gesture, font=("Helvetica", 50, "bold"), fill="black")

        # Convert the frame to Image for Tkinter display
        img = Image.fromarray(frame_rgb)
        img = ImageTk.PhotoImage(img)

        video_label.config(image=img)
        video_label.image = img

    root.after(30, update_frame)

update_frame()

root.mainloop()

cap.release()
