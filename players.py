import numpy as np
import random
import time
import pygame
import math
from copy import deepcopy
from connect4 import connect4

class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move: list) -> None:
		move = [-1]

class human(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
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

    def simulateMove(self, env: connect4, move: int, playerTurn: int):
        env.board[env.topPosition[move]][move] = playerTurn
        env.topPosition[move] -= 1
        env.history[0].append(move)

    def calculateScore(self, myAICount, none, AICount):
        line_score = 0
        if myAICount == 4:
            line_score += 500
        elif myAICount == 3 and none == 1:
            line_score += 5
        elif myAICount == 2 and none == 2:
            line_score += 1
        if AICount == 4:
            line_score -= 500
        elif AICount == 3 and none == 1:
            line_score -= 5
        elif AICount == 2 and none == 2:
            line_score -= 1
        return line_score

    def checkLine(self, board, playerTurn: int, positions):
        myAICount, AICount, none = 0, 0, 0
        for (i, j) in positions:
            if board[i][j] == playerTurn:
                myAICount += 1
            elif board[i][j] == 0:
                none += 1
            else:
                AICount += 1
        return self.calculateScore(myAICount, none, AICount)

    def horizantalChecks(self, board, playerTurn: int):
        return sum(self.checkLine(board, playerTurn, [(i, j + k) for k in range(4)])
                   for i in range(ROW_COUNT) for j in range(COLUMN_COUNT - 3))

    def verticalChecks(self, board, playerTurn: int):
        return sum(self.checkLine(board, playerTurn, [(i - k, j) for k in range(4)])
                   for i in range(3, ROW_COUNT) for j in range(COLUMN_COUNT))

    def diagonalChecks(self, board, playerTurn: int, direction):
        score = 0
        if direction == 'left':
            for i in range(3, ROW_COUNT):
                for j in range(4):
                    score += self.checkLine(board, playerTurn, [(i - k, j + k) for k in range(4)])
        else:  # right diagonal
            for i in range(3):
                for j in range(4):
                    score += self.checkLine(board, playerTurn, [(i + k, j + k) for k in range(4)])
        return score

    def evalFunction(self, board, playerTurn: int):
        return (self.horizantalChecks(board, playerTurn) +
                self.verticalChecks(board, playerTurn) +
                self.diagonalChecks(board, playerTurn, 'left') +
                self.diagonalChecks(board, playerTurn, 'right'))

    def getBestMove(self, env: connect4, end: int, playerTurn: int, isMaximizingPlayer: bool):
        if env.turnPlayer.position == 2:
            playerPlayed = 0
        else:
            playerPlayed = 1
        if len(env.history[playerPlayed]) > 0 and env.gameOver(env.history[playerPlayed][-1], playerPlayed):
            return env.history[playerPlayed][-1], (5000 if isMaximizingPlayer else -5000)

        if end == 0:
            return 0, self.evalFunction(env.board, playerTurn)

        indices = [i for i, p in enumerate(env.topPosition >= 0) if p]
        bestMove = random.choice(indices)
        bestScore = -float('inf') if isMaximizingPlayer else float('inf')

        for column in indices:
            envCopy = deepcopy(env)
            self.simulateMove(envCopy, column, envCopy.turnPlayer.position)
            envCopy.turnPlayer = envCopy.turnPlayer.opponent
            _, score = self.getBestMove(envCopy, end - 1, playerTurn, not isMaximizingPlayer)
            if isMaximizingPlayer and score > bestScore or not isMaximizingPlayer and score < bestScore:
                bestScore = score
                bestMove = column

        return bestMove, bestScore

    def play(self, env: connect4, move: list) -> None:
        maxDepth = 2
        bestMove, value = self.getBestMove(env, maxDepth, self.position, True)
        move[:] = [bestMove]

class alphaBetaAI(connect4Player):
    def simulateMove(self, env: connect4, move: int, player: int):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        env.history[0].append(move)

    def checkLine(self, myAICount, none, AICount):
        line_score = 0
        if myAICount == 4:
            line_score += 500
        elif myAICount == 3 and none == 1:
            line_score += 5
        elif myAICount == 2 and none == 2:
            line_score += 1
        if AICount == 4:
            line_score -= 500
        elif AICount == 3 and none == 1:
            line_score -= 5
        elif AICount == 2 and none == 2:
            line_score -= 1
        return line_score

    def horizontalChecks(self, board, playerTurn: int):
        score = 0
        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT - 3):
                score += self.checkLine(
                    sum(board[i][j+k] == playerTurn for k in range(4)),
                    sum(board[i][j+k] == 0 for k in range(4)),
                    sum(board[i][j+k] == (3-playerTurn) for k in range(4))
                )
        return score

    def verticalChecks(self, board, playerTurn: int):
        score = 0
        for j in range(COLUMN_COUNT):
            for i in range(ROW_COUNT - 3):
                score += self.checkLine(
                    sum(board[i+k][j] == playerTurn for k in range(4)),
                    sum(board[i+k][j] == 0 for k in range(4)),
                    sum(board[i+k][j] == (3-playerTurn) for k in range(4))
                )
        return score

    def diagonalChecks(self, board, playerTurn: int):
        score = 0
        for i in range(ROW_COUNT - 3):
            for j in range(COLUMN_COUNT - 3):
                score += self.checkLine(
                    sum(board[i+k][j+k] == playerTurn for k in range(4)),
                    sum(board[i+k][j+k] == 0 for k in range(4)),
                    sum(board[i+k][j+k] == (3-playerTurn) for k in range(4))
                )
                if j >= 3:
                    score += self.checkLine(
                        sum(board[i+k][j-k] == playerTurn for k in range(4)),
                        sum(board[i+k][j-k] == 0 for k in range(4)),
                        sum(board[i+k][j-k] == (3-playerTurn) for k in range(4))
                    )
        return score

    def evalFunction(self, board, playerTurn: int):
        return (
            self.horizontalChecks(board, playerTurn)
            + self.verticalChecks(board, playerTurn)
            + self.diagonalChecks(board, playerTurn)
        )
    
    def maxValue(self, env, alpha, beta, end, playerTurn):
        playerPlayed = 1 - env.turnPlayer.position
        if len(env.history[playerPlayed]) > 0 and env.gameOver(env.history[playerPlayed][-1], playerPlayed):
            return env.history[playerPlayed][-1], 5000
        if end == 0:
            return None, self.evalFunction(env.board, playerTurn)
        
        bestScore = -float('inf')
        bestMove = None
        for column in self.getSortedMoves(env):
            envCopy = deepcopy(env)
            self.simulateMove(envCopy, column, envCopy.turnPlayer.position)
            envCopy.turnPlayer = envCopy.turnPlayer.opponent
            _, score = self.minValue(envCopy, alpha, beta, end - 1, playerTurn)
            if score > bestScore:
                bestScore = score
                bestMove = column

            if bestScore >= beta:
                break
            alpha = max(alpha, bestScore)

        return bestMove, bestScore

    def minValue(self, env, alpha, beta, end, playerTurn):
        playerPlayed = 1 - env.turnPlayer.position
        if len(env.history[playerPlayed]) > 0 and env.gameOver(env.history[playerPlayed][-1], playerPlayed):
            return env.history[playerPlayed][-1], -5000
        if end == 0:
            return None, self.evalFunction(env.board, playerTurn)
        
        bestScore = float('inf')
        bestMove = None
        for column in self.getSortedMoves(env):
            envCopy = deepcopy(env)
            self.simulateMove(envCopy, column, envCopy.turnPlayer.position)
            envCopy.turnPlayer = envCopy.turnPlayer.opponent
            _, score = self.maxValue(envCopy, alpha, beta, end - 1, playerTurn)
            if score < bestScore:
                bestScore = score
                bestMove = column

            if bestScore <= alpha:
                break
            beta = min(beta, bestScore)

        return bestMove, bestScore

    def getSortedMoves(self, env):
        possible = [i for i, p in enumerate(env.topPosition >= 0) if p]
        sortedMoves = sorted(possible, key=lambda x: abs(x - 3))
        return sortedMoves
		
    def play(self, env: connect4, move: list) -> None:
        maxDepth = 2
        bestMove, value = self.maxValue(env, -1000000000, 1000000000, maxDepth, self.position)
        move[:] = [bestMove]

SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)



