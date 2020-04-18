import pygame
import tiles
import config
import mark
from enum import Enum
from random import randint
import sprites

class Adjacency(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


class GameRoom:
    def __init__(self, size, line, column):

        self.fixedTiles = []
        # Wall
        self.physics = [[0 for x in range(size)] for y in range(size)]
        self.fixedWall = []
        self.generatedTiles = []

        self.tiles = []
        self.size = size

        self.tilesToGenerate = []

        self.wallsToGenerate = []
        self.nbWallToGenerate = 0
        self.generatedWall = []

        self.enemiesToGenerate = dict()
        self.itemsToGenerate = dict()

        self.enemies = []
        self.items = []


        self.adjacencies = [Adjacency.TOP, Adjacency.BOTTOM, Adjacency.LEFT, Adjacency.RIGHT]

        self.xStart = config.TILESIZE * size * column
        self.yStart = config.TILESIZE * size * line
        self.tilesGroup = None

    def generateLevel(self, loadedRessources: dict, mark : mark.Mark):
        for x in range(self.size):
            for y in range(self.size):
                pass

    def render(self, window):
        self.tilesGroup.draw(window)

    def update(self):
        self.tilesGroup.update();


class BasicRoom(GameRoom):
    #Todo rename cette
    def __init__(self, size, line, column):
        GameRoom.__init__(self, size, line, column)

        self.tilesToGenerate.append(tiles.GrassTile);
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.size = size;

    def generateLevel(self, loadedRessources: dict, mark : mark.Mark):

        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)


class TreeRoom(GameRoom):
    #Todo rename cette
    def __init__(self, size, line, column):
        GameRoom.__init__(self, size, line, column)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.wallsToGenerate.append((1, 2, tiles.TreeTiles))
        self.nbWallToGenerate = 8;
        self.size = size;

    def generateLevel(self, loadedRessources: dict, mark : mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

        for x in range(self.nbWallToGenerate):
            generated = False
            tryb = 0
            brutcap = 100
            while not generated and tryb < brutcap:
                tryb += 1
                wallToGenerate = self.wallsToGenerate[randint(0, len(self.wallsToGenerate) - 1)]
                generateCoordX = randint(2, len(self.physics) - 4)
                generateCoordY = randint(2, len(self.physics) - 4)

                #Check generation validity
                if self.physics[generateCoordY][generateCoordX] == 0:
                    ycheck = wallToGenerate[1];
                    xcheck = wallToGenerate[0];
                    res = True
                    while ycheck >= 0:
                        for x in range(xcheck):
                            if self.physics[generateCoordY - ycheck][generateCoordX - x] == 1:
                                res = False;
                                break;
                        ycheck -= 1;
                    if res:
                        ycheck = wallToGenerate[1];
                        generated = True
                        while ycheck >= 0:
                            for x in range(xcheck):
                                self.physics[generateCoordY - ycheck][generateCoordX - x] = 1
                            ycheck -= 1
                        tile = wallToGenerate[2](loadedRessources, self.tilesGroup, self.xStart + generateCoordX * config.TILESIZE, self.yStart + generateCoordY * config.TILESIZE, mark)
                        self.generatedWall.append(tile)
                        self.tiles.append(tile)

