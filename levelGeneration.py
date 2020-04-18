import pygame
import tiles
import config
import mark
from enum import Enum
from random import randint
import sprites
import mob

class Adjacency(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


class GameRoom:
    def __init__(self, textures: pygame.image):
        self.textures = textures
        self.fixedTiles = []
        self.generatedTiles = []
        self.tiles = []
        self.size = 0
        self.tilesToGenerate = []
        self.enemiesToGenerate = {}
        self.itemsToGenerate = {}
        self.enemies = sprites.GameSpriteGroup()
        self.items = []
        self.adjacencies = [Adjacency.TOP, Adjacency.BOTTOM, Adjacency.LEFT, Adjacency.RIGHT]
        self.xStart = 0
        self.yStart = 0
        self.tilesGroup = None

    def generateLevel(self, loadedRessources: dict):
        # for x in range(self.size):
        #     for y in range(self.size):
        pass

    def render(self, window):
        if self.tilesGroup:
            self.tilesGroup.draw(window)
        if self.enemies:
            self.enemies.draw(window)

    def update(self):
        if self.tilesGroup:
            self.tilesGroup.update()
        if self.enemies:
            self.enemies.update()

    def getRandomX(self):
        return 0

    def getRandomY(self):
        return 0

    def buildMobs(self):
        pass

    def generateTiles(self):
        pass

    def generateMobs(self):
        pass

class BasicRoom(GameRoom):
    #Todo rename cette
    def __init__(self, textures: pygame.image, size, line, column, width, height):
        GameRoom.__init__(self, textures)
        self.size = 0
        self.xStart = config.TILESIZE * width * column;
        self.yStart = config.TILESIZE * height * line

        self.tilesToGenerate.append(tiles.GrassTile);
        self.tilesToGenerate.append(tiles.TreeTiles);
        self.size = size;
        self.buildMobs()

    def buildMobs(self):
        self.enemiesToGenerate[mob.Gobelin] = 1

    def generateLevel(self, spriteBank: dict, mark : mark.Mark):
        self.generateTiles(spriteBank['tiles'], mark)
        self.generateMobs(spriteBank, mark)

    def generateTiles(self, loadedRessources: dict, mark : mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

    # self, x, y, group: sprites.GameSpriteGroup,
    # spriteBank: dict, mark: mark, textures: pygame.image, gameRoom: board.GameRoom

    def generateMobs(self, spriteBank: dict, mark: mark.Mark):
        for mobClass in self.enemiesToGenerate:
            for nb in range(self.enemiesToGenerate[mobClass]):
                x = self.getRandomX() # TODO
                y = self.getRandomY()
                m = mobClass(x, y, self.enemies, spriteBank, mark, self.textures)
                self.enemies.add(m)
