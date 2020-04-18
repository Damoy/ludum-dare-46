import pygame
from pygame.sprite import Sprite, Group
from pygame.rect import Rect
from movement import Direction
from gameTime import TickCounter


def load(path):
    return pygame.image.load(path).convert()


class GameSpriteGroup(Group):
    def __init__(self):
        Group.__init__(self)


class GameSprite(Sprite):
    def __init__(self, image: pygame.image, group: GameSpriteGroup, x=-1, y=-1):
        Sprite.__init__(self, group)
        self.image = image
        self.rect = self.image.get_rect()
        if x != -1:
            self.rect.x = x
        if y != -1:
            self.rect.y = y


class DirectedAnimation:
    def __init__(self, tickCap, loop):
        self.spritesheet = {}
        self.framePtrs = {}
        self.tickCap = tickCap
        self.loop = loop
        self.currentDirection = None
        self.currentFrame = None

    def setDirection(self, direction: Direction):
        self.framePtrs[self.currentDirection] = 0
        self.currentDirection = direction
        self.currentFrame = self.spritesheet[self.currentDirection][self.framePtrs[self.currentDirection]]

    def update(self):
        framePtr = self.framePtrs[self.currentDirection]
        framePtr += 1
        if framePtr >= len(self.spritesheet[self.currentDirection]):
            framePtr = 0
        self.framePtrs[self.currentDirection] = framePtr
        self.currentFrame = self.spritesheet[self.currentDirection][framePtr]

    def getCurrentFrame(self):
        return self.currentFrame

    def addFrame(self, direction: Direction, image: pygame.image):
        if direction in self.spritesheet:
            self.spritesheet[direction].append(image)
        else:
            self.spritesheet[direction] = [image]
            self.framePtrs[direction] = 0
        return self


def subImage(image: pygame.image, x, y, w, h):
    return image.subsurface(Rect(x, y, w, h)).convert()


