import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    h, w, c = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    hand_centers = []

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            x_list = []
            y_list = []

            for lm in hand_landmarks.landmark:

                x_list.append(lm.x)
                y_list.append(lm.y)

            center_x = int(sum(x_list) / len(x_list) * w)
            center_y = int(sum(y_list) / len(y_list) * h)

            hand_centers.append((center_x, center_y))

            cv2.circle(frame, (center_x, center_y), 10, (0, 255, 0), -1)

        # If 2 hands detected
        if len(hand_centers) == 2:

            x1, y1 = hand_centers[0]
            x2, y2 = hand_centers[1]

            distance = int(math.hypot(x2 - x1, y2 - y1))

            # Draw line between hands
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # Show distance
            cv2.putText(
                frame,
                f"Distance: {distance}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
