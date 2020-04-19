import pygame
import tiles
import config
import mark
from enum import Enum
from random import randint
import sprites
import mob
import item
import random
import text

class Adjacency(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    ALL = 4


class GameRoom:
    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        self.player = player
        self.textures = textures
        self.fixedTiles = []
        self.texts = texts
        # Wall
        self.physics = [[0 for x in range(size)] for y in range(size)]
        self.fixedWalls = []
        self.generatedTiles = []

        self.tiles = []
        self.size = size

        self.size = size
        self.line = line
        self.column = column
        self.width = size * config.TILESIZE
        self.height = size * config.TILESIZE
        self.tilesToGenerate = []

        self.wallsToGenerate = []
        self.nbWallToGenerate = 0
        self.generatedWall = []

        self.enemiesToGenerate = {}
        self.itemsToGenerate = {}
        self.enemies = sprites.GameSpriteGroup()
        self.enemiesGenerated = []
        self.enemiesToDestroy = []

        self.items = sprites.GameSpriteGroup()
        self.itemsToGenerate = {}
        self.itemsGenerated = []
        self.itemsToDestroy = []

        self.adjacencies = [Adjacency.ALL]

        self.xStart = config.TILESIZE * size * column
        self.yStart = config.TILESIZE * size * line
        self.tilesGroup = None

    def generateLevel(self, spriteBank: dict, mark: mark.Mark):
        self.generateTiles(spriteBank, mark)
        self.generateMobs(spriteBank, mark)
        self.generateWalls(spriteBank, mark)
        if self.nbWallToGenerate > 0:
            self.generateWalls(spriteBank, mark)
        self.generateItems(spriteBank, mark)

    def render(self, window):
        if self.tilesGroup:
            self.tilesGroup.draw(window)
        if self.enemies:
            self.enemies.draw(window)
            # for enemy in self.enemiesGenerated:
            #     enemy.render(window)
        if self.itemsGenerated:
            # self.items.draw(window)
            for item in self.itemsGenerated:
                item.render(window)


    def update(self):
        if self.tilesGroup:
            self.tilesGroup.update()
        if self.enemies:
            self.enemies.update([self.xStart, self.xStart + self.width - config.TILESIZE,
                                 self.yStart, self.yStart + self.height - config.TILESIZE])
        if self.items:
            self.items.update()

    def getRandomX(self):
        return randint(self.xStart, self.xStart + self.width - config.TILESIZE)

    def getRandomY(self):
        return randint(self.yStart, self.yStart + self.height - config.TILESIZE)

    def buildMobs(self):
        pass

    def buildItems(self):
        pass


    def generateMobs(self, spriteBank: dict, mark: mark.Mark):
        for mobClass in self.enemiesToGenerate:
            for nb in range(self.enemiesToGenerate[mobClass]):
                x = self.getRandomX()
                y = self.getRandomY()
                m = mobClass(x, y, self.enemies, spriteBank, mark, self.textures)
                self.enemies.add(m)
                self.enemiesGenerated.append(m)

    def generateWalls(self, loadedRessource: dict, mark : mark.Mark):
        pass

    def generateItems(self, loadedRessource: dict, mark: mark.Mark):
        pass

    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)


