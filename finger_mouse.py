import cv2
import mediapipe as mp
import pyautogui
import math
import time
from pynput import mouse

pyautogui.FAILSAFE = False

# ===== Mediapipe =====
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# ===== Screen =====
screen_w, screen_h = pyautogui.size()

# ===== Camera =====
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# ===== Smoothing =====
smooth_x, smooth_y = screen_w // 2, screen_h // 2
alpha = 0.18

# ===== Interaction box =====
x_min, x_max = 0.2, 0.8
y_min, y_max = 0.2, 0.8

# ===== States =====
left_clicking = False
right_clicking = False
paused = False
scroll_mode = False

# ===== Physical mouse detection =====
physical_mouse = mouse.Controller()
prev_mouse_pos = physical_mouse.position
last_mouse_move_time = 0
PAUSE_DELAY = 1.2

prev_time = 0

while True:
    # ----- Physical mouse pause -----
    current_mouse_pos = physical_mouse.position
    if current_mouse_pos != prev_mouse_pos:
        paused = True
        last_mouse_move_time = time.time()
    prev_mouse_pos = current_mouse_pos

    if paused and (time.time() - last_mouse_move_time) > PAUSE_DELAY:
        paused = False

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mode_text = "MOVE"

    if not paused:
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]

            # ===== Draw hand skeleton =====
            mp_draw.draw_landmarks(
                frame, hand, mp_hands.HAND_CONNECTIONS
            )

            # ===== Landmarks =====
            ix, iy = hand.landmark[8].x, hand.landmark[8].y
            ibx, iby = hand.landmark[5].x, hand.landmark[5].y
            mx, my = hand.landmark[12].x, hand.landmark[12].y
            px, py = hand.landmark[20].x, hand.landmark[20].y
            tx, ty = hand.landmark[4].x, hand.landmark[4].y

            h, w, _ = frame.shape

            # ===== Draw finger tips =====
            def draw_point(x, y, color):
                cv2.circle(frame, (int(x*w), int(y*h)), 6, color, -1)

            draw_point(ix, iy, (255, 0, 0))    # index
            draw_point(mx, my, (0, 255, 0))    # middle
            draw_point(tx, ty, (0, 0, 255))    # thumb
            draw_point(px, py, (255, 0, 255))  # pinky

            # ===== Cursor movement =====
            norm_x = min(max((ix - x_min) / (x_max - x_min), 0), 1)
            norm_y = min(max((iy - y_min) / (y_max - y_min), 0), 1)

            target_x = int(norm_x * screen_w)
            target_y = int(norm_y * screen_h)

            if abs(target_x - smooth_x) < 5 and abs(target_y - smooth_y) < 5:
                target_x, target_y = smooth_x, smooth_y

            smooth_x = int(smooth_x * (1 - alpha) + target_x * alpha)
            smooth_y = int(smooth_y * (1 - alpha) + target_y * alpha)

            pyautogui.moveTo(smooth_x, smooth_y)

            # ===== Distances =====
            pinch_pinky = math.hypot(tx - px, ty - py)
            pinch_middle = math.hypot(tx - mx, ty - my)
            finger_dist = math.hypot(ix - mx, iy - my)
            tilt = iy - iby

            # ===== LEFT CLICK =====
            if pinch_pinky < 0.07 and not left_clicking:
                pyautogui.mouseDown(button='left')
                left_clicking = True
                mode_text = "LEFT CLICK"
            elif pinch_pinky > 0.09 and left_clicking:
                pyautogui.mouseUp(button='left')
                left_clicking = False

            # ===== RIGHT CLICK =====
            if pinch_middle < 0.07 and not right_clicking:
                pyautogui.click(button='right')
                right_clicking = True
                mode_text = "RIGHT CLICK"
            elif pinch_middle > 0.09:
                right_clicking = False

            # ===== SCROLL (TILT) =====
            scroll_mode = False
            if finger_dist > 0.05 and pinch_pinky > 0.1 and pinch_middle > 0.1:
                if tilt > 0.04:
                    pyautogui.scroll(-40)
                    scroll_mode = True
                    mode_text = "SCROLL DOWN"
                elif tilt < -0.04:
                    pyautogui.scroll(40)
                    scroll_mode = True
                    mode_text = "SCROLL UP"

            # ===== Debug text =====
            cv2.putText(frame, f"LP:{pinch_pinky:.2f}",
                        (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255), 1)
            cv2.putText(frame, f"RP:{pinch_middle:.2f}",
                        (5, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255), 1)
            cv2.putText(frame, f"Tilt:{tilt:.2f}",
                        (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255), 1)

    # ===== FPS & status =====
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time

    status = "PAUSED" if paused else "ACTIVE"
    cv2.putText(frame, f"{status} | {mode_text} | FPS:{int(fps)}",
                (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

    cv2.imshow("Finger Mouse – Debug View", cv2.resize(frame, (360, 270)))

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

