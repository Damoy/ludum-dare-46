import pygame
from window import Window
from levelGeneration import BasicRoom, Adjacency
import sprites
import mark
from random import randint

TILE_SIZE = 16


class Board:
    def __init__(self, window: Window, textures: pygame.image, spriteBank: dict, mark: mark.Mark):
        self.mark = mark;
        self.window = window
        self.textures = textures
        self.rows = window.heigthScaled // TILE_SIZE
        self.cols = window.widthScaled // TILE_SIZE
        self.maxHeight = self.rows * TILE_SIZE
        self.maxWidth = self.cols * TILE_SIZE
        self.spriteBank = spriteBank
        self.tilesGroup = sprites.GameSpriteGroup()
        self.boardGrid = []


    def initBoard(self, width, height):
        self.boardGrid = [[None for x in range(width)] for y in range(height)];
        v = 0
        for y in range(width):
            v += 1
            for x in range(height):
                room = self.generateRoom(y, x, width, height);
                self.boardGrid[x][y] = room;

    def generateRoom(self, line, column, width, height):
        #TODO stuff
        #like LevelMAnager.getArray
        rooms = [BasicRoom];
        newRoom = rooms[randint(0, len(rooms) - 1)](self.textures, 10, line, column, width, height)

        possibleTop = (Adjacency.TOP in newRoom.adjacencies and
                       ((line == 0) or self.boardGrid[line - 1][column] is None or Adjacency.BOTTOM in self.boardGrid[line - 1][column].adjacencies )
                       or not (Adjacency.TOP in newRoom.adjacencies))

        possibleBottom = (Adjacency.BOTTOM in newRoom.adjacencies and
                          ((line == len(self.boardGrid) - 1) or self.boardGrid[line + 1][column] is None or Adjacency.TOP in self.boardGrid[line + 1][column].adjacencies  )
                          or not (Adjacency.BOTTOM in newRoom.adjacencies))

        possibleLEFT = (Adjacency.LEFT in newRoom.adjacencies and
                        ((column == 0) or self.boardGrid[line][column - 1] is None or Adjacency.RIGHT in self.boardGrid[line][column - 1].adjacencies  )
                        or not (Adjacency.LEFT in newRoom.adjacencies))

        possibleRight = (Adjacency.RIGHT in newRoom.adjacencies and
                         ((column == len(self.boardGrid[0]) - 1) or self.boardGrid[line][column + 1] is None or Adjacency.LEFT in self.boardGrid[line][column + 1].adjacencies )
                         or not (Adjacency.RIGHT in newRoom.adjacencies))


        while not (possibleTop and possibleBottom and possibleLEFT and possibleRight):

            newRoom = rooms[randint(0, len(rooms) - 1)](self.textures)

            possibleTop = (Adjacency.TOP in newRoom.adjacencies and
                           ((line == 0) or self.boardGrid[line - 1][column] is None or Adjacency.BOTTOM in
                            self.boardGrid[line - 1][column].adjacencies)
                           or not (Adjacency.TOP in newRoom.adjacencies))

            possibleBottom = (Adjacency.BOTTOM in newRoom.adjacencies and
                              ((line == len(self.boardGrid) - 1) or self.boardGrid[line + 1][
                                  column] is None or Adjacency.TOP in self.boardGrid[line + 1][column].adjacencies)
                              or not (Adjacency.BOTTOM in newRoom.adjacencies))

            possibleLEFT = (Adjacency.LEFT in newRoom.adjacencies and
                            ((column == 0) or self.boardGrid[line][column - 1] is None or Adjacency.RIGHT in
                             self.boardGrid[line][column - 1].adjacencies)
                            or not (Adjacency.LEFT in newRoom.adjacencies))

            # print(self.boardGrid)
            possibleRight = (Adjacency.RIGHT in newRoom.adjacencies and
                             ((column == len(self.boardGrid[0])) or self.boardGrid[line][
                                 column + 1] is None or Adjacency.LEFT in self.boardGrid[line][column + 1].adjacencies)
                             or not (Adjacency.RIGHT in newRoom.adjacencies))

        newRoom.generateLevel(self.spriteBank, self.mark)
        return newRoom;


    # def getRandomTile(self, arrs):
    #     n = len(arrs)
    #     row = random.randint(0, n - 1)
    #     m = random.randint(0, len(arrs[row]) - 1)
    #     return arrs[row][m]

    def update(self):
        for line in self.boardGrid:
            for col in line:
                col.update()

    def render(self):
        for line in self.boardGrid:
            for col in line:
                col.render(self.window.get())
        pass

