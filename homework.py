
import cv2
from deepface import DeepFace

# Load face detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# Start webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Webcam not found!")
    exit()

print("REAL-TIME FACE AND EMOTION DETECTION")
print("Press Q to quit")

while True:

    # Read webcam frame
    success, frame = camera.read()

    if not success:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(
        frame, cv2.COLOR_BGR2GRAY
    )

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    # Process each detected face
    for (x, y, w, h) in faces:

        # Crop face
        face = frame[y:y+h, x:x+w]

        try:
            # Detect emotion
            result = DeepFace.analyze(
                face,
                actions=["emotion"],
                enforce_detection=False,
                detector_backend="skip",
                silent=True
            )

            if isinstance(result, list):
                result = result[0]

            emotion = result["dominant_emotion"]

        except Exception:
            emotion = "Unknown"

        # Draw rectangle around face
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        # Display emotion
        cv2.putText(
            frame,
            emotion,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    # Display webcam
    cv2.imshow(
        "Face and Emotion Detection",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close webcam
camera.release()
cv2.destroyAllWindows()

print("Application closed!")
