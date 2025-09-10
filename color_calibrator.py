import cv2
import numpy as np

def nothing (x):
    pass

#open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Create a window with sliders to adjust the HSV values
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)  # Lower Hue
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)  # Lower Saturation
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)  # Lower Value
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing) # Upper Hue
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing) # Upper Saturation
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing) # Upper Value

# Set some initial values for a typical bright orange
cv2.setTrackbarPos("L - H", "Trackbars", 5)
cv2.setTrackbarPos("L - S", "Trackbars", 150)
cv2.setTrackbarPos("L - V", "Trackbars", 150)

print("\n--- INSTRUCTIONS ---")
print("1. Place your orange/or any other color sticker in front of the camera.")
print("2. Adjust the 'L' sliders up and the 'U' sliders down.")
print("3. Your goal is to make the sticker appear as a solid white shape in the 'Mask' window,")
print("   while the rest of the image is as black as possible.")
print("4. Once you are happy, write down the six L and U values.")
print("5. Press 'q' to quit.")
print("--------------------\n")

while True:
    ret, frame = cap.read()  # returns tuple of (status, frame)
    if not ret:
        break

    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the current slider positions
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Define the lower and upper bounds of the color to track
    lower_bound = np.array([l_h, l_s, l_v])
    upper_bound = np.array([u_h, u_s, u_v])

    # Create the mask
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Show the original frame and the mask
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
