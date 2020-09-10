import sys
import math
import re
import argparse
import random
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

SPPARAM = 20.0

position = [-20.0, 20.0, 100.0, 1.0]
ambient = [0.6, 0.6, 0.6]
diffuse = [0.7, 0.7, 0.7]
specular = [0.2, 0.2, 0.2]

sp = 0.0
tb = 0.0
tl = 0.0

parser = argparse.ArgumentParser(
    prog = 'wind.py',
    usage = 'Receive wind speed/direction sensor data from MQTT server',
    description= 'This applicatin visualize SGLab HWD Series Wind sensor (anomometer) using OpenGL',
    epilog = 'Programmer Hiroaki Nishi west@west.yokohama',
    add_help = True)
parser.add_argument('--version', version='%(prog)s 0.1',
    action = 'version',
    help = 'verbose operation (output sensor data)')
parser.add_argument('-v', '--verbose',
    action = 'store_true',
    help = 'verbose operation (output sensor data)',
    default = False)
parser.add_argument('-q', '--quiet',
    action = 'store_true',
    help = 'quiet (does not output data messages)',
    default = False)
parser.add_argument('-P', '--pseudo_sensor',
    action = 'store_true',
    help = 'generate random sensor values without ALPS module',
    default = False)
parser.add_argument('-D', '--demo',
    action = 'store_true',
    help = 'DEMO mode to operate using key q<>a:length w<>s:rotation e<>d:depression o:quit',
    default = False)
parser.add_argument('-d', '--broker_address',
    action = 'store',
    help = 'specify destination MQTT broker address',
    default = '131.113.98.77',
    type = str)
parser.add_argument('-p', '--broker_port',
    action = 'store',
    help = 'specify destination MQTT broker port',
    default = 1883,
    type = int)
parser.add_argument('-t', '--topic',
    action = 'store',
    help = 'specify topic of MQTT',
    default = '/TESTData',
    type = str)
parser.add_argument('-E', '--elasticsearch',
    action = 'store_true',
    help = 'prepare elasticsearch/kibana data and push',
    default = False)
parser.add_argument('-e', '--elasticsearch_address',
    action = 'store',
    help = 'specify destination Bluetooth address',
    nargs = '?',
    default = 'http://localhost:9200/plugfest',
    type = str)

args = parser.parse_args()
port = args.broker_port
host = args.broker_address
topic = args.topic
vflag = False
if args.verbose:
    vflag = True
qflag = False
if args.quiet:
    qflag = True
dflag = False
dummyflag = False
if args.demo:
    dflag = True
    dummyflag = True
if args.pseudo_sensor:
    dummyflag = True
eflag = False
if args.elasticsearch:
    eflag = True
pflag = False
if args.pseudo_sensor:
    pflag = True

def on_connect(client, userdata, flags, respons_code):
    if qflag == False:
        print('CONNECT: status {0}'.format(respons_code))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global sp, tb, tl
    strdat = str(msg.payload,'utf-8')
    if vflag:
        print(msg.topic + ' ' + strdat)
    ardat = strdat.split(',')
    if(re.search('<AM', ardat[0])):
        try:
            sp = float(ardat[1])
        except:
            return
        try:
            tb = -float(ardat[2])
        except:
            return
        try:
            tl = float(ardat[3])-90.0
        except:
            return
        if qflag == False:
            print("RCV:", sp, tb, tl)
        glutPostRedisplay()

def display():
    global sp, tb, tl
    if vflag:
        print("USE:", sp, tb, tl)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, 1.0, 1.0, 100.0)
#    glMatrixMode(GL_MODELVIEW)

    gluLookAt(2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)
    glRotatef(tb, 0.0, 1.0, 0.0)
    glRotatef(tl, 0.0, 0.0, 1.0)
#    glTranslatef(-UPPER_ARM_WIDTH/2, sp*SPPARAM, -UPPER_ARM_WIDTH/2)
    glTranslatef(0, sp*SPPARAM, 0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(p, UPPER_ARM_WIDTH, 0, UPPER_ARM_HEIGHT, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.0, 1.0, 0.0)
    glRotatef(tb, 0.0, 1.0, 0.0)
    glRotatef(tl, 0.0, 0.0, 1.0)
    glTranslatef(0.0, BASE_HEIGHT, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(p, LOWER_ARM_WIDTH, LOWER_ARM_WIDTH, sp*SPPARAM, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glRotatef(tb, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(p, BASE_RADIUS, BASE_RADIUS, BASE_HEIGHT, 20, 10)
    glScalef(BASE_RADIUS, BASE_RADIUS, BASE_HEIGHT) 
    glutSolidCube(1.0)
    glPopMatrix()

    glFlush()

def mykey(key, x, y):
    if vflag:
        print("key:",key)
    global tb, tl, sp
    if key == b'Q': # +base
        sp = sp + 0.01
    elif key == b'A': # -base
        sp = sp - 0.01
    elif key == b'W': #+lower
        tb = tb + 5.0
    elif key == b'S': #-lower
        tb = tb - 5.0
    elif key == b'E': #+upper
        tl = tl + 5.0
    elif key == b'D': #-upper
        tl = tl - 5.0
    elif key == b'O': 
        sys.exit()
    if vflag:
        print("sp=", sp, "tb=", tb, " tl=", tl)
    glutPostRedisplay()

def idlef():
    global tb, tl, sp
    if dummyflag == True and dflag == False:
        global sp, tb, tl
        sp = sp + random.randint(-3, 3)/100
        if sp < 0.0:
            sp == 0.0
        if sp > 2.0:
            sp == 1.5
        tb = tb + random.randint(-20, 20)
        tl = tl + random.randint(-20, 20)
    glutPostRedisplay()
    sleep(0.2)

if sys.version_info[0] != 3:
    print("Version 3 is required")
    sys.exit()
            
glutInit( sys.argv )
glutInitDisplayMode( GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize( 400, 400 )
glutInitWindowPosition(100,0)
glutCreateWindow( 'WindArrow' )
glutDisplayFunc( display )
glutKeyboardFunc(mykey)
glutIdleFunc(idlef)
p = gluNewQuadric()
#gluQuadricDrawStyle(p, GLU_LINE)
gluQuadricDrawStyle(p, GLU_FILL)

glClearColor(0.0, 0.0, 0.0, 0.0)

#glLightfv(GL_LIGHT0, GL_POSITION, position)
#glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
#glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
#glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
glEnable(GL_DEPTH_TEST)
#glEnable(GL_LIGHTING)
#glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # Wireframe

if dummyflag == False:
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host , port, 60)
    client.loop_start()
glutMainLoop()
