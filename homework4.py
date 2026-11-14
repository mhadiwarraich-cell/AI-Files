
import cv2
import numpy as np

# Start webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Webcam not found!")
    exit()

print("REAL-TIME COLOR FILTERS AND EDGE DETECTION")
print("------------------------------------------")
print("Press 0 = Normal Camera")
print("Press 1 = Red Filter")
print("Press 2 = Green Filter")
print("Press 3 = Blue Filter")
print("Press 4 = Grayscale")
print("Press 5 = Canny Edge Detection")
print("Press 6 = Sobel Edge Detection")
print("Press 7 = Laplacian Edge Detection")
print("Press Q = Quit")

while True:

    ret, frame = camera.read()

    if not ret:
        print("Unable to read webcam")
        break

    # Resize camera frame
    frame = cv2.resize(frame, (640, 480))

    # Create a copy of the original image
    output = frame.copy()

    # Read keyboard input
    key = cv2.waitKey(1) & 0xFF

    # Normal camera
    if key == ord('0'):
        output = frame.copy()

    # Red colour filter
    elif key == ord('1'):
        output = frame.copy()
        output[:, :, 0] = 0
        output[:, :, 1] = 0

    # Green colour filter
    elif key == ord('2'):
        output = frame.copy()
        output[:, :, 0] = 0
        output[:, :, 2] = 0

    # Blue colour filter
    elif key == ord('3'):
        output = frame.copy()
        output[:, :, 1] = 0
        output[:, :, 2] = 0

    # Grayscale filter
    elif key == ord('4'):
        gray = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY
        )
        output = cv2.cvtColor(
            gray, cv2.COLOR_GRAY2BGR
        )

    # Canny edge detection
    elif key == ord('5'):
        gray = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY
        )
        output = cv2.Canny(gray, 100, 200)
        output = cv2.cvtColor(
            output, cv2.COLOR_GRAY2BGR
        )

    # Sobel edge detection
    elif key == ord('6'):
        gray = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY
        )
        sobel_x = cv2.Sobel(
            gray, cv2.CV_64F, 1, 0, ksize=3
        )
        sobel_y = cv2.Sobel(
            gray, cv2.CV_64F, 0, 1, ksize=3
        )

        sobel = cv2.magnitude(
            sobel_x, sobel_y
        )

        sobel = cv2.convertScaleAbs(sobel)
        output = cv2.cvtColor(
            sobel, cv2.COLOR_GRAY2BGR
        )

    # Laplacian edge detection
    elif key == ord('7'):
        gray = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY
        )

        laplacian = cv2.Laplacian(
            gray, cv2.CV_64F
        )

        laplacian = cv2.convertScaleAbs(
            laplacian
        )

        output = cv2.cvtColor(
            laplacian, cv2.COLOR_GRAY2BGR
        )

    # Quit program
    elif key == ord('q'):
        break

    # Display output
    cv2.imshow(
        "Real-Time Color Filters and Edge Detection",
        output
    )

# Release webcam
camera.release()
cv2.destroyAllWindows()

print("Program closed successfully!")
