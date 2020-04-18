import pygame

from LevelGeneration import *
from window import Window
import sprites

import random
from Tiles import Tile

TILE_SIZE = 16


class Board:
    def __init__(self, window: Window, textures: pygame.image, spriteBank: dict):
        self.window = window
        self.textures = textures
        self.rows = window.heigthScaled // TILE_SIZE
        self.cols = window.widthScaled // TILE_SIZE
        self.maxHeight = self.rows * TILE_SIZE
        self.maxWidth = self.cols * TILE_SIZE
        self.tilesBank = spriteBank['tiles']
        self.tilesGroup = sprites.GameSpriteGroup()
        self.boardGrid = []
    # self.tiles = self.initTiles()

    # def initTiles(self):
    #     tiles = []
    #     grassFlowerTiles = self.tilesBank['grassFlower']
    #     for row in range(self.rows):
    #         y = max(TILE_SIZE // 2, min(self.maxHeight - TILE_SIZE, row * TILE_SIZE))
    #         tileRow = []
    #         for col in range(self.cols):
    #             x = max(TILE_SIZE // 2, min(self.maxWidth - TILE_SIZE, col * TILE_SIZE))
    #             texture = self.getRandomTile(grassFlowerTiles)
    #             tile = Tile(texture, self.tilesGroup, x, y)
    #             tileRow.append(tile)
    #         tiles.append(tileRow)
    #     return tiles

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
        newRoom = rooms[randint(0, len(rooms) - 1)](10,line,column,width, height)


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

            newRoom = rooms[randint(0,len(rooms) - 1)]()

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

        newRoom.generateLevel(self.tilesBank)
        return newRoom;


    # def getRandomTile(self, arrs):
    #     n = len(arrs)
    #     row = random.randint(0, n - 1)
    #     m = random.randint(0, len(arrs[row]) - 1)
    #     return arrs[row][m]

    def update(self):
        pass

    def render(self):
        #self.window.get().fill(self.tilesBank['grass'].get_at((0, 0)))
        #self.tilesGroup.draw(self.window.get())
        #print(self.boardGrid);
        for line in self.boardGrid:
            for col in line:
                print(col)
                col.render(self.window.get())
        pass

