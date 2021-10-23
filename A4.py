import sys
import time

try:
    import numpy as np
except:
    print("ERROR: Numpy not installed properly.")
    sys.exit()
try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print("ERROR: PyOpenGL not installed properly.")
    sys.exit()

'''
INSTALLATION:
-----------------------------------------
unter anaconda (python 3.6):
    conda install numpy
    conda install freeglut
    conda install pyopengl
    conda install pyopengl-accelerate

(bei fehlenden Bibliotheken googeln)

Ausführung:
    start anaconda prompt
    navigiere in den Game Ordner
    tippe: python A5.py
-----------------------------------------
'''


class GameGL(object):
    config = None

    def __init__(self, config=None):
        self.config = config

    '''
    Is needed for the OpenGL-Library because standard strings are not allowed.
    '''

    def toCString(self, string):
        return bytes(string, "ascii")


class BasicGame(GameGL):

    windowName = "PingPong"
    pixelSize = 30

    xMatrix = 5
    yMatrix = 5

    xBall = xMatrix//2+1
    yBall = yMatrix//2

    xPlayer = xMatrix//2
    wPlayer = 3

    xV = 1
    yV = 1

    score = 0



    def __init__(self, name, width=pixelSize*(2+xMatrix), height=pixelSize*(2+yMatrix)):
        super
        self.windowName = name
        self.width = width
        self.height = height

    def keyboard(self, key, x, y):
        # ESC = \x1w
        if key == b'\x1b':
            glutLeaveMainLoop()
            sys.exit(0)

    def display(self):
        # clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # reset position
        glLoadIdentity()
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        action = 2.0 * np.random.random() - 1.0
        if action < -0.3:
            self.xPlayer -= 1
        if action > 0.3:
            self.xPlayer += 1

        # limit players reach
        if self.xPlayer < 0:
            self.xPlayer = 0
        if self.xPlayer > self.xMatrix-1:
            self.xPlayer = self.xMatrix-1

        # update ball coordinates
        self.xBall += self.xV
        self.yBall += self.yV

        # bounce ball on wall
        if (self.xBall > self.xMatrix or self.xBall < 1):
            self.xV = -self.xV
        if (self.yBall > self.yMatrix or self.yBall < 1):
            self.yV = -self.yV

        # check whether ball on bottom line
        if self.yBall == 0:
            # player-ball collision
            if (self.xPlayer == self.xBall
                    or self.xPlayer == self.xBall - 1
                    or self.xPlayer == self.xBall - 2):
                print("positive reward")
            else:
                print("negative reward")

        self.drawBall()
        self.drawPlayer()

        # adaptive speed depending on matrix size
        time.sleep(0.8/((self.xMatrix+self.yMatrix)/2))

        glutSwapBuffers()

    def start(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(self.toCString(self.windowName))
        # self.init()
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.onResize)
        glutIdleFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutMainLoop()

    def updateSize(self):
        self.width = glutGet(GLUT_WINDOW_WIDTH)
        self.height = glutGet(GLUT_WINDOW_HEIGHT)

    def onResize(self, width, height):
        self.width = width
        self.height = height

    def drawBall(self, width=1, height=1, x=xBall, y=yBall, color=(0.0, 1.0, 0.0)):
        x = self.xBall
        y = self.yBall
        xPos = x * self.pixelSize
        yPos = y * self.pixelSize
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, yPos)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), yPos)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), yPos + (self.pixelSize * height))
        # top left point
        glVertex2f(xPos, yPos + (self.pixelSize * height))
        glEnd()

    def drawPlayer(self, width=wPlayer, height=1, x=0, y=0, color=(1.0, 0.0, 0.0)):
        x = self.xPlayer
        xPos = x * self.pixelSize
        # set a bit away from bottom
        yPos = y * self.pixelSize  # + (self.pixelSize * height / 2)
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, yPos)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), yPos)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), yPos + (self.pixelSize * height / 4))
        # top left point
        glVertex2f(xPos, yPos + (self.pixelSize * height / 4))
        glEnd()


if __name__ == '__main__':
    game = BasicGame("PingPong")
    game.start()