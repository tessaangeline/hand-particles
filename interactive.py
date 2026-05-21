import cv2
import mediapipe as mp
import math
import random

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# ---------------------------
# MEDIAPIPE SETUP
# ---------------------------

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

# ---------------------------
# OPENGL SETUP
# ---------------------------

pygame.init()

display = (1000, 700)

pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

glTranslatef(0.0, 0.0, -8)

glEnable(GL_BLEND)

glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glPointSize(2)

# ---------------------------
# PARTICLES
# ---------------------------

particles = []

num_particles = 3000

for i in range(num_particles):

    theta = random.uniform(0, math.pi)
    phi = random.uniform(0, 2 * math.pi)

    particles.append((theta, phi))

clock = pygame.time.Clock()

time_value = 0

# Orb size
base_radius = 4

# ---------------------------
# MAIN LOOP
# ---------------------------

while True:

    clock.tick(60)

    time_value += 0.03

    # ---------------------------
    # WEBCAM PROCESSING
    # ---------------------------

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    hand_centers = []

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            x_list = []
            y_list = []

            for lm in hand_landmarks.landmark:

                x_list.append(lm.x)
                y_list.append(lm.y)

            center_x = sum(x_list) / len(x_list)
            center_y = sum(y_list) / len(y_list)

            hand_centers.append((center_x, center_y))

    # ---------------------------
    # HAND DISTANCE LOGIC
    # ---------------------------

    target_radius = 4

    if len(hand_centers) == 2:

        x1, y1 = hand_centers[0]
        x2, y2 = hand_centers[1]

        distance = math.hypot(x2 - x1, y2 - y1)

        # Hands close = smaller orb
        target_radius = 1 + distance * 5

    # Smooth transition
    base_radius += (target_radius - base_radius) * 0.05

    # ---------------------------
    # OPENGL EVENTS
    # ---------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            cap.release()
            quit()

    # ---------------------------
    # RENDERING
    # ---------------------------

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glRotatef(0.2, 0.2, 1, 0.3)

    glBegin(GL_POINTS)

    for theta, phi in particles:

        wave = math.sin(theta * 6 + time_value) * 0.2

        radius = base_radius + wave

        x = radius * math.sin(theta) * math.cos(phi)
        y = radius * math.sin(theta) * math.sin(phi)
        z = radius * math.cos(theta)

        r = 0.4 + 0.3 * math.sin(time_value + theta)

        glColor4f(r, 0.5, 1.0, 1)

        glVertex3f(x, y, z)

    glEnd()

    pygame.display.flip()
