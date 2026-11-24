
import cv2
import mediapipe as mp
import pyautogui
import time


mp_hands = mp.solutions.hands
draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1,
    min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)
SCROLL_AMOUNT, DELAY = 100, 0.15
last_scroll = 0


def count_fingers(hand):
    lm = hand.landmark
    tips = [8, 12, 16, 20]
    joints = [6, 10, 14, 18]
    return sum(lm[t].y < lm[j].y for t, j in zip(tips, joints))

print("Open palm: scroll up | Fist: scroll down | Q: quit")

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    gesture, color = "No hand detected", (255, 255, 255)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        count = count_fingers(hand)
        if count == 4:
            gesture, color = "OPEN PALM - SCROLL UP", (0, 255, 0)
            direction = 1
        elif count == 0:
            gesture, color = "FIST - SCROLL DOWN", (0, 0, 255)
            direction = -1
        else:
            gesture, color = "Hand detected - waiting", (0, 255, 255)
            direction = 0

       
        if direction and time.time() - last_scroll >= DELAY:
            pyautogui.scroll(direction * SCROLL_AMOUNT)
            last_scroll = time.time()

    cv2.putText(frame, "GESTURE SCROLL", (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(frame, gesture, (15, 75),
        cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)
    cv2.imshow("Gesture Scrolling", frame)
    if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
print("Program ended.")
