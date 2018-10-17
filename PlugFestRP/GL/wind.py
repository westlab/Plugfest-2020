import sys
import math
from time import sleep
import paho.mqtt.client as mqtt
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

BASE_RADIUS = 0.7
BASE_HEIGHT = 0.05
UPPER_ARM_WIDTH = 0.08
UPPER_ARM_HEIGHT = 0.3
LOWER_ARM_WIDTH = 0.03
LOWER_ARM_HEIGHT = 0.5

position = [-2.0, 2.0, 10.0, 1.0]
ambient = [0.5, 0.5, 0.5]
diffuse = [0.7, 0.7, 0.7]
specular = [0.2, 0.2, 0.2]

tb = 0
tl = 0
sp = 0

host = '131.113.98.77'
port = 1883
topic = 'TESTData'

def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    strdat = str(msg.payload,'utf-8')
    print(msg.topic + ' ' + strdat)
    ardat = istrdat.split(',')
    if(ardat[0] == "<AM"):
        sp = float(ardata[1])
        tb = float(ardata[2])
        tl = float(ardata[3])
        print(sp, tb, tl)
        glutPostRedisplay()
        

def display():
#    glLightfv(GL_LIGHT0, GL_POSITION, position)
#    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
#    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
#    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
#    glEnable(GL_LIGHTING)
#    glEnable(GL_LIGHT0)
#    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
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
    glTranslatef(0.0, sp*10, 0.0)
    glRotatef(0, 0.0, 0.0, 1.0)
    glColor3f(0.0, 0.0, 1.0)
    upper_arm()
    glFlush()

def base():
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(p, BASE_RADIUS, BASE_RADIUS, BASE_HEIGHT, 20, 10)
    glScalef(BASE_RADIUS, BASE_RADIUS, BASE_HEIGHT) 
    glutSolidCube(1.0)
    glPopMatrix()

def upper_arm():
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(p, UPPER_ARM_WIDTH, 0, UPPER_ARM_HEIGHT, 10, 10)
    glPopMatrix()

def lower_arm():
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(p, LOWER_ARM_WIDTH, LOWER_ARM_WIDTH, sp*10, 10, 10)
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
#    elif key=='e': #+upper
#        tu = tu + 5.0
#    elif key=='d': #-upper
#        tu = tu - 5.0
    else: 
        sys.exit()
#    print "tb=", tb, " tl=", tl, " tu=", tu
    print "tb=", tb, " tl=", tl
    glutPostRedisplay()


def idlef():
    glutPostRedisplay()
            
glutInit( sys.argv )
glutInitDisplayMode( GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize( 500, 500 )
glutInitWindowPosition(0,0)
glutCreateWindow( 'WindArrow' )
glutDisplayFunc( display )
glutKeyboardFunc(mykey)
glutIdleFunc(idlef)
p=gluNewQuadric()
#gluQuadricDrawStyle(p, GLU_LINE)
gluQuadricDrawStyle(p, GLU_FILL)

glClearColor(0.0, 0.0, 0.0, 0.0)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(30, 1.0, 0.0, 100.0)

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port=port, keepalive=60)
client.loop_start()
glutMainLoop()

