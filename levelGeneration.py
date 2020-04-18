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
    def __init__(self):
        self.fixedTiles = []
        self.generatedTiles = []
        self.tiles = []
        self.size = 0
        self.tilesToGenerate = []
        self.enemiesToGenerate = dict()
        self.itemsToGenerate = dict()
        self.enemies = []
        self.items = []
        self.adjacencies = [Adjacency.TOP, Adjacency.BOTTOM, Adjacency.LEFT, Adjacency.RIGHT]
        self.xStart = 0
        self.yStart = 0
        self.tilesGroup = None

    def generateLevel(self, loadedRessources: dict):
        for x in range(self.size):
            for y in range(self.size):
                pass

    def render(self, window):
        self.tilesGroup.draw(window)

    def update(self):
        self.tilesGroup.update();


class BasicRoom(GameRoom):
    #Todo rename cette
    def __init__(self, size, line, column, width, height):
        GameRoom.__init__(self)
        self.size = 0
        self.xStart = config.TILESIZE * width * column;
        self.yStart = config.TILESIZE * height * line

        self.tilesToGenerate.append(tiles.GrassTile);
        self.tilesToGenerate.append(tiles.TreeTiles);
        self.size = size;

    def generateLevel(self, loadedRessources: dict, mark : mark.Mark):

        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)
