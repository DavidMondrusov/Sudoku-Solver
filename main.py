from solver import Solver
from sudokuTables import Tables
import numpy as np
import pygame
import sys
import copy

pygame.init()
pygame.display.set_caption("Backtracking Sudoku Solver")
res = (700, 700)
white = (255, 255, 255)
smallfont = pygame.font.SysFont("Corbel", 40)
numfont = pygame.font.SysFont("Corbel", 45)
solveText = smallfont.render("Solve", True, (100, 100, 100))
resetText = smallfont.render("Reset", True, (100, 100, 100))
screen = pygame.display.set_mode(res)
SCREENWIDTH = screen.get_width()
SCREENHEIGHT = screen.get_height()
block_size = 500 / 9


class Game:
    def __init__(self):
        self.table = Tables()
        self.solver = Solver()
        self.SudokuTable = copy.deepcopy(self.table.getTable())

    def change(self, x, y, num):
        self.SudokuTable[x][y] = num
        if num != 0 and not self.solver.constraints(self.SudokuTable, x, y, num):
            return False
        return self.check()

    def drawGrid(self):
        for i in range(10):
            lineSize = 1
            if i % 3 == 0:
                lineSize = 3
            pygame.draw.line(
                screen,
                (0, 0, 0),
                (100, 100 + i * block_size),
                (600, 100 + i * block_size),
                lineSize,
            )
            pygame.draw.line(
                screen,
                (0, 0, 0),
                (100 + i * block_size, 100),
                (100 + i * block_size, 600),
                lineSize,
            )

    def drawBox(self, x, y):
        for i in range(2):
            pygame.draw.line(
                screen,
                (40, 40, 40),
                (100 + x * block_size, 100 + (y + i) * block_size),
                (100 + block_size + x * block_size, 100 + (y + i) * block_size),
                3,
            )
            pygame.draw.line(
                screen,
                (40, 40, 40),
                (100 + (x + i) * block_size, 100 + y * block_size),
                (100 + (x + i) * block_size, 100 + block_size + y * block_size),
                3,
            )

    def drawNumbers(self):
        for x in range(9):
            for y in range(9):
                if self.SudokuTable[x][y] != 0:
                    text = numfont.render(
                        str(self.SudokuTable[x][y]), True, (100, 100, 100)
                    )
                    screen.blit(text, (117 + x * block_size, 117 + y * block_size))

    def check(self):
        tempTable = copy.deepcopy(self.SudokuTable)
        return self.solver.solve(tempTable, 0, 0)

    def start(self):
        self.solver.solve(self.SudokuTable, 0, 0)
        return self.solver.recursions()

    def reset(self):
        self.table.randomTable()
        self.SudokuTable = copy.deepcopy(self.table.getTable())


running = True
game = Game()
solved = False
solvable = True

select = False
xSel = -1
ySel = -1
recNum = 0
while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (
                solvable
                and not solved
                and 190 <= mouse[0] <= 190 + 130
                and 30 <= mouse[1] <= 30 + 40
            ):
                recNum = game.start()
                solved = True
            if (
                SCREENWIDTH - 190 - 130 <= mouse[0] <= SCREENWIDTH - 190
                and 30 <= mouse[1] <= 30 + 40
            ):
                game.reset()
                select = False
                solved = False
                solvable = True
            if 100 <= mouse[0] <= 600 and 100 <= mouse[1] <= 600:
                select = True
                xSel = int((mouse[0] - 100) // block_size)
                ySel = int((mouse[1] - 100) // block_size)
        if select and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and xSel != 0:
                xSel -= 1
            if event.key == pygame.K_RIGHT and xSel != 8:
                xSel += 1
            if event.key == pygame.K_UP and ySel != 0:
                ySel -= 1
            if event.key == pygame.K_DOWN and ySel != 8:
                ySel += 1
            if event.key == pygame.K_BACKSPACE:
                solvable = game.change(xSel, ySel, 0)
                solved = False
            if event.key == pygame.K_1:
                solvable = game.change(xSel, ySel, 1)
            if event.key == pygame.K_2:
                solvable = game.change(xSel, ySel, 2)
            if event.key == pygame.K_3:
                solvable = game.change(xSel, ySel, 3)
            if event.key == pygame.K_4:
                solvable = game.change(xSel, ySel, 4)
            if event.key == pygame.K_5:
                solvable = game.change(xSel, ySel, 5)
            if event.key == pygame.K_6:
                solvable = game.change(xSel, ySel, 6)
            if event.key == pygame.K_7:
                solvable = game.change(xSel, ySel, 7)
            if event.key == pygame.K_8:
                solvable = game.change(xSel, ySel, 8)
            if event.key == pygame.K_9:
                solvable = game.change(xSel, ySel, 9)

    screen.fill(pygame.Color("aquamarine"))
    pygame.draw.rect(screen, (170, 170, 170), [193, 33, 124, 34])
    pygame.draw.rect(screen, (150, 150, 150), [190, 30, 130, 40], 3, 4)

    pygame.draw.rect(screen, (170, 170, 170), [SCREENWIDTH - 190 - 127, 33, 124, 34])
    pygame.draw.rect(
        screen, (150, 150, 150), [SCREENWIDTH - 190 - 130, 30, 130, 40], 3, 4
    )

    screen.blit(
        solveText,
        (
            190 + (130 - solveText.get_rect().width) / 2,
            30 + (40 - solveText.get_rect().height) / 2,
        ),
    )
    screen.blit(
        resetText,
        (
            SCREENWIDTH - 190 - 130 + ((130 - resetText.get_rect().width) / 2),
            30 + (40 - resetText.get_rect().height) / 2,
        ),
    )
    game.drawGrid()
    game.drawNumbers()
    if not solvable:
        fail = smallfont.render(f"Unsolvable", True, (100, 100, 100))
        screen.blit(
            fail,
            (SCREENWIDTH - 100 - fail.get_rect().width, SCREENHEIGHT - 70),
        )

    if select:
        game.drawBox(xSel, ySel)
    if solved:
        recursionsText = smallfont.render(
            f"Recursions: {recNum}", True, (100, 100, 100)
        )
    else:
        recursionsText = smallfont.render(f"Recursions:", True, (100, 100, 100))
    screen.blit(
        recursionsText,
        (100, SCREENHEIGHT - 70),
    )

    pygame.display.flip()

pygame.quit()
