
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Cell(object):
    def __init__(self, live, x, y):
        self.live = live
        self.x = x
        self.y = y
        self.neighbors = []

def draw(surface):
    global liveCellsCoords
    for y in range(0, int(GRIDSIZE)):
        for x in range(0, int(GRIDSIZE)):
            rBorder = pygame.Rect((x * GRID_WIDTH, y * GRID_HEIGHT), (GRID_WIDTH, GRID_HEIGHT))
            r = pygame.Rect((x * GRID_WIDTH, y * GRID_HEIGHT), (GRID_WIDTH - 1, GRID_HEIGHT - 1))
            pygame.draw.rect(surface, (255, 255, 255), rBorder)
            if (x, y) in liveCellsCoords:
                pygame.draw.rect(surface, (0, 255, 0), r)
            else:
                pygame.draw.rect(surface, (0, 0, 0), r)

def initCells():
    global cells
    global liveCellsCoords
    cell = None
    for y in range(0, int(GRIDSIZE)):
        for x in range(0, int(GRIDSIZE)):
            coords = (x, y)
            if coords in liveCellsCoords:
                cell = Cell(True, x, y)
            else:
                cell = Cell(False, x, y)
            cells.append(cell)

def initLiveCellsCoords():
    global liveCellsCoords
    middleOfBoard = (GRIDSIZE / 2 - 1, GRIDSIZE / 2 - 1)
    left = (middleOfBoard[0] - 1, middleOfBoard[1])
    right = (middleOfBoard[0] + 1, middleOfBoard[1])
    top = (middleOfBoard[0], middleOfBoard[1] + 1)
    bottom = (middleOfBoard[0], middleOfBoard[1] - 1)
    diagLeftTop = (middleOfBoard[0] - 1, middleOfBoard[1] + 1)
    diagLeftBottom = (middleOfBoard[0] - 1, middleOfBoard[1] - 1)
    diagRightTop = (middleOfBoard[0] + 1, middleOfBoard[1] + 1)
    diagRightBottom = (middleOfBoard[0] + 1, middleOfBoard[1] - 1)
    liveCellsCoords = [middleOfBoard, left, right, top, bottom, diagLeftTop, diagLeftBottom, diagRightTop, diagRightBottom]

    leftCross = [(middleOfBoard[0] - 3, middleOfBoard[1]), (left[0] - 3, left[1]), (right[0] - 3, right[1]), (top[0] - 3, top[1]), (bottom[0] - 3, bottom[1])]
    rightCross = [(middleOfBoard[0] + 3, middleOfBoard[1]), (left[0] + 3, left[1]), (right[0] + 3, right[1]), (top[0] + 3, top[1]), (bottom[0] + 3, bottom[1])]

    liveCellsCoords += leftCross + rightCross
    #print(str(liveCellsCoords))

def setCellNeighbors():
    global cells
    for cell in cells:
        for i in range(0, len(cells)):
            if cell.y == cells[i].y and (cell.x - 1 == cells[i].x or cell.x + 1 == cells[i].x):
                cell.neighbors.append(cells[i])
            elif cell.x == cells[i].x and (cell.y - 1 == cells[i].y or cell.y + 1 == cells[i].y):
                cell.neighbors.append(cells[i])
            elif cell.x - 1 == cells[i].x and (cell.y - 1 == cells[i].y or cell.y + 1 == cells[i].y):
                cell.neighbors.append(cells[i])
            elif cell.x + 1 == cells[i].x and (cell.y - 1 == cells[i].y or cell.y + 1 == cells[i].y):
                cell.neighbors.append(cells[i])

def updateCells():
    #print('updateCells')
    global cells
    global liveCellsCoords
    for cell in cells:
        liveNeighborCount = 0
        for c in cell.neighbors:
            if c.live:
                liveNeighborCount += 1

        if not cell.live:
            if liveNeighborCount == 3:
                cell.live = True
                liveCellsCoords.append((cell.x, cell.y))
        elif liveNeighborCount < 2 or liveNeighborCount > 3:
            cell.live = False
            liveCellsCoords.remove((cell.x, cell.y))

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRIDSIZE = 50
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE

cells = []
liveCellsCoords = []

def main():
    initLiveCellsCoords()
    initCells()
    setCellNeighbors()

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size()).convert()

    running = True
    while running:
        clock.tick(4)
        draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
        updateCells()

if __name__ == '__main__':
    main()