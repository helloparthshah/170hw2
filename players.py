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
    def CalcStraight(self, env, n):
        env = env.getEnv()
        RowPlayer = 0
        RowOpponent = 0
        opponent = 2 if self.position == 1 else 1
        # Horizontal
        for row in range(env.shape[0]):
            for col in range(env.shape[1]-(n-1)):
                countSelf = 0
                countOpp = 0
                countBlank = 0
                for i in range(n):
                    if env.board[row][col+i] == self.position:
                        countSelf += 1
                    elif env.board[row][col+i] == opponent:
                        countOpp += 1
                    else:
                        countBlank += 1
                RowPlayer += (countSelf >= n-1 and countBlank == 1)
                RowOpponent += (countOpp >= n-1 and countBlank == 1)
        # Vertical
        for col in range(env.shape[1]):
            for row in range(env.shape[0]-(n-1)):
                countSelf = 0
                countOpp = 0
                countBlank = 0
                for i in range(n):
                    if env.board[row+i][col] == self.position:
                        countSelf += 1
                    elif env.board[row+i][col] == opponent:
                        countOpp += 1
                    else:
                        countBlank += 1
                RowPlayer += (countSelf >= n-1 and countBlank == 1)
                RowOpponent += (countOpp >= n-1 and countBlank == 1)
        # Diagonal
        for row in range(env.shape[0]-(n-1)):
            for col in range(env.shape[1]-(n-1)):
                countSelf = 0
                countOpp = 0
                countBlank = 0
                for i in range(n):
                    if env.board[row+i][col+i] == self.position:
                        countSelf += 1
                    elif env.board[row+i][col+i] == opponent:
                        countOpp += 1
                    else:
                        countBlank += 1
                RowPlayer += (countSelf >= n-1 and countBlank == 1)
                RowOpponent += (countOpp >= n-1 and countBlank == 1)
        for row in range(env.shape[0]-(n-1)):
            for col in range(n-1, env.shape[1]):
                countSelf = 0
                countOpp = 0
                countBlank = 0
                for i in range(n):
                    if env.board[row+i][col-i] == self.position:
                        countSelf += 1
                    elif env.board[row+i][col-i] == opponent:
                        countOpp += 1
                    else:
                        countBlank += 1
                RowPlayer += (countSelf >= n-1 and countBlank == 1)
                RowOpponent += (countOpp >= n-1 and countBlank == 1)
        return RowPlayer, RowOpponent

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
        fourRowPlayer, fourRowOpponent = self.CalcStraight(env, 4)
        threeRowPlayer, threeRowOpponent = self.CalcStraight(env, 3)
        twoRowPlayer, twoRowOpponent = self.CalcStraight(env, 2)
        ''' print(fourRowPlayer, threeRowPlayer, twoRowPlayer,
              fourRowOpponent, threeRowOpponent, twoRowOpponent) '''
        return (fourRowPlayer-fourRowOpponent*2)*1000 + (threeRowPlayer-threeRowOpponent*2)*10 + (twoRowPlayer-twoRowOpponent)*2

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
            newMove = self.minPlayer(newBoard, depth-1)
            if newMove > v:
                v = newMove
                move[:] = [i]

    def play(self, env, move):
        env = env.getEnv()
        env.visualize = False
        self.minimax(env, 2, move)


class alphaBetaAI(minimaxAI):
    def getPossibleMoves(self, env, type="max"):
        env = env.getEnv()
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        random.shuffle(indices)
        # Sort based on evaluation function
        ''' if type == "max":
            indices.sort(key=lambda x: self.evaluationFunction(
                self.simulateMove(env, x, self.position)), reverse=True)
        else:
            indices.sort(key=lambda x: self.evaluationFunction(
                self.simulateMove(env, x, 2 if self.position == 1 else 1))) '''
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
            newMove = self.minPlayer(newBoard, depth-1, -math.inf, math.inf)
            # print(newMove)
            if newMove > v:
                v = newMove
                move[:] = [i]
        return v

    def play(self, env, move):
        env = env.getEnv()
        env.visualize = False
        self.abpruning(env, 2, move)


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
