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
from copy import deepcopy


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
        blanks = 0
        # 2 5
        for k in range(max(j-1, 0), min(j+n, env.shape[1])):
            if env.board[i][k] == env.board[i][j]:
                count += 1
            elif env.board[i][k] == 0:
                blanks += 1
            else:
                break
        if count == n-1:
            return blanks
        return 0

    def checkNVert(self, env, i, j, n):
        env = env.getEnv()
        count = 0
        blanks = 0
        for k in range(max(i-n+1, 0), i+1):
            if env.board[k][j] == env.board[i][j]:
                count += 1
            elif env.board[k][j] == 0:
                blanks += 1
            else:
                break
        return (count == n-1) and (blanks == 1)

    def checkNDiag(self, env, i, j, n):
        env = env.getEnv()
        count = 0
        blanks = 0
        total = 0
        # column increasing and row increasing (Downward Diagonal)
        col = max(j-1, 0)
        # print(len(range(max(i-1, 0), min(i+n, env.shape[0]))))
        for m in range(max(i-1, 0), min(i+n, env.shape[0])):
            if(col >= min(j+n, env.shape[1])):
                break
            if(env.board[m][col] == env.board[i][j]):
                count += 1
            elif(env.board[m][col] == 0):
                blanks += 1
            else:
                break
            col += 1
        if count == n-1:
            total = blanks
        # Upward Diagonal (column decreasing and row increasing)
        count = 0
        blanks = 0
        col = max(j-1, 0)
        for m in range(min(i+1, env.shape[0]-1), max(i-n+1, 0)-1, -1):
            if(col >= env.shape[1]):
                break
            if(env.board[m][col] == env.board[i][j]):
                count += 1
            elif(env.board[m][col] == 0):
                blanks += 1
            else:
                break
            col += 1
        if count == n-1:
            total += blanks
        # total += (count == n-1) and (blanks == 1)
        return total

    def hasBlankNei(self, env, i, j):
        # check if there is a blank neighbor
        env = env.getEnv()
        for k in range(max(i-1, 0), min(i+2, env.shape[0])):
            for l in range(max(j-1, 0), min(j+2, env.shape[1])):
                if env.board[k][l] == 0:
                    return True
        return False

    def evaluationFunction(self, env):
        env = env.getEnv()
        # Get utility value of board
        # Calculate possible 4s, 3s and 2s in a row
        opponent = 2 if self.position == 1 else 1
        fourRowPlayer = 0
        threeRowPlayer = 0
        twoRowPlayer = 0
        fourRowOpponent = 0
        threeRowOpponent = 0
        twoRowOpponent = 0
        for i in range(env.shape[0]):
            for j in range(env.shape[1]):
                if env.board[i][j] == self.position and self.hasBlankNei(env, i, j):
                    fourRowPlayer += (self.checkNHori(env, i, j, 4) +
                                      self.checkNVert(env, i, j, 4)+self.checkNDiag(env, i, j, 4))
                    threeRowPlayer += (self.checkNHori(env, i, j, 3) +
                                       self.checkNVert(env, i, j, 3)+self.checkNDiag(env, i, j, 3))
                    twoRowPlayer += (self.checkNHori(env, i, j, 2) +
                                     self.checkNVert(env, i, j, 2)+self.checkNDiag(env, i, j, 2))
                elif env.board[i][j] == opponent and self.hasBlankNei(env, i, j):
                    fourRowOpponent += (self.checkNHori(env, i, j, 4) +
                                        self.checkNVert(env, i, j, 4)+self.checkNDiag(env, i, j, 4))
                    threeRowOpponent += (self.checkNHori(env, i, j, 3) +
                                         self.checkNVert(env, i, j, 3)+self.checkNDiag(env, i, j, 3))
                    twoRowOpponent += (self.checkNHori(env, i, j, 2) +
                                       self.checkNVert(env, i, j, 2)+self.checkNDiag(env, i, j, 2))
        print(fourRowPlayer, threeRowPlayer, twoRowPlayer,
              fourRowOpponent, threeRowOpponent, twoRowOpponent)
        return (fourRowPlayer-fourRowOpponent)*100 + (threeRowPlayer-threeRowOpponent)*20 + (twoRowPlayer-twoRowOpponent)

    def getPossibleMoves(self, env, type="max"):
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

    def maxPlayer(self, env, depth):
        env = env.getEnv()
        if depth == 0:
            return self.evaluationFunction(env)
        v = -math.inf
        for i in self.getPossibleMoves(env):
            temp = self.simulateMove(env, i, self.position)
            if temp.gameOver(i, self.position):
                return math.inf
            v = max(v, self.minPlayer(temp, depth-1))
        return v

    def minPlayer(self, env, depth):
        env = env.getEnv()
        if depth == 0:
            return self.evaluationFunction(env)
        v = math.inf
        for i in self.getPossibleMoves(env):
            temp = self.simulateMove(
                env, i, 2 if self.position == 1 else 1)
            if temp.gameOver(i, 2 if self.position == 1 else 1):
                return -math.inf
            v = min(v, self.maxPlayer(temp, depth-1))
        return v

    def minimax(self, env, depth, move):
        env = env.getEnv()
        v = -math.inf
        for i in self.getPossibleMoves(env):
            newBoard = self.simulateMove(env, i, self.position)
            if newBoard.gameOver(i, self.position):
                move[:] = [i]
                return
            newMove = self.minPlayer(newBoard, depth)
            if newMove > v:
                v = newMove
                move[:] = [i]

    def play(self, env, move):
        env = env.getEnv()
        env.visualize = False
        # print(self.checkWin(env))
        # self.getBestMove(env, 3, move)
        self.minimax(env, 1, move)
        # self.minimax(env, 3, move)


class alphaBetaAI(minimaxAI):
    def getPossibleMoves(self, env, type="max"):
        env = env.getEnv()
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        # random.shuffle(indices)
        indices = sorted(indices, key=lambda x: self.evaluationFunction(
            env), reverse=type == "max")
        return indices

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
            if v >= b:
                return v
            a = max(a, v)
        return v

    def minPlayer(self, env, depth, a, b):
        env = env.getEnv()
        if depth == 0:
            return self.evaluationFunction(env)
        v = math.inf
        for i in self.getPossibleMoves(env, "min"):
            temp = self.simulateMove(
                env, i, 2 if self.position == 1 else 1)
            if temp.gameOver(i, 2 if self.position == 1 else 1):
                return -math.inf
            v = min(v, self.maxPlayer(temp, depth-1, a, b))
            if v <= a:
                return v
            b = min(b, v)
        return v

    def abpruning(self, env, depth, move, v=-math.inf):
        env = env.getEnv()
        for i in self.getPossibleMoves(env):
            newBoard = self.simulateMove(env, i, self.position)
            if newBoard.gameOver(i, self.position):
                move[:] = [i]
                return
            newMove = self.minPlayer(newBoard, depth, -math.inf, math.inf)
            # print(newMove)
            if newMove > v:
                v = newMove
                move[:] = [i]
        return v

    def play(self, env, move):
        env = env.getEnv()
        env.visualize = False
        ''' env.board = [[0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 2, 0, 0, 0],
                     [0, 0, 0, 1, 2, 0, 0],
                     [0, 0, 2, 2, 1, 1, 0]] '''

        print(self.evaluationFunction(env))
        # move[:] = [0]
        # v = self.abpruning(env, 1, move)
        self.abpruning(env, 2, move)
        env.visualize = True


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
# remove this line for csif
screen = pygame.display.set_mode(size)
