
import cv2
import numpy as np

# Start webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Webcam not found!")
    exit()

# Original mode
mode = "original"

print("IMAGE PROCESSING APPLICATION")
print("----------------------------")
print("0 - Original Image")
print("1 - Red Filter")
print("2 - Green Filter")
print("3 - Blue Filter")
print("4 - Canny Edge Detection")
print("5 - Sobel Edge Detection")
print("6 - Laplacian Edge Detection")
print("S - Save Image")
print("Q - Quit")

while True:

    # Read webcam frame
    success, frame = camera.read()

    if not success:
        print("Cannot read webcam!")
        break

    # Create a copy
    result = frame.copy()

    # Convert image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply selected colour filter
    if mode == "red":
        result[:, :, 0] = 0
        result[:, :, 1] = 0

    elif mode == "green":
        result[:, :, 0] = 0
        result[:, :, 2] = 0

    elif mode == "blue":
        result[:, :, 1] = 0
        result[:, :, 2] = 0

    # Canny edge detection
    elif mode == "canny":
        edges = cv2.Canny(gray, 100, 200)
        result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Sobel edge detection
    elif mode == "sobel":
        x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        edges = cv2.magnitude(x, y)
        edges = cv2.convertScaleAbs(edges)

        result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Laplacian edge detection
    elif mode == "laplacian":
        edges = cv2.Laplacian(gray, cv2.CV_64F)
        edges = cv2.convertScaleAbs(edges)

        result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Display current mode
    cv2.putText(
        result,
        "Mode: " + mode,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Show processed image
    cv2.imshow("Image Processing Application", result)

    # Get keyboard input
    key = cv2.waitKey(1) & 0xFF

    # Change colour filters
    if key == ord('0'):
        mode = "original"

    elif key == ord('1'):
        mode = "red"

    elif key == ord('2'):
        mode = "green"

    elif key == ord('3'):
        mode = "blue"

    # Change edge detection
    elif key == ord('4'):
        mode = "canny"

    elif key == ord('5'):
        mode = "sobel"

    elif key == ord('6'):
        mode = "laplacian"

    # Save processed image
    elif key == ord('s'):
        cv2.imwrite("processed_image.jpg", result)
        print("Image saved successfully!")

    # Exit application
    elif key == ord('q'):
        print("Application closed!")
        break

# Release webcam
camera.release()
cv2.destroyAllWindows()
