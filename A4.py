#author: Candra Mulyadhi (1920996)
#date: 31/10/2021

import random
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


gamma = 0.9  # [0,1]
alpha = 0.1  # [0,1]
epsilon = 0.01  # [0,1]
state = 0


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

    pixelSize = 30
    speed = 0.3
    score = 0
    count = 0
    hits = 0
    reward = 0

    action = [-1, 0, 1]


    # ENGINE
    def __init__(self, name, x, y, w):
        super
        self.windowName = name
        self.xMatrix, self.yMatrix = x, y
        self.width = self.pixelSize * self.xMatrix
        self.height = self.pixelSize * self.yMatrix

        self.xBall, self.yBall = (self.xMatrix // 2), (self.yMatrix // 2)
        self.xPlayer, self.wPlayer = (self.xMatrix // 2), w
        self.xV, self.yV = 1, 1

        self.amount_states = self.xMatrix ** 2 * 4 * (self.xMatrix - (self.wPlayer - 1))
        self.limit = [self.xMatrix, self.yMatrix, 1, 1, (self.xMatrix - (self.wPlayer - 1))]
        self.Q_t = np.zeros((self.amount_states, len(self.action)))

    def keyboard(self, key, x, y):
        # ESC = \x1w
        if key == b'\x1b':
            glutLeaveMainLoop()
            sys.exit(0)

    def start(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(self.toCString(self.windowName))

        self.initiate_Q()
        self.state = self.get_state()
        glutDisplayFunc(self.run)
        glutReshapeFunc(self.on_resize)
        glutIdleFunc(self.run)
        glutKeyboardFunc(self.keyboard)
        glutMainLoop()

    def update_size(self):
        self.width = glutGet(GLUT_WINDOW_WIDTH)
        self.height = glutGet(GLUT_WINDOW_HEIGHT)

    def on_resize(self, width, height):
        self.width = width
        self.height = height


    # VISUALISATION
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

    def draw_ball(self, width=1, height=1, color=(0.0, 1.0, 0.0)):
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

    def draw_player(self, height=1, color=(1.0, 0.0, 0.0)):

        xPos = self.xPlayer * self.pixelSize

        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, 0)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * self.wPlayer), 0)
        # top right point
        glVertex2f(xPos + (self.pixelSize * self.wPlayer), (self.pixelSize * height))
        # top left point
        glVertex2f(xPos, (self.pixelSize * height))
        glEnd()


    # PHYSICS
    def move_player(self, idx):
        self.xPlayer += self.action[idx]

    def limit_player_reach(self):
        # limit players reach
        if self.xPlayer < 0:
            self.xPlayer = 0
        if self.xPlayer + self.wPlayer > self.xMatrix:
            self.xPlayer = self.xMatrix - self.wPlayer

    def move_ball(self):
        self.xBall += self.xV
        self.yBall += self.yV

    def bounce_ball(self):
        if (self.xBall >= self.xMatrix - 1 or self.xBall < 1):
            self.xV = -self.xV
        if (self.yBall >= self.yMatrix - 1 or self.yBall < 1):
            self.yV = -self.yV

    def handle_collision(self):
        self.reward = 0
        # check whether ball on bottom line
        if self.yBall == 1 and self.yV == -1:

            self.count += 1

            if self.xV > 0:
                threshold_r = self.xPlayer + (self.wPlayer - 1)
                threshold_l = self.xPlayer - 1
            else:
                threshold_r = self.xPlayer + self.wPlayer
                threshold_l = self.xPlayer

            # player-ball collision
            if self.xBall >= threshold_l and self.xBall <= threshold_r:
                # bounce ball on player
                self.hits += 1
                self.yV = -self.yV
                self.score = self.score + self.xMatrix/10
                self.reward = 1
                p = int(round(self.hits / self.count, 2)*100)
                print("hitrate:",p, "%       HIT > ", self.score)
            else:
                p = int(round(self.hits / self.count, 2)*100)
                print("hitrate:",p, "%             ", self.score, " < MISS")
                self.reward = -1
                self.score = self.score - 1


    # LEARNING
    def initiate_Q(self):
        for i in range(len(self.Q_t)):
            for j in range(len(self.Q_t[0])):
                rand = random.uniform(0.01, 0.001)
                self.Q_t[i][j] = rand

    def get_environment(self):
        return [self.xBall, self.yBall, self.xV, self.yV, self.xPlayer]

    def get_state(self):
        env = self.get_environment()
        s = env[0]
        for i in range(1, len(env)):
            s = s * self.limit[i] + env[i]
        return s

    def select_action(self):
        p = random.random()
        if p > epsilon:
            val, idx = self.get_max(self.Q_t[self.state])
            return idx
        else:
            return random.randrange(0, len(self.action))

    def get_max(self, arr):
        idx, max = 0, 0
        for i in range(len(arr)):
            if arr[i] > max:
                max = arr[i]
                idx = i
        return max, idx

    def update_Q_t(self, new_state, action):
        val, idx = self.get_max(self.Q_t[new_state])
        self.Q_t[self.state][action] = self.Q_t[self.state][action] + \
                                       alpha * (self.reward + gamma * val - self.Q_t[self.state][action])



    def run(self):

        action = self.select_action()
        self.move_player(action)
        self.limit_player_reach()

        self.move_ball()
        self.bounce_ball()
        self.handle_collision()

        new_state = self.get_state()
        self.update_Q_t(new_state, action)
        self.state = new_state


        self.display()
        self.draw_ball()
        self.draw_player()


        time.sleep(self.speed / (self.xMatrix * self.yMatrix))
        glutSwapBuffers()


if __name__ == '__main__':

    xMax, yMax = 10, 10
    player_width = 3
    game = BasicGame("pingpong", xMax, yMax, player_width)
    game.start()
