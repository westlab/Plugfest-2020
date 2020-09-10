from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()


def main():
    glutInit(sys.argv)
    glutInitWindowSize(300, 300)
    glutInitDisplayMode(GLUT_RGBA)
    glutCreateWindow(b"OpenGL")

    glutDisplayFunc(display)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glutMainLoop()

    return 0


if __name__ == "__main__":
    main()