class BasicRoom(GameRoom):
    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.buildMobs()
        self.buildItems()

    def buildMobs(self):
        self.enemiesToGenerate[mob.Gobelin] = {'nb': 1, "proba": 0.25}
        self.enemiesToGenerate[mob.Knight1] = {'nb': 1, "proba": 0.25}
        self.enemiesToGenerate[mob.Skeleton] = {'nb': 1, "proba": 0.25}

    def buildItems(self):
        self.itemsToGenerate[item.Scroll] = {"nb": 1, "proba": 1, "type": item.Scroll, "content":
            ["Hello Roger the TV lover !",
            "You have been teleported to the age",
            "of Le Roi Arthur because of a magic",
            "remote control. Yes, this is an",
            "astonishing news.",
            "You have to keep it alive and",
            "bring it to the castle."
            "You will find more scrolls like",
            "this one through your adventure.",
            "Be careful, Roger."],
        "delaySeconds": config.FPS * 10,
        "screenX": config.TILESIZE,
        "screenY": config.TILESIZE,
        "color": (255, 255, 255),
        "player": self.player}

    def generateTiles(self, loadedRessources: dict, mark : mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

    def generateMobs(self, spriteBank: dict, mark: mark.Mark):
        for mobClass in self.enemiesToGenerate:
            mobGenInfo = self.enemiesToGenerate[mobClass]
            nbToGen = mobGenInfo['nb']
            proba = 1 // mobGenInfo['proba']
            for nb in range(nbToGen):
                if random.randint(0, proba - 1) == 0:
                    x = self.getRandomX()
                    y = self.getRandomY()
                    m = mobClass(x, y, self.enemies, spriteBank, mark, self.textures)
                    self.enemies.add(m)
                    self.enemiesGenerated.append(m)

    def generateItems(self, spriteBank: dict, mark: mark.Mark):
        for itemClass in self.itemsToGenerate:
            itemGenInfo = self.itemsToGenerate[itemClass]
            nbToGen = itemGenInfo['nb']
            proba = 1 // itemGenInfo['proba']
            for nb in range(nbToGen):
                if random.randint(0, proba - 1) == 0:
                    # print("JYHTGFRDES")
                    x = self.getRandomX()
                    y = self.getRandomY()
                    if itemGenInfo['type'] == item.Scroll:
                        screenX = itemGenInfo['screenX']
                        screenY = itemGenInfo['screenY']
                        color = itemGenInfo['color']
                        scrollTexts = itemGenInfo['content']
                        delaySeconds = itemGenInfo['delaySeconds']
                        player = itemGenInfo['player']
                        m = itemClass(x, y, self.items, spriteBank, mark, self.textures, self.texts,
                                      scrollTexts, delaySeconds, screenX, screenY, color, player)
                    else:
                        m = itemClass(x, y, self.items, spriteBank, mark, self.textures, self.texts)
                    self.items.add(m)
                    self.itemsGenerated.append(m)


class TreeRoom(GameRoom):
    def __init__(self, textures: pygame.image,size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures,size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.wallsToGenerate.append((1, 2, tiles.TreeTiles))
        self.nbWallToGenerate = 8
        self.size = size

    def buildMobs(self):
        self.enemiesToGenerate[mob.Gobelin] = 1

    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

    def generateMobs(self, spriteBank: dict, mark: mark.Mark):
        for mobClass in self.enemiesToGenerate:
            for nb in range(self.enemiesToGenerate[mobClass]):
                x = self.getRandomX()
                y = self.getRandomY()
                m = mobClass(x, y, self.enemies, spriteBank, mark, self.textures)
                self.enemiesGenerated.append(m)
                self.enemies.add(m)


    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
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


class RuinedWildRoom(GameRoom):
    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.tilesToGenerate.append(tiles.FloorTiles)
        self.wallsToGenerate.append((1, 1, tiles.WallTiles))
        self.nbWallToGenerate = 10
        self.buildMobs()

    def buildMobs(self):
        self.enemiesToGenerate[mob.Gobelin] = 1


    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

    def generateMobs(self, spriteBank: dict, mark: mark.Mark):
        for mobClass in self.enemiesToGenerate:
            for nb in range(self.enemiesToGenerate[mobClass]):
                x = self.getRandomX()
                y = self.getRandomY()
                m = mobClass(x, y, self.enemies, spriteBank, mark, self.textures)
                self.enemiesGenerated.append(m)
                self.enemies.add(m)


    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
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


class CossWallRoom(GameRoom):

    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.wallsToGenerate.append((1, 1, tiles.WallTiles))
        self.nbWallToGenerate = 1
        self.adjacencies = [Adjacency.RIGHT, Adjacency.LEFT, Adjacency.BOTTOM, Adjacency.TOP]
        self.nbWallToGenerate = 1;
        self.buildMobs()

    def buildMobs(self):
        self.enemiesToGenerate[mob.Gobelin] = 1

    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

    def generateMobs(self, spriteBank: dict, mark: mark.Mark):
        for mobClass in self.enemiesToGenerate:
            for nb in range(self.enemiesToGenerate[mobClass]):
                x = self.getRandomX()
                y = self.getRandomY()
                m = mobClass(x, y, self.enemies, spriteBank, mark, self.textures)
                self.enemiesGenerated.append(m)
                self.enemies.add(m)


    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
        for x in range(int(self.size/2) - 1):
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + 0 * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + 0 * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + 0 * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1) * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1) * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1) * config.TILESIZE, mark))

        for x in range(int(self.size/2) + 1, self.size):
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + 0 * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + 0 * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + 0 * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1) * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1) * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1) * config.TILESIZE, mark))

        for y in range(int(self.size/2) + 1, self.size):
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))

        for y in range(int(self.size/2) - 1):
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))

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
        self.generatedWall.extend(self.fixedWalls)


