import pygame
import random

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Particle System")

clock = pygame.time.Clock()

particles = []

# Create particles
for _ in range(300):

    particle = {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "vx": random.uniform(-1, 1),
        "vy": random.uniform(-1, 1),
        "size": random.randint(2, 5)
    }

    particles.append(particle)

running = True

while running:

    clock.tick(60)

    screen.fill((0, 0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Update particles
    for p in particles:

        p["x"] += p["vx"]
        p["y"] += p["vy"]

        # Bounce on edges
        if p["x"] <= 0 or p["x"] >= WIDTH:
            p["vx"] *= -1

        if p["y"] <= 0 or p["y"] >= HEIGHT:
            p["vy"] *= -1

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(p["x"]), int(p["y"])),
            p["size"]
        )

    pygame.display.update()

pygame.quit()
