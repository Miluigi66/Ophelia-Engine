from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initialize OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glEnable(GL_DEPTH_TEST)  # Enable depth testing

# Display callback
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen and depth buffer

    # Render OpenGL content here
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex3f(-0.5, -0.5, -1.0)
    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex3f(0.5, -0.5, -1.0)
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glVertex3f(0.0, 0.5, -1.0)
    glEnd()

    glutSwapBuffers()  # Swap buffers

# Keyboard callback
def keyboard(key, x, y):
    if key == b'\x1b':  # ESC key
        glutLeaveMainLoop()

# Main function
def main():
    glutInit()  # Initialize GLUT
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffer, RGB, depth buffer
    glutInitWindowSize(800, 600)  # Window size
    glutCreateWindow(b"OpenGL with GLUT")  # Create window with title

    init()  # Initialize OpenGL settings

    glutDisplayFunc(display)  # Set display callback
    glutIdleFunc(display)  # Redraw continuously
    glutKeyboardFunc(keyboard)  # Set keyboard callback

    glutMainLoop()  # Enter the main loop

if __name__ == "__main__":
    main()