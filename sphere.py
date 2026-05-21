import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
import random

pygame.init()

display = (1000, 700)

pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

glTranslatef(0.0, 0.0, -8)

glEnable(GL_BLEND)

glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glPointSize(2)

particles = []

num_particles = 3000
base_radius = 2

# Generate sphere coordinates
for i in range(num_particles):

    theta = random.uniform(0, math.pi)
    phi = random.uniform(0, 2 * math.pi)

    particles.append((theta, phi))

clock = pygame.time.Clock()

time_value = 0

while True:

    clock.tick(60)

    time_value += 0.03

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glRotatef(0.2, 0.2, 1, 0.3)

    glBegin(GL_POINTS)

    for theta, phi in particles:

        # Wave deformation
        wave = math.sin(theta * 6 + time_value) * 0.2

        radius = base_radius + wave

        x = radius * math.sin(theta) * math.cos(phi)
        y = radius * math.sin(theta) * math.sin(phi)
        z = radius * math.cos(theta)

        # Gradient glow
        r = 0.4 + 0.3 * math.sin(time_value + theta)
        g = 0.5
        b = 1.0

        glColor4f(r, g, b, 1)

        glVertex3f(x, y, z)

    glEnd()

    pygame.display.flip()
