import cv2
import numpy as np
from PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
detector = PoseDetector()

correct_count = 0
direction = 0
hold_frames = 0
required_hold = 5
exercise_started = False

text_color = (255, 255, 255)
error_color = (0, 0, 255)
font = cv2.FONT_HERSHEY_SIMPLEX

def draw_button(img, text, position, size, color, thickness=2):
    overlay = img.copy()
    x, y = position
    w, h = size
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)
    cv2.putText(img, text, (x + 20, y + h - 15), font, 1, (255, 255, 255), thickness)

def is_within_button(click, position, size):
    x, y = position
    w, h = size
    return x <= click[0] <= x + w and y <= click[1] <= y + h

def mouse_callback(event, x, y, flags, param):
    global exercise_started
    if event == cv2.EVENT_LBUTTONDOWN:
        if is_within_button((x, y), (200, 250), (200, 100)):
            exercise_started = True

cv2.namedWindow("Deadlift Counter")
cv2.setMouseCallback("Deadlift Counter", mouse_callback)

while True:
    success, img = cap.read()
    if not success:
        break

    if not exercise_started:
        img[:] = (0, 0, 0)
        draw_button(img, "Start", (200, 250), (200, 100), (0, 128, 255))
        cv2.putText(img, "Click 'Start' to begin", (150, 200), font, 1, text_color, 2)
    else:
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)

        if lmList:
            angle = detector.findAngle(img, 23, 25, 27)  # Hip, knee, ankle
            if angle > 160:  # Standing position
                if direction == 0:
                    hold_frames += 1
                    if hold_frames >= required_hold:
                        direction = 1
                        hold_frames = 0
                else:
                    hold_frames = 0
            elif angle < 80 and direction == 1:  # Lowered position
                hold_frames += 1
                if hold_frames >= required_hold:
                    correct_count += 1
                    direction = 0
                    hold_frames = 0
            else:
                hold_frames = 0
                cv2.putText(img, "Not in correct position", (50, 50), font, 1, error_color, 2)

            cv2.putText(img, f"Deadlifts: {correct_count}", (50, 100), font, 1, text_color, 2)

        else:
            cv2.putText(img, "Not in correct position", (50, 50), font, 1, error_color, 2)

    cv2.imshow("Deadlift Counter", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
