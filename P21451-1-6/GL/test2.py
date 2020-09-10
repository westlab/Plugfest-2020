import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

BASE_RADIUS = 0.1
BASE_HEIGHT = 0.1
UPPER_ARM_WIDTH = 0.05
UPPER_ARM_HEIGHT=0.5
LOWER_ARM_WIDTH=0.08
LOWER_ARM_HEIGHT=0.3
tb=0
tl=45
tu=30

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    gluLookAt(2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glColor3f(1.0, 0.0, 0.0)
    glRotatef(tb, 0.0, 1.0, 0.0)
    base()
    glTranslatef(0.0, BASE_HEIGHT, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glRotatef(tl, 0.0, 0.0, 1.0)
    lower_arm()
    glTranslatef(0.0, LOWER_ARM_HEIGHT, 0.0)
    glRotatef(tu, 0.0, 0.0, 1.0)
    glColor3f(0.0, 0.0, 1.0)
    upper_arm()
    glFlush()

def base():
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(p, BASE_RADIUS, BASE_RADIUS, BASE_HEIGHT, 10, 10)
    glPopMatrix()

def upper_arm():
    glPushMatrix()
    glTranslatef(0.0, 0.5*UPPER_ARM_HEIGHT, 0.0)
    glScalef(UPPER_ARM_WIDTH, UPPER_ARM_HEIGHT, UPPER_ARM_WIDTH)
    glutSolidCube(1.0)
    glPopMatrix()

def lower_arm():
    glPushMatrix()
    glTranslatef(0.0, 0.5*LOWER_ARM_HEIGHT, 0.0)
    glScalef(LOWER_ARM_WIDTH, LOWER_ARM_HEIGHT, LOWER_ARM_WIDTH)
    glutSolidCube(1.0)
    glPopMatrix()

def mykey(key, x, y):
    global tb, tl, tu
    if key=='q': # +base
        tb = tb + 5.0
    elif key=='a': # -base
        tb = tb - 5.0
    elif key=='w': #+lower
        tl = tl + 5.0
    elif key=='s': #-lower
        tl = tl - 5.0
    elif key=='e': #+upper
        tu = tu + 5.0
    elif key=='d': #-upper
        tu = tu - 5.0
    print "tb=", tb, " tl=", tl, " tu=", tu
    glutPostRedisplay()
            
glutInit( sys.argv )
glutInitDisplayMode( GLUT_SINGLE | GLUT_RGB )
glutInitWindowSize( 500, 500 )
glutInitWindowPosition(0,0)
glutCreateWindow( 'robot' )
glutDisplayFunc( display )
glutKeyboardFunc(mykey)
p=gluNewQuadric()
gluQuadricDrawStyle(p, GLU_LINE)

glClearColor(0.0, 0.0, 0.0, 0.0)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(30, 1.0, 0.0, 100.0)

glutMainLoop()

