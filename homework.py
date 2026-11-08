
import cv2
from deepface import DeepFace

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Start webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Cannot open webcam.")
    exit()

print("Press Q to quit.")

while True:
    success, frame = camera.read()

    if not success:
        print("Cannot read webcam.")
        break

    # Convert image to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
    )

    for (x, y, w, h) in faces:
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Crop the face
        face = frame[y:y + h, x:x + w]

        try:
            # Predict facial expression with pretrained model
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

            # Display predicted expression
            cv2.putText(
                frame, emotion, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0), 2
            )

        except Exception:
            cv2.putText(
                frame, "Emotion unavailable", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 0, 255), 2
            )

    # Show live video
    cv2.imshow("Face and Emotion Detection", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
