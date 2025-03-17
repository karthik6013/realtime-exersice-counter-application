import cv2
import numpy as np
from PoseModule import PoseDetector

# Initialize variables
cap = cv2.VideoCapture(0)
detector = PoseDetector()

correct_count = 0
direction = 0
hold_frames = 0  # Counts frames held in position
required_hold = 5  # Frames required to stabilize a position
exercise_started = False  # Tracks whether the exercise has started

# Colors and font settings
text_color = (255, 255, 255)
error_color = (0, 0, 255)
progress_start_color = (255, 140, 0)  # Orange start
progress_end_color = (50, 205, 50)  # Green end
font = cv2.FONT_HERSHEY_SIMPLEX

def draw_button(img, text, position, size, color, thickness=2, radius=20):
    """Draws a button with rounded corners and centered text."""
    overlay = img.copy()
    x, y = position
    w, h = size
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)
    cv2.putText(img, text, (x + 20, y + h - 15), font, 1, (255, 255, 255), thickness)

# Check if click is within button
def is_within_button(click, position, size):
    x, y = position
    w, h = size
    return x <= click[0] <= x + w and y <= click[1] <= y + h

# Mouse callback to check for button click
def mouse_callback(event, x, y, flags, param):
    global exercise_started
    if event == cv2.EVENT_LBUTTONDOWN:
        if is_within_button((x, y), (200, 250), (200, 100)):  # Button position and size
            exercise_started = True

cv2.namedWindow("Pull-Up Counter")
cv2.setMouseCallback("Pull-Up Counter", mouse_callback)

while True:
    success, img = cap.read()
    if not success:
        break

    if not exercise_started:
        # Display start screen
        img[:] = (0, 0, 0)  # Clear screen to black
        draw_button(img, "Start", (200, 250), (200, 100), (0, 128, 255))  # Draw start button
        cv2.putText(img, "Click 'Start' to begin", (150, 200), font, 1, text_color, 2)
    else:
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)

        if lmList:
            # Exercise counting logic
            frame_height, frame_width = img.shape[:2]
            in_frame = all(0 <= lm[1] <= frame_width and 0 <= lm[2] <= frame_height for lm in [lmList[11], lmList[12], lmList[23], lmList[24]])

            if in_frame:
                angle = detector.findAngle(img, 11, 13, 15)  # Shoulder, elbow, wrist
                if angle > 160:  # Arms extended
                    if direction == 0:
                        hold_frames += 1
                        if hold_frames >= required_hold:
                            direction = 1
                            hold_frames = 0
                    else:
                        hold_frames = 0
                elif angle < 60 and direction == 1:  # Arms pulled up
                    hold_frames += 1
                    if hold_frames >= required_hold:
                        correct_count += 1
                        direction = 0
                        hold_frames = 0
                else:
                    hold_frames = 0
                    cv2.putText(img, "Not in correct position", (50, 50), font, 1, error_color, 2)

                # Progress bar
                progress = int(np.interp(angle, [60, 160], [50, 400]))
                gradient_color = (
                    int(progress_start_color[0] + (progress_end_color[0] - progress_start_color[0]) * (progress / 400)),
                    int(progress_start_color[1] + (progress_end_color[1] - progress_start_color[1]) * (progress / 400)),
                    int(progress_start_color[2] + (progress_end_color[2] - progress_start_color[2]) * (progress / 400))
                )
                cv2.rectangle(img, (50, 50), (int(progress), 90), gradient_color, -1)

                # Stylish count display
                cv2.circle(img, (250, 400), 90, (0, 0, 0, 128), -1)
                cv2.circle(img, (250, 400), 100, text_color, 5)
                cv2.putText(img, f"{correct_count}", (215, 415), font, 2, text_color, 5)

            else:
                cv2.putText(img, "Person is outside camera view", (50, 50), font, 1, error_color, 2)
        else:
            cv2.putText(img, "Not in correct position", (50, 50), font, 1, error_color, 2)

    # Show the final image
    cv2.imshow("Pull-Up Counter", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 