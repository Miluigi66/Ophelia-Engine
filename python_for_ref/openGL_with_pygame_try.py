import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Initialize pygame and OpenGL
pygame.init()
pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL with Pygame")

# Set up OpenGL
glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
glEnable(GL_DEPTH_TEST)  # Enable depth testing

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    # Clear the screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Render OpenGL content here
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex3f(-0.5, -0.5, -1.0)
    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex3f(0.5, -0.5, -1.0)
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glVertex3f(0.0, 0.5, -1.0)
    glEnd()

    # Swap buffers
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()