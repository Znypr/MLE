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

    xBall = xMatrix//2
    yBall = yMatrix//2


    xPlayer = xMatrix//2
    wPlayer = 2

    xV = 1
    yV = 1

    score = 0


    def simulateBallMovement(self, x, y, xV, yV):

        x += xV
        y += yV

        if (x >= self.xMatrix-1 or x < 1):
            xV = -xV
        if (y >= self.yMatrix-1 or y < 1):
            yV = -yV

        return x,y, xV, yV

    def calculateProjection(self):

        x, y = self.xBall, self.yBall
        xV, yV = self.xV, self.yV

        while y > 1:
            x, y, xV, yV = self.simulateBallMovement(x, y, xV, yV)

        return x

    def getRewards(self, projectedTarget):

        rewards = np.ones((self.xMatrix - self.wPlayer + 1,), dtype=int) * -1

        for i in range(self.wPlayer):
            if projectedTarget < len(rewards) and projectedTarget >= 0:
                rewards[projectedTarget] = 1

            projectedTarget = projectedTarget - 1
        return rewards



    def __init__(self, name, width=pixelSize*xMatrix, height=pixelSize*yMatrix):
        super
        self.windowName = name
        self.width = width
        self.height = height

    def keyboard(self, key, x, y):
        # ESC = \x1w
        if key == b'\x1b':
            glutLeaveMainLoop()
            sys.exit(0)



    def movePlayer(self):

        action = 2.0 * np.random.random() - 1.0
        if action < -0.3:
            self.xPlayer -= 1
        if action > 0.3:
            self.xPlayer += 1

    def limitPlayerReach(self):
        # limit players reach
        if self.xPlayer < 0:
            self.xPlayer = 0
        if self.xPlayer+self.wPlayer > self.xMatrix:
            self.xPlayer = self.xMatrix-self.wPlayer


    def moveBall(self):
        self.xBall += self.xV
        self.yBall += self.yV

    def bounceBall(self):
        if (self.xBall >= self.xMatrix-1 or self.xBall < 1):
            self.xV = -self.xV
        if (self.yBall >= self.yMatrix-1 or self.yBall < 1):
            self.yV = -self.yV

    def handleCollision(self, rewards):
        # check whether ball on bottom line
        if self.yBall == 1 and self.yV == -1:
            self.score += rewards[self.xPlayer]
            # player-ball collision
            if self.xBall >= self.xPlayer-1 and self.xBall <= self.xPlayer + self.wPlayer:
                # bounce ball on player
                self.yV = -self.yV
                print("HIT > ", self.score)
            else:
                print("MISS > ", self.score)

            print(rewards)


    def run(self):

        self.display()

        rewards = self.getRewards(self.calculateProjection())

        self.movePlayer()
        self.limitPlayerReach()

        self.moveBall()
        self.bounceBall()

        self.handleCollision(rewards)


        self.drawBall()
        self.drawPlayer()

        # adaptive speed depending on matrix size
        time.sleep(1/((self.xMatrix+self.yMatrix)))

        glutSwapBuffers()

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

    def start(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(self.toCString(self.windowName))
        # self.init()
        glutDisplayFunc(self.run)
        glutReshapeFunc(self.onResize)
        glutIdleFunc(self.run)
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

    def drawPlayer(self, width=wPlayer, height=1, color=(1.0, 0.0, 0.0)):

        xPos = self.xPlayer * self.pixelSize
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, 0)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), 0)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), (self.pixelSize * height))
        # top left point
        glVertex2f(xPos, (self.pixelSize * height))
        glEnd()


if __name__ == '__main__':
    game = BasicGame("PingPong")
    game.start()