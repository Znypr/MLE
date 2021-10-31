import random
import sys
import time
import math

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


class Player(object):
    xPos = 0
    yPos = 0
    width = 0

    def __init__(self, xPos, width):
        super
        self.xPos = xPos
        self.width = width

    def move(self, d):
        self.xPos += d

    def limit_mobility(self, xLimit):
        # limit players reach
        if self.xPos < 0:
            self.xPos = 0
        if self.xPos + self.width > xLimit:
            self.xPos = xLimit - self.width

class Ball(object):
    xPos, yPos = 0, 0
    xDir, yDir = 1, 1

    def __init__(self, xPos, yPos, xDir, yDir):
        self.xPos, self.yPos = xPos, yPos
        self.xDir, self.yDir = xDir, yDir

    def move(self):
        self.xPos += self.xDir
        self.yPos += self.yDir

    def set_direction(self, xDir, yDir):
        self.xDir, self.yDir = xDir, yDir

    def bounce_ball(self, xLimit, yLimit):
        if (self.xPos >= xLimit - 1 or self.xPos < 1):
            self.xDir = -self.xDir
        if (self.yPos >= yLimit - 1 or self.yPos < 1):
            self.yDir = -self.yDir

class GameGL(object):
    config = None

    def __init__(self, config=None):
        self.config = config


    def toCString(self, string):
        return bytes(string, "ascii")

class BasicGame(GameGL):

    pixelSize = 30
    score = 0
    reward = 0
    action = [-1, 0, 1]


    # ENGINE
    def __init__(self, name, xMatrix, yMatrix, speed, ball, player):
        super

        self.windowName = name
        self.width = self.pixelSize * xMatrix
        self.height = self.pixelSize * yMatrix

        self.xMatrix, self.yMatrix = xMatrix, yMatrix
        self.speed = speed

        self.ball = ball
        self.player = player

        self.amount_states = self.xMatrix ** 2 * 4 * (self.xMatrix - (self.player.width - 1))
        self.limit = [self.xMatrix-1, self.yMatrix-1, 1, 1, (self.xMatrix - (self.player.width - 1))]
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

    def draw_ball(self, color=(0.0, 1.0, 0.0)):

        width, height = 1, 1

        x = ball.xPos
        y = ball.yPos
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

    def draw_player(self, color=(1.0, 0.0, 0.0)):

        height = 1
        xPos = player.xPos * self.pixelSize
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, 0)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * player.width), 0)
        # top right point
        glVertex2f(xPos + (self.pixelSize * player.width), (self.pixelSize * height))
        # top left point
        glVertex2f(xPos, (self.pixelSize * height))
        glEnd()


    # PHYSICS
    def handle_collision(self):
        self.reward = 0
        # check whether ball on bottom line
        if ball.yPos == 1 and ball.yDir == -1:

            if ball.xDir > 0:
                threshold_r = player.xPos + (player.width-1)
                threshold_l = player.xPos - 1
            else:
                threshold_r = player.xPos + player.width
                threshold_l = player.xPos

            # player-ball collision
            if ball.xPos >= threshold_l and ball.xPos <= threshold_r:
                # bounce ball on player
                ball.yDir = -ball.yDir
                self.reward = 1
                self.score += 1
                #self.score = math.floor(self.score + self.xMatrix/10)
                #self.reward = self.xMatrix/10
                print("  HIT> ", str(self.score).zfill(3))

            else:
                print("       ", str(self.score).zfill(3), "  <MISS")
                self.reward = -1
                self.score -= 1

    # LEARNING
    def initiate_Q(self):
        for i in range(len(self.Q_t)):
            for j in range(len(self.Q_t[0])):
                rand = random.uniform(0.1, 0.01)
                self.Q_t[i][j] = rand

    def get_environment(self):
        return [ball.xPos, ball.yPos, ball.xDir, ball.yDir, player.xPos]

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

        action = self.action[self.select_action()]
        player.move(action)
        player.limit_mobility(self.xMatrix)

        ball.move()
        ball.bounce_ball(self.xMatrix, self.yMatrix)
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

    # field
    x, y = 10, 10
    xMid, yMid = x//2, y//2

    speed = 1

    ball = Ball(xMid, yMid, 1, 1)
    player = Player(xMid, 3)

    game = BasicGame("pingpong", x, y, speed, ball, player)
    game.start()
