
import cv2
import mediapipe as mp
import numpy as np
import screen_brightness_control as sbc
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL



print("ADVANCED GESTURE CONTROL STARTING...")


try:
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume_control = cast(interface, POINTER(IAudioEndpointVolume))
    min_volume, max_volume = volume_control.GetVolumeRange()[:2]
except Exception as e:
    print("Audio Error:", e)
    raise SystemExit


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

THUMB = mp_hands.HandLandmark.THUMB_TIP
INDEX = mp_hands.HandLandmark.INDEX_FINGER_TIP


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webcam not found!")
    raise SystemExit

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

WINDOW = "ADVANCED GESTURE CONTROL"
cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)

# SYSTEM VARIABLES
paused = False
muted = False
volume = 50
brightness = 50
smooth_volume = 50.0
smooth_brightness = 50.0
fps = 0
previous_time = time.time()
last_volume = 0
last_brightness = 0
SMOOTHING = 0.25
DELAY = 0.1


def draw_bar(img, x, y, value, color, title):
    value = int(np.clip(value, 0, 100))
    cv2.rectangle(img, (x, y), (x+35, y+220), color, 2)
    fill = int(220 * value / 100)
    cv2.rectangle(
        img, (x, y+220-fill), (x+35, y+220),
        color, cv2.FILLED
    )
    cv2.putText(img, title, (x-10, y-15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    cv2.putText(img, f"{value}%", (x-5, y+250),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def dashboard(img):
    h, w = img.shape[:2]
    cv2.rectangle(img, (0, 0), (w, 65), (25, 25, 25), -1)
    cv2.putText(img, "GESTURE CONTROL SYSTEM", (20, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    cv2.putText(img, f"FPS: {fps:.1f}", (w-150, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    draw_bar(img, 45, 130, volume, (255, 100, 0), "VOLUME")
    draw_bar(img, w-85, 130, brightness, (0, 255, 100), "BRIGHTNESS")
    status = "PAUSED" if paused else "ACTIVE"
    color = (0, 0, 255) if paused else (0, 255, 0)
    cv2.putText(img, "STATUS: "+status, (20, h-65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(img, "SPACE: Pause | M: Mute | Q: Exit",
                (20, h-25), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 1)

print("Show your hands to the camera.")
print("Left hand: Volume | Right hand: Brightness")

while True:
    success, img = cap.read()
    if not success:
        print("Camera error!")
        break

    img = cv2.flip(img, 1)
    h, w = img.shape[:2]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # FPS CALCULATION
    now = time.time()
    elapsed = now - previous_time
    if elapsed > 0:
        fps = 1 / elapsed
    previous_time = now

  
    if result.multi_hand_landmarks and not paused:
        for i, hand in enumerate(result.multi_hand_landmarks):
            label = result.multi_handedness[i].classification[0].label
            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
            lm = hand.landmark
            tp = (int(lm[THUMB].x*w), int(lm[THUMB].y*h))
            ip = (int(lm[INDEX].x*w), int(lm[INDEX].y*h))
            cv2.circle(img, tp, 12, (255, 0, 255), -1)
            cv2.circle(img, ip, 12, (255, 0, 255), -1)
            cv2.line(img, tp, ip, (0, 255, 255), 4)
            distance = np.hypot(ip[0]-tp[0], ip[1]-tp[1])

           
            if label == "Left":
                target = np.interp(distance, [30, 250], [0, 100])
                smooth_volume += (target-smooth_volume)*SMOOTHING
                volume = int(np.clip(smooth_volume, 0, 100))
                if now-last_volume > DELAY:
                    db = np.interp(volume, [0, 100],
                                   [min_volume, max_volume])
                    try:
                        volume_control.SetMasterVolumeLevel(float(db), None)
                        last_volume = now
                    except Exception as e:
                        print("Volume error:", e)
                cv2.putText(img, "VOLUME HAND", (tp[0], tp[1]-25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 0), 2)

           
            elif label == "Right":
                target = np.interp(distance, [30, 250], [0, 100])
                smooth_brightness += (target-smooth_brightness)*SMOOTHING
                brightness = int(np.clip(smooth_brightness, 0, 100))
                if now-last_brightness > DELAY:
                    try:
                        sbc.set_brightness(brightness)
                        last_brightness = now
                    except Exception as e:
                        print("Brightness error:", e)
                cv2.putText(img, "BRIGHTNESS HAND", (tp[0], tp[1]-25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 100), 2)

   
    dashboard(img)
    cv2.imshow(WINDOW, img)

   
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break
    elif key == ord(" "):
        paused = not paused
        print("Paused" if paused else "Resumed")
    elif key == ord("m"):
        muted = not muted
        try:
            volume_control.SetMute(1 if muted else 0, None)
            print("Muted" if muted else "Unmuted")
        except Exception as e:
            print("Mute error:", e)

  
    try:
        if cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) < 1:
            break
    except cv2.error:
        break


cap.release()
hands.close()
cv2.destroyAllWindows()
print("GESTURE CONTROL STOPPED SUCCESSFULLY!")
