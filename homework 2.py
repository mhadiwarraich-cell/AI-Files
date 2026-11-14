
import cv2

# Load face detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# Start webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Webcam not found!")
    exit()

print("REAL-TIME FACE TRACKING & PEOPLE COUNT")
print("Press Q to quit")

while True:

    # Capture webcam frame
    success, frame = camera.read()

    if not success:
        print("Cannot read webcam!")
        break

    # Flip camera
    frame = cv2.flip(frame, 1)

    # Convert image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40)
    )

    # Count detected faces
    count = len(faces)

    # Draw rectangles around faces
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Display face label
        cv2.putText(
            frame,
            "Face Detected",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # Display people count
    cv2.putText(
        frame,
        "People Count: " + str(count),
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    # Display webcam
    cv2.imshow("Face Tracking and People Count", frame)

    # Quit using Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam
camera.release()
cv2.destroyAllWindows()

print("Application closed!")