class HCorridorWallRoom(GameRoom):
    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.FloorTiles)
        self.wallsToGenerate.append((1, 1, tiles.WallTiles))
        self.adjacencies = [Adjacency.RIGHT, Adjacency.LEFT]

        self.nbWallToGenerate = 1;
        self.buildMobs()

    def buildMobs(self):
        self.enemiesToGenerate[mob.Gobelin] = 1

    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)



    def generateMobs(self, spriteBank: dict, mark: mark.Mark):
        for mobClass in self.enemiesToGenerate:
            for nb in range(self.enemiesToGenerate[mobClass]):
                x = self.getRandomX()
                y = self.getRandomY()
                m = mobClass(x, y, self.enemies, spriteBank, mark, self.textures)
                self.enemies.add(m)
                self.enemiesGenerated.append(m)


    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):

        for x in range(self.size):
            for val in range(3):
                self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (0 + val) * config.TILESIZE, mark))
                self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (0 + val) * config.TILESIZE, mark))
                self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (0 + val) * config.TILESIZE, mark))
                self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1 - val) * config.TILESIZE, mark))
                self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1 - val) * config.TILESIZE, mark))
                self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1 - val) * config.TILESIZE, mark))

        # for x in range(int(self.size/2) + 1, self.size):
        #     for val in range(3):
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (0 + val) * config.TILESIZE, mark))
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (0 + val) * config.TILESIZE, mark))
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (0 + val) * config.TILESIZE, mark))
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1 - val) * config.TILESIZE, mark))
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1 - val) * config.TILESIZE, mark))
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1 - val) * config.TILESIZE, mark))

        for y in range(int(self.size/2) + 1, self.size):
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))

        for y in range(int(self.size/2) - 1):
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))

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
        self.generatedWall.extend(self.fixedWalls)


class VCorridorWallRoom(GameRoom):
    # Todo rename cette
    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.FloorTiles)
        self.wallsToGenerate.append((1, 1, tiles.WallTiles))
        self.adjacencies = [Adjacency.TOP, Adjacency.BOTTOM]

        self.nbWallToGenerate = 1;
        self.buildMobs()

    def buildMobs(self):
        self.enemiesToGenerate[mob.Gobelin] = 1

    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self. size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + y * config.TILESIZE, mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

    def generateMobs(self, spriteBank: dict, mark: mark.Mark):
        for mobClass in self.enemiesToGenerate:
            for nb in range(self.enemiesToGenerate[mobClass]):
                x = self.getRandomX()
                y = self.getRandomY()
                m = mobClass(x, y, self.enemies, spriteBank, mark, self.textures)
                self.enemies.add(m)
                self.enemiesGenerated.append(m)


    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):

        for y in range(self.size):
            for val in range(3):
                self.fixedWalls.append(
                    tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (0 + val) * config.TILESIZE,
                                    self.yStart + y * config.TILESIZE, mark))
                self.fixedWalls.append(
                    tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (0 + val) * config.TILESIZE,
                                    self.yStart + y * config.TILESIZE, mark))
                self.fixedWalls.append(
                    tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (0 + val) * config.TILESIZE,
                                    self.yStart + y * config.TILESIZE, mark))
                self.fixedWalls.append(
                    tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1 - val) * config.TILESIZE,
                                    self.yStart + y * config.TILESIZE, mark))
                self.fixedWalls.append(
                    tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1 - val) * config.TILESIZE,
                                    self.yStart + y * config.TILESIZE, mark))
                self.fixedWalls.append(
                    tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1 - val) * config.TILESIZE,
                                    self.yStart + y * config.TILESIZE, mark))

        # for x in range(int(self.size/2) + 1, self.size):
        #     for val in range(3):
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (0 + val) * config.TILESIZE, mark))
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (0 + val) * config.TILESIZE, mark))
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (0 + val) * config.TILESIZE, mark))
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1 - val) * config.TILESIZE, mark))
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1 - val) * config.TILESIZE, mark))
        #         self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1 - val) * config.TILESIZE, mark))

        for y in range(int(self.size/2) + 1, self.size):
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))

        for y in range(int(self.size/2) - 1):
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))
            self.fixedWalls.append(tiles.WallTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))

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
        self.generatedWall.extend(self.fixedWalls)


