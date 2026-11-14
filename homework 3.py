
import cv2
import numpy as np

# Start webcam
camera = cv2.VideoCapture(0)

# Create drawing canvas
canvas = None

# Store previous hand position
previous_x = 0
previous_y = 0

print("GESTURE CONTROL USING OPENCV")
print("----------------------------")
print("Move hand - Move circle and draw")
print("C - Clear drawing")
print("Q - Quit")

while True:

    # Read webcam
    success, frame = camera.read()

    if not success:
        print("Webcam not found!")
        break

    # Flip camera
    frame = cv2.flip(frame, 1)

    # Create canvas
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Convert image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Set skin colour range
    lower = np.array([0, 20, 70])
    upper = np.array([20, 255, 255])

    # Apply colour filtering
    mask = cv2.inRange(hsv, lower, upper)

    # Remove noise
    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN, kernel
    )

    # Find contours
    contours, hierarchy = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Detect largest hand-like region
    if len(contours) > 0:

        hand = max(contours, key=cv2.contourArea)

        if cv2.contourArea(hand) > 1500:

            # Find hand position
            x, y, w, h = cv2.boundingRect(hand)

            center_x = x + w // 2
            center_y = y + h // 2

            # Draw rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Draw circle
            cv2.circle(
                frame,
                (center_x, center_y),
                15,
                (0, 0, 255),
                -1
            )

            # Draw line following hand
            if previous_x != 0:
                cv2.line(
                    canvas,
                    (previous_x, previous_y),
                    (center_x, center_y),
                    (255, 0, 0),
                    5
                )

            previous_x = center_x
            previous_y = center_y

    else:
        previous_x = 0
        previous_y = 0

    # Combine canvas and webcam
    output = cv2.add(frame, canvas)

    # Display information
    cv2.putText(
        output,
        "Gesture Control",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Show output
    cv2.imshow("Gesture Control", output)
    cv2.imshow("Hand Detection", mask)

    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        canvas = np.zeros_like(frame)
        previous_x = 0
        previous_y = 0

    elif key == ord('q'):
        break

# Close webcam
camera.release()
cv2.destroyAllWindows()

print("Gesture control stopped!")
