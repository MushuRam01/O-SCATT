# analysis_headon.py

import cv2
import numpy as np

# --- Configuration ---
LOWER_ORANGE = np.array([5, 150, 150])
UPPER_ORANGE = np.array([15, 255, 255])
VIDEO_SOURCE = "my_headon_video.mp4"

# --- Main Program ---
cap = cv2.VideoCapture(VIDEO_SOURCE)
if not cap.isOpened():
    print(f"Error: Could not open video file at {VIDEO_SOURCE}")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_ORANGE, UPPER_ORANGE)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        best_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(best_contour)

        if area > 100:
            M = cv2.moments(best_contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                cv2.circle(frame, (cX, cY), 10, (0, 0, 255), -1)
                cv2.putText(frame, f"({cX}, {cY})", (cX + 15, cY + 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Sticker Tracking", frame)
    cv2.imshow("Mask", mask) 

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()