
import cv2
import numpy as np

# Start webcam
camera = cv2.VideoCapture(0)

canvas = None


previous_point = None


circle_x = 320
circle_y = 240


lower_color = np.array([0, 20, 70])
upper_color = np.array([20, 255, 255])

print("GESTURE CONTROL APPLICATION")
print("---------------------------")
print("Move hand - Move circle")
print("Hold hand in view - Draw lines")
print("Press C - Clear drawing")
print("Press Q - Quit")

while True:

   
    success, frame = camera.read()

    if not success:
        print("Webcam not found!")
        break

    # Flip camera
    frame = cv2.flip(frame, 1)

   
    if canvas is None:
        canvas = np.zeros_like(frame)

   
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   
    mask = cv2.inRange(hsv, lower_color, upper_color)

   
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN, kernel
    )

   
        mask, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) > 0:

        hand = max(contours, key=cv2.contourArea)

        if cv2.contourArea(hand) > 1500:

          
            x, y, w, h = cv2.boundingRect(hand)

            circle_x = x + w // 2
            circle_y = y + h // 2

            current_point = (circle_x, circle_y)

           
            if previous_point is not None:
                cv2.line(
                    canvas,
                    previous_point,
                    current_point,
                    (0, 255, 0),
                    5
                )

            previous_point = current_point

          
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

           
            cv2.putText(
                frame,
                "Hand Detected",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    else:
        previous_point = None

    
    cv2.circle(
        frame,
        (circle_x, circle_y),
        25,
        (0, 0, 255),
        -1
    )

  
    output = cv2.add(frame, canvas)

   
    cv2.imshow("Gesture Control", output)
    cv2.imshow("Hand Detection Mask", mask)

   
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        canvas = np.zeros_like(frame)
        previous_point = None

    elif key == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()
