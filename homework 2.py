
import cv2
import numpy as np


camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Webcam not found!")
    exit()


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

   
    result = frame.copy()

  
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    if mode == "red":
        result[:, :, 0] = 0
        result[:, :, 1] = 0

    elif mode == "green":
        result[:, :, 0] = 0
        result[:, :, 2] = 0

    elif mode == "blue":
        result[:, :, 1] = 0
        result[:, :, 2] = 0

   
    elif mode == "canny":
        edges = cv2.Canny(gray, 100, 200)
        result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    
    elif mode == "sobel":
        x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        edges = cv2.magnitude(x, y)
        edges = cv2.convertScaleAbs(edges)

        result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif mode == "laplacian":
        edges = cv2.Laplacian(gray, cv2.CV_64F)
        edges = cv2.convertScaleAbs(edges)

        result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

   
    cv2.putText(
        result,
        "Mode: " + mode,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    
    cv2.imshow("Image Processing Application", result)

 
    key = cv2.waitKey(1) & 0xFF

  
    if key == ord('0'):
        mode = "original"

    elif key == ord('1'):
        mode = "red"

    elif key == ord('2'):
        mode = "green"

    elif key == ord('3'):
        mode = "blue"


    elif key == ord('4'):
        mode = "canny"

    elif key == ord('5'):
        mode = "sobel"

    elif key == ord('6'):
        mode = "laplacian"

 
    elif key == ord('s'):
        cv2.imwrite("processed_image.jpg", result)
        print("Image saved successfully!")

  
    elif key == ord('q'):
        print("Application closed!")
        break

camera.release()
cv2.destroyAllWindows()
