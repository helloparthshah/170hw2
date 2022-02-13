from itertools import count
import random
import re
from tabnanny import check
import time
from turtle import position
import pygame
import math
import os
import sys


class connect4Player(object):
    def __init__(self, position, seed=0):
        self.position = position
        self.opponent = None
        self.seed = seed
        random.seed(seed)

    def play(self, env, move):
        move = [-1]


class human(connect4Player):

    def play(self, env, move):
        move[:] = [int(input('Select next move: '))]
        while True:
            if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
                break
            move[:] = [int(input('Index invalid. Select next move: '))]


class human2(connect4Player):

    def play(self, env, move):
        done = False
        while(not done):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.position == 1:
                        pygame.draw.circle(
                            screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                    else:
                        pygame.draw.circle(
                            screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
                    move[:] = [col]
                    done = True


class randomAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        move[:] = [random.choice(indices)]


class stupidAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        if 3 in indices:
            move[:] = [3]
        elif 2 in indices:
            move[:] = [2]
        elif 1 in indices:
            move[:] = [1]
        elif 5 in indices:
            move[:] = [5]
        elif 6 in indices:
            move[:] = [6]
        else:
            move[:] = [0]


class minimaxAI(connect4Player):
    def checkNHori(self, env, i, j, n):
        env = env.getEnv()
        count = 0
        for k in range(j, min(j+n, env.shape[1])):
            if env.board[i][k] == env.board[i][j]:
                count += 1
            else:
                break
        return (count >= n)

    def checkNVert(self, env, i, j, n):
        env = env.getEnv()
        count = 0
        for k in range(i, env.shape[0]):
            if env.board[k][j] == env.board[i][j]:
                count += 1
            else:
                break
        return (count >= n)

    def checkNDiag(self, env, i, j, n):
        env = env.getEnv()
        total = 0
        count = 0
        col = j
        for a in range(i, env.shape[0]):
            if col < env.shape[0]:
                if env.board[a][col] == env.board[i][j]:
                    count += 1
                else:
                    break
                col += 1
        if count >= n:
            total += 1
        count = 0
        col = j
        for k in range(i, -1, -1):
            if col > env.shape[0]:
                break
            elif env.board[k][col] == env.board[i][j]:
                count += 1
            else:
                break
            col += 1
        if count >= n:
            total += 1
        return total

    def evaluationFunction(self, env):
        env = env.getEnv()
        # Get utility value of board
        # Calculate possible 4s, 3s and 2s in a row
        fourRowPlayer = 0
        threeRowPlayer = 0
        twoRowPlayer = 0
        fourRowOpponent = 0
        threeRowOpponent = 0
        twoRowOpponent = 0
        for i in range(env.shape[0]):
            for j in range(env.shape[1]):
                if env.board[i][j] == self.position:
                    fourRowPlayer += (self.checkNHori(env, i, j, 4) +
                                      self.checkNVert(env, i, j, 4)+self.checkNDiag(env, i, j, 4))
                    threeRowPlayer += (self.checkNHori(env, i, j, 3) +
                                       self.checkNVert(env, i, j, 3)+self.checkNDiag(env, i, j, 3))
                    twoRowPlayer += (self.checkNHori(env, i, j, 2) +
                                     self.checkNVert(env, i, j, 2)+self.checkNDiag(env, i, j, 2))
                elif env.board[i][j] != 0:
                    fourRowOpponent += 2*(self.checkNHori(env, i, j, 4) +
                                          self.checkNVert(env, i, j, 4)+self.checkNDiag(env, i, j, 4))
                    threeRowOpponent += 2*(self.checkNHori(env, i, j, 3) +
                                           self.checkNVert(env, i, j, 3)+self.checkNDiag(env, i, j, 3))
                    twoRowOpponent += 2*(self.checkNHori(env, i, j, 2) +
                                         self.checkNVert(env, i, j, 2)+self.checkNDiag(env, i, j, 2))
        # print(fourRowPlayer, threeRowPlayer, twoRowPlayer,
        #       fourRowOpponent, threeRowOpponent, twoRowOpponent)
        return (fourRowPlayer-fourRowOpponent)*10 + (threeRowPlayer-threeRowOpponent)*5 + (twoRowPlayer-twoRowOpponent)*2

    def checkWin(self, env):
        env = env.getEnv()
        for i in range(env.shape[0]):
            for j in range(env.shape[1]):
                if env.board[i][j] != 0:
                    if self.checkNHori(env, i, j, 4):
                        return env.board[i][j]
                    elif self.checkNVert(env, i, j, 4):
                        return env.board[i][j]
                    elif self.checkNDiag(env, i, j, 4):
                        return env.board[i][j]
        return 0

    def simulateMove(self, env, move, player):
        env = env.getEnv()
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        env.history[0].append(move)
        return env

    def maxPlayer(self, env, depth):
        env = env.getEnv()
        """ if self.checkWin(env):
            return -math.inf """
        if depth == 0:
            return self.evaluationFunction(env)
        v = -math.inf
        for i in range(env.shape[1]):
            if env.topPosition[i] >= 0:
                temp = self.simulateMove(env, i, self.position)
                if temp.gameOver(i, self.position):
                    return math.inf
                v = max(v, self.minPlayer(temp, depth-1))
        return v

    def minPlayer(self, env, depth):
        env = env.getEnv()
        """ if self.checkWin(env):
            return math.inf """
        if depth == 0:
            return self.evaluationFunction(env)
        v = math.inf
        for i in range(env.shape[1]):
            if env.topPosition[i] >= 0:
                temp = self.simulateMove(
                    env, i, 2 if self.position == 1 else 1)
                if temp.gameOver(i, 2 if self.position == 1 else 1):
                    return -math.inf
                v = min(v, self.maxPlayer(temp, depth-1))
        return v

    def minimax(self, env, depth, move):
        env = env.getEnv()
        v = -math.inf
        for i in range(env.shape[1]):
            if env.topPosition[i] >= 0:
                newBoard = self.simulateMove(env, i, self.position)
                if newBoard.gameOver(i, self.position):
                    move[:] = [i]
                    return
                """ if self.checkWin(newBoard):
                    move[:] = [i]
                    return """
                newMove = self.minPlayer(newBoard, depth)
                print(newMove)
                if newMove > v:
                    v = newMove
                    move[:] = [i]

    def play(self, env, move):
        env = env.getEnv()
        env.visualize = False
        # print(self.checkWin(env))
        # self.getBestMove(env, 3, move)
        self.minimax(env, 0, move)
        # self.minimax(env, 3, move)


class alphaBetaAI(connect4Player):
    def checkNHori(self, env, i, j, n):
        env = env.getEnv()
        count = 0
        for k in range(j, env.shape[1]):
            if env.board[i][k] == env.board[i][j]:
                count += 1
            elif env.board[i][k] != 0:
                break
        return (count >= n-1)

    def checkNVert(self, env, i, j, n):
        env = env.getEnv()
        count = 0
        for k in range(i, env.shape[0]):
            if env.board[k][j] == env.board[i][j]:
                count += 1
            elif env.board[k][j] != 0:
                break
        return (count >= n-1)

    def checkNDiag(self, env, i, j, n):
        env = env.getEnv()
        total = 0
        count = 0
        col = j
        for a in range(i, env.shape[0]):
            if col < env.shape[0]:
                if env.board[a][col] == env.board[i][j]:
                    count += 1
                elif env.board[a][col] != 0:
                    break
                col += 1
        if count >= n-1:
            total += 1
        count = 0
        col = j
        for k in range(i, -1, -1):
            if col > env.shape[0]:
                break
            elif env.board[k][col] == env.board[i][j]:
                count += 1
            elif env.board[k][col] != 0:
                break
            col += 1
        if count >= n-1:
            total += 1
        return total

    def evaluationFunction(self, env):
        env = env.getEnv()
        # Get utility value of board
        # Calculate possible 4s, 3s and 2s in a row
        fourRowPlayer = 0
        threeRowPlayer = 0
        twoRowPlayer = 0
        fourRowOpponent = 0
        threeRowOpponent = 0
        twoRowOpponent = 0
        for i in range(env.shape[0]):
            for j in range(env.shape[1]):
                if env.board[i][j] == self.position:
                    fourRowPlayer += (self.checkNHori(env, i, j, 4) +
                                      self.checkNVert(env, i, j, 4)+self.checkNDiag(env, i, j, 4))
                    threeRowPlayer += (self.checkNHori(env, i, j, 3) +
                                       self.checkNVert(env, i, j, 3)+self.checkNDiag(env, i, j, 3))
                    twoRowPlayer += (self.checkNHori(env, i, j, 2) +
                                     self.checkNVert(env, i, j, 2)+self.checkNDiag(env, i, j, 2))
                elif env.board[i][j] != 0:
                    fourRowOpponent += (self.checkNHori(env, i, j, 4) +
                                        self.checkNVert(env, i, j, 4)+self.checkNDiag(env, i, j, 4))
                    threeRowOpponent += (self.checkNHori(env, i, j, 3) +
                                         self.checkNVert(env, i, j, 3)+self.checkNDiag(env, i, j, 3))
                    twoRowOpponent += (self.checkNHori(env, i, j, 2) +
                                       self.checkNVert(env, i, j, 2)+self.checkNDiag(env, i, j, 2))
        # print(fourRowPlayer, threeRowPlayer, twoRowPlayer,
        #       fourRowOpponent, threeRowOpponent, twoRowOpponent)
        return (fourRowPlayer-fourRowOpponent)*20 + (threeRowPlayer-threeRowOpponent)*10 + (twoRowPlayer-twoRowOpponent)*2

    def checkWin(self, env):
        env = env.getEnv()
        for i in range(env.shape[0]):
            for j in range(env.shape[1]):
                if env.board[i][j] != 0:
                    if self.checkNHori(env, i, j, 4):
                        return env.board[i][j]
                    elif self.checkNVert(env, i, j, 4):
                        return env.board[i][j]
                    elif self.checkNDiag(env, i, j, 4):
                        return env.board[i][j]
        return 0

    def getPossibleMoves(self, env):
        env = env.getEnv()
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        random.shuffle(indices)
        return indices

    def simulateMove(self, env, move, player):
        env = env.getEnv()
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        env.history[0].append(move)
        return env

    def maxPlayer(self, env, depth, a, b):
        env = env.getEnv()
        if depth == 0:
            return self.evaluationFunction(env)
        v = -math.inf
        for i in self.getPossibleMoves(env):
            temp = self.simulateMove(env, i, self.position)
            if temp.gameOver(i, self.position):
                return math.inf
            v = max(v, self.minPlayer(temp, depth-1, a, b))
            if v <= a:
                return v
            b = min(b, v)
        return v

    def minPlayer(self, env, depth, a, b):
        env = env.getEnv()
        if depth == 0:
            return self.evaluationFunction(env)
        v = math.inf
        for i in self.getPossibleMoves(env):
            temp = self.simulateMove(
                env, i, 2 if self.position == 1 else 1)
            if temp.gameOver(i, 2 if self.position == 1 else 1):
                return -math.inf
            v = min(v, self.maxPlayer(temp, depth-1, a, b))
            if v >= b:
                return v
            a = max(a, v)
        return v

    def abpruning(self, env, depth, move):
        env = env.getEnv()
        v = -math.inf
        for i in self.getPossibleMoves(env):
            newBoard = self.simulateMove(env, i, self.position)
            if newBoard.gameOver(i, self.position):
                move[:] = [i]
                return
            newMove = self.minPlayer(newBoard, depth, -math.inf, math.inf)
            if newMove > v:
                v = newMove
                move[:] = [i]

    def play(self, env, move):
        env = env.getEnv()
        env.visualize = False
        print(self.evaluationFunction(env))
        self.abpruning(env, 3, move)


SQUARESIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