class LeftBorder(GameRoom):
    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.adjacencies = [Adjacency.TOP, Adjacency.RIGHT, Adjacency.BOTTOM]
        self.nbWallToGenerate = 0;
        self.buildMobs()

    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self.size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources,
                                                                                       self.tilesGroup,
                                                                                       self.xStart + x * config.TILESIZE,
                                                                                       self.yStart + y * config.TILESIZE,
                                                                                       mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
        for y in range(self.size):
            self.fixedWalls.append(tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))



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
        self.generatedWall.extend(self.fixedWalls)
        print(self.generatedWall[1].rect.y)
        print(self.generatedWall[2].rect.y)


class TopBorder(GameRoom):
    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.adjacencies = [ Adjacency.RIGHT, Adjacency.BOTTOM,Adjacency.LEFT]
        self.nbWallToGenerate = 0;
        self.buildMobs()

    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self.size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources,
                                                                                       self.tilesGroup,
                                                                                       self.xStart + x * config.TILESIZE,
                                                                                       self.yStart + y * config.TILESIZE,
                                                                                       mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
        for x in range(self.size):
            self.fixedWalls.append(tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart +  0 * config.TILESIZE, mark))



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
        self.generatedWall.extend(self.fixedWalls)
        print(self.generatedWall[1].rect.y)
        print(self.generatedWall[2].rect.y)


class BotBorder(GameRoom):
    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.adjacencies = [ Adjacency.RIGHT, Adjacency.TOP,Adjacency.LEFT]
        self.nbWallToGenerate = 0;
        self.buildMobs()

    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self.size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources,
                                                                                       self.tilesGroup,
                                                                                       self.xStart + x * config.TILESIZE,
                                                                                       self.yStart + y * config.TILESIZE,
                                                                                       mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
        for x in range(self.size):
            self.fixedWalls.append(tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE, self.yStart + (self.size - 1) * config.TILESIZE, mark))
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
        self.generatedWall.extend(self.fixedWalls)
        print(self.generatedWall[1].rect.y)
        print(self.generatedWall[2].rect.y)


class RightBorder(GameRoom):
    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.adjacencies = [ Adjacency.LEFT, Adjacency.TOP,Adjacency.LEFT]
        self.nbWallToGenerate = 0;
        self.buildMobs()


    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
        for y in range(self.size):
            self.fixedWalls.append(tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE, self.yStart + y * config.TILESIZE, mark))

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
        self.generatedWall.extend(self.fixedWalls)
        print(self.generatedWall[1].rect.y)
        print(self.generatedWall[2].rect.y)