def loadSpriteBank(textures: pygame.image):
    spriteBank = {}
    tilesBank = {}
    tilesBank['grass'] = subImage(textures, 177, 1, 16, 16)
    tilesBank['fullTree'] = subImage(textures, 177, 33, 16, 32)
    tilesBank['overlapTree'] = subImage(textures, 193, 1, 16, 32)

    grassPlantTiles = []
    grassPlantTiles.append(subImage(textures, 210, 18, 14, 13))
    grassPlantTiles.append(subImage(textures, 226, 17, 14, 14))
    tilesBank['grassPlant'] = grassPlantTiles

    rockTiles = []
    rockTiles.append(subImage(textures, 209, 50, 16, 14))
    rockTiles.append(subImage(textures, 225, 50, 16, 13))
    rockTiles.append(subImage(textures, 241, 49, 16, 15))
    tilesBank['rock'] = rockTiles

    grassFlowerTiles = []
    grassFlower1 = []
    grassFlower1.append(subImage(textures, 257, 33, 16, 16))
    grassFlower1.append(subImage(textures, 273, 33, 16, 16))
    grassFlower1.append(subImage(textures, 289, 33, 16, 16))
    grassFlower2 = []
    grassFlower2.append(subImage(textures, 258, 50, 16, 16))
    grassFlower2.append(subImage(textures, 274, 50, 16, 16))
    grassFlower2.append(subImage(textures, 290, 50, 16, 16))
    # grassFlower3 = []
    # grassFlower3.append(subImage(textures, 0, 21, 7, 4))
    # grassFlower3.append(subImage(textures, 8, 21, 7, 6))
    # grassFlower3.append(subImage(textures, 16, 21, 9, 8))
    # grassFlower4 = []
    # grassFlower4.append(subImage(textures, 258, 83, 12, 12))
    # grassFlower4.append(subImage(textures, 274, 82, 14, 13))
    # grassFlower4.append(subImage(textures, 289, 82, 15, 13))
    grassFlowerTiles.append(grassFlower1)
    grassFlowerTiles.append(grassFlower2)
    # grassFlowerTiles.append(grassFlower3)
    # grassFlowerTiles.append(grassFlower4)
    tilesBank['grassFlower'] = grassFlowerTiles

    grassBlocks = []
    grassBlocks.append(subImage(textures, 312, 57, 34, 37))
    grassBlocks.append(subImage(textures, 257, 55, 24, 21))
    tilesBank['grassBlock'] = grassBlocks

    entitiesBank = {}
    entitiesBank['potion'] = subImage(textures, 0, 51, 9, 13)
    entitiesBank['seed'] = subImage(textures, 10, 13, 7, 11)
    entitiesBank['apple'] = subImage(textures, 18, 53, 10, 11)
    entitiesBank['scroll'] = subImage(textures, 29, 51, 12, 13)
    entitiesBank['heart'] = subImage(textures, 42, 51, 15, 13)

    characters = {}
    playerBank = {}
    playerDownFrames = []
    playerDownFrames.append(subImage(textures, 0, 1, 14, 15))
    playerDownFrames.append(subImage(textures, 18, 1, 14, 15))
    playerUpFrames = []
    playerUpFrames.append(subImage(textures, 34, 1, 14, 15))
    playerUpFrames.append(subImage(textures, 48, 1, 14, 15))
    playerRightFrames = []
    playerRightFrames.append(subImage(textures, 65, 1, 14, 15))
    playerRightFrames.append(subImage(textures, 82, 1, 14, 15))
    playerLeftFrames = []
    playerLeftFrames.append(pygame.transform.flip(playerRightFrames[0], True, False).convert())
    playerLeftFrames.append(pygame.transform.flip(playerRightFrames[1], True, False).convert())

    playerDash = {}
    playerDash['down'] = []
    playerDash['down'].append(subImage(textures, 0, 34, 14, 14))
    playerDash['down'].append(subImage(textures, 16, 33, 16, 15))
    playerDash['up'] = []
    playerDash['up'].append(subImage(textures, 34, 34, 14, 14))
    playerDash['up'].append(subImage(textures, 49, 34, 14, 15))
    playerDash['right'] = []
    playerDash['right'].append(subImage(textures, 65, 34, 14, 14))
    playerDash['right'].append(subImage(textures, 81, 34, 15, 14))
    playerDash['left'] = []
    playerDash['left'].append(pygame.transform.flip(playerDash['right'][0], True, False).convert())
    playerDash['left'].append(pygame.transform.flip(playerDash['right'][1], True, False).convert())

    playerWalk = {}
    playerWalk['down'] = playerDownFrames
    playerWalk['up'] = playerUpFrames
    playerWalk['left'] = playerLeftFrames
    playerWalk['right'] = playerRightFrames

    playerBank['walk'] = playerWalk
    playerBank['dash'] = playerDash

    enemiesBank = {}
    gobelin = {}
    gobelin['down'] = subImage(textures, 112, 33, 16, 15)
    gobelin['left'] = subImage(textures, 129, 33, 16, 15)
    gobelin['right'] = pygame.transform.flip(gobelin['left'], True, False).convert()
    enemiesBank['gobelin'] = gobelin

    knight1 = {}
    knight1['right'] = []
    knight1['right'].append(subImage(textures, 4, 163, 20, 17))
    knight1['right'].append(subImage(textures, 27, 163, 20, 17))
    knight1['right'].append(subImage(textures, 50, 163, 20, 17))
    knight1['right'].append(subImage(textures, 73, 163, 20, 17))
    knight1['left'] = []
    for frame in knight1['right']:
        knight1['left'].append(pygame.transform.flip(frame, True, False).convert())
    enemiesBank['knight1'] = knight1

    characters['player'] = playerBank
    characters['enemies'] = enemiesBank
    entitiesBank['characters'] = characters

    spriteBank['tiles'] = tilesBank
    spriteBank['entities'] = entitiesBank
    return spriteBank

