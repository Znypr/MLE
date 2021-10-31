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
alpha = 0.9  # [0,1]
epsilon = 0.2  # [0,1]
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
    windowName = "y:" + str(gamma) + " a:" + str(alpha) + " e:" + str(epsilon)
    pixelSize = 30
    n = 0.3  # [0,5]
    score = 0
    reward = 0

    xMatrix, yMatrix = 5, 5
    xBall, yBall = (xMatrix // 2), (yMatrix // 2)
    xPlayer, wPlayer = (xMatrix // 2), 1
    xV, yV = 1, 1

    amount_states = xMatrix ** 2 * 4 * (xMatrix - (wPlayer-1))
    limit = [xMatrix, yMatrix, 1, 1, (xMatrix - (wPlayer-1))]
    action = [-1, 0, 1]
    Q_t = np.zeros((amount_states, len(action)))


    # ENGINE
    def __init__(self, name, width=pixelSize * xMatrix, height=pixelSize * yMatrix):
        super
        self.windowName = name
        self.width = width
        self.height = height

    def keyboard(self, key, x, y):
        # ESC = \x1w
        if key == b'\x1b':
            glutLeaveMainLoop()
            sys.exit(0)

    def start(self):
        self.initiate_Q()
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(self.toCString(self.windowName))
        # self.init()

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

    def draw_ball(self, width=1, height=1, x=xBall, y=yBall, color=(0.0, 1.0, 0.0)):
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

    def draw_player(self, width=wPlayer, height=1, color=(1.0, 0.0, 0.0)):

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

            # player-ball collision
            if self.xBall >= self.xPlayer and self.xBall <= self.xPlayer + self.wPlayer - 1:
                # bounce ball on player
                self.yV = -self.yV
                self.score = self.score + self.xMatrix/10
                self.reward = self.xMatrix/10
                print("HIT > ", self.score)
            else:
                print("      ", self.score, " < MISS")
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

    def get_reward(self, action):
        return self.Q_t[self.state][action]

    def update_Q_t(self, new_state, action):
        val, idx = self.get_max(self.Q_t[new_state])
        self.Q_t[self.state][action] = self.Q_t[self.state][action] + \
                                       alpha * (self.reward + gamma * val - self.Q_t[self.state][action])

    def run(self):

        self.display()

        action = self.select_action()
        self.move_player(action)
        self.limit_player_reach()

        self.move_ball()
        self.bounce_ball()

        self.handle_collision()

        new_state = self.get_state()
        self.update_Q_t(new_state, action)

        self.draw_ball()
        self.draw_player()

        self.state = new_state

        # adaptive speed depending on matrix size
        time.sleep(self.n / (self.xMatrix * self.yMatrix))

        glutSwapBuffers()


if __name__ == '__main__':
    game = BasicGame("y:" + str(gamma) + " a:" + str(alpha) + " e:" + str(epsilon))
    game.start()