class TopLeftBorder(GameRoom):

    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.adjacencies = [Adjacency.RIGHT, Adjacency.BOTTOM]
        self.nbWallToGenerate = 0;
        self.buildMobs()

    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
        for y in range(self.size):
            self.fixedWalls.append(
                tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE,
                                  self.yStart + y * config.TILESIZE, mark))
        for x in range(1, self.size):
            self.fixedWalls.append(
                tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE,
                                  self.yStart + 0 * config.TILESIZE, mark))

        for x in range(self.nbWallToGenerate):
            generated = False
            tryb = 0
            brutcap = 100
            while not generated and tryb < brutcap:
                tryb += 1
                wallToGenerate = self.wallsToGenerate[randint(0, len(self.wallsToGenerate) - 1)]
                generateCoordX = randint(2, len(self.physics) - 4)
                generateCoordY = randint(2, len(self.physics) - 4)

                # Check generation validity
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
                        tile = wallToGenerate[2](loadedRessources, self.tilesGroup,
                                                 self.xStart + generateCoordX * config.TILESIZE,
                                                 self.yStart + generateCoordY * config.TILESIZE, mark)
                        self.generatedWall.append(tile)
                        self.tiles.append(tile)
        self.generatedWall.extend(self.fixedWalls)
        print(self.generatedWall[1].rect.y)
        print(self.generatedWall[2].rect.y)


class TopRightBorder(GameRoom):

    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.adjacencies = [Adjacency.LEFT, Adjacency.BOTTOM]
        self.nbWallToGenerate = 0;
        self.buildMobs()

    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        self.tilesGroup = sprites.GameSpriteGroup()
        for x in range(self.size):
            for y in range(self.size):
                tile = self.tilesToGenerate[randint(0, len(self.tilesToGenerate) - 1)](loadedRessources,
                                                                                       self.tilesGroup,
                                                                                       self.xStart + x * config.TILESIZE,
                                                                                       self.yStart + y * config.TILESIZE,
                                                                                       mark)
                self.generatedTiles.append(tile)
                self.tiles.append(tile)

    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
        for y in range(self.size):
            self.fixedWalls.append(
                tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1 ) * config.TILESIZE,
                                  self.yStart + y * config.TILESIZE, mark))
        for x in range(1, self.size):
            self.fixedWalls.append(
                tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE,
                                  self.yStart + 0 * config.TILESIZE, mark))

        for x in range(self.nbWallToGenerate):
            generated = False
            tryb = 0
            brutcap = 100
            while not generated and tryb < brutcap:
                tryb += 1
                wallToGenerate = self.wallsToGenerate[randint(0, len(self.wallsToGenerate) - 1)]
                generateCoordX = randint(2, len(self.physics) - 4)
                generateCoordY = randint(2, len(self.physics) - 4)

                # Check generation validity
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
                        tile = wallToGenerate[2](loadedRessources, self.tilesGroup,
                                                 self.xStart + generateCoordX * config.TILESIZE,
                                                 self.yStart + generateCoordY * config.TILESIZE, mark)
                        self.generatedWall.append(tile)
                        self.tiles.append(tile)
        self.generatedWall.extend(self.fixedWalls)


class TopRightBorder(GameRoom):

    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.adjacencies = [Adjacency.LEFT, Adjacency.BOTTOM]
        self.nbWallToGenerate = 0;
        self.buildMobs()

    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):

        for y in range(self.size):
            self.fixedWalls.append(
                tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1 ) * config.TILESIZE,
                                  self.yStart + y * config.TILESIZE, mark))
        for x in range(self.size - 1):
            self.fixedWalls.append(
                tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE,
                                  self.yStart + 0 * config.TILESIZE, mark))

        for x in range(self.nbWallToGenerate):
            generated = False
            tryb = 0
            brutcap = 100
            while not generated and tryb < brutcap:
                tryb += 1
                wallToGenerate = self.wallsToGenerate[randint(0, len(self.wallsToGenerate) - 1)]
                generateCoordX = randint(2, len(self.physics) - 4)
                generateCoordY = randint(2, len(self.physics) - 4)

                # Check generation validity
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
                        tile = wallToGenerate[2](loadedRessources, self.tilesGroup,
                                                 self.xStart + generateCoordX * config.TILESIZE,
                                                 self.yStart + generateCoordY * config.TILESIZE, mark)
                        self.generatedWall.append(tile)
                        self.tiles.append(tile)
        self.generatedWall.extend(self.fixedWalls)
        print(self.generatedWall[1].rect.y)
        print(self.generatedWall[2].rect.y)


class BottomRightBorder(GameRoom):

    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.adjacencies = [Adjacency.LEFT, Adjacency.TOP]
        self.nbWallToGenerate = 0;
        self.buildMobs()

    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
        for y in range(self.size):
            self.fixedWalls.append(
                tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + (self.size - 1) * config.TILESIZE,
                                  self.yStart + y * config.TILESIZE, mark))
        for x in range(self.size - 1):
            self.fixedWalls.append(
                tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE,
                                  self.yStart + (self.size - 1) * config.TILESIZE, mark))

        for x in range(self.nbWallToGenerate):
            generated = False
            tryb = 0
            brutcap = 100
            while not generated and tryb < brutcap:
                tryb += 1
                wallToGenerate = self.wallsToGenerate[randint(0, len(self.wallsToGenerate) - 1)]
                generateCoordX = randint(2, len(self.physics) - 4)
                generateCoordY = randint(2, len(self.physics) - 4)

                # Check generation validity
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
                        tile = wallToGenerate[2](loadedRessources, self.tilesGroup,
                                                 self.xStart + generateCoordX * config.TILESIZE,
                                                 self.yStart + generateCoordY * config.TILESIZE, mark)
                        self.generatedWall.append(tile)
                        self.tiles.append(tile)
        self.generatedWall.extend(self.fixedWalls)
        print(self.generatedWall[1].rect.y)
        print(self.generatedWall[2].rect.y)


class BottomLeftBorder(GameRoom):

    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.adjacencies = [Adjacency.RIGHT, Adjacency.TOP]
        self.nbWallToGenerate = 0;
        self.buildMobs()

    def generateWalls(self, loadedRessources: dict, mark: mark.Mark):
        for y in range(self.size):
            self.fixedWalls.append(
                tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + 0 * config.TILESIZE,
                                  self.yStart + y * config.TILESIZE, mark))
        for x in range(1, self.size):
            self.fixedWalls.append(
                tiles.BorderTiles(loadedRessources, self.tilesGroup, self.xStart + x * config.TILESIZE,
                                  self.yStart + (self.size - 1) * config.TILESIZE, mark))

        for x in range(self.nbWallToGenerate):
            generated = False
            tryb = 0
            brutcap = 100
            while not generated and tryb < brutcap:
                tryb += 1
                wallToGenerate = self.wallsToGenerate[randint(0, len(self.wallsToGenerate) - 1)]
                generateCoordX = randint(2, len(self.physics) - 4)
                generateCoordY = randint(2, len(self.physics) - 4)

                # Check generation validity
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
                        tile = wallToGenerate[2](loadedRessources, self.tilesGroup,
                                                 self.xStart + generateCoordX * config.TILESIZE,
                                                 self.yStart + generateCoordY * config.TILESIZE, mark)
                        self.generatedWall.append(tile)
                        self.tiles.append(tile)
        self.generatedWall.extend(self.fixedWalls)
        print(self.generatedWall[1].rect.y)
        print(self.generatedWall[2].rect.y)


class SpawnTopLeftBorder(TopLeftBorder):

    def __init__(self, textures: pygame.image, size, line, column, texts: text.Texts, player):
        GameRoom.__init__(self, textures, size, line, column, texts, player)
        self.tilesToGenerate.append(tiles.GrassTile)
        self.tilesToGenerate.append(tiles.FlowerGrassTile)
        self.adjacencies = [Adjacency.LEFT, Adjacency.BOTTOM]
        self.nbWallToGenerate = 0
        self.buildMobs()

    def generateTiles(self, loadedRessources: dict, mark: mark.Mark):
        GameRoom.generateTiles(self, loadedRessources,mark)
        self.fixedTiles.append(tiles.FloorTiles(loadedRessources, self.tilesGroup, self.xStart + 5 * config.TILESIZE, self.yStart + 5 * config.TILESIZE,
                                                                   mark))


