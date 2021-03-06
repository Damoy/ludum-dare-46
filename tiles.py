import sprites
import pygame
import mark
from random import randint


class Tile(sprites.GameSprite):
    def __init__(self, image: pygame.image, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        sprites.GameSprite.__init__(self, image, group, x, y)

        self.mark = mark
        self.x = x;
        self.y = y;

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.x - self.mark.getY()



class GrassTile(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, loadedRessources['tiles']['grass'], group, x, y,mark)


    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


class FlowerGrassTile(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        flowerSet = randint(0, len(loadedRessources['tiles']['grassFlower'])-1)
        Tile.__init__(self, loadedRessources['tiles']['grassFlower'][flowerSet][randint(0, len(loadedRessources['tiles']['grassFlower'][flowerSet]) - 1)], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


class TreeTiles(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y,mark:mark.Mark):
        Tile.__init__(self, loadedRessources['tiles']['fullTree'], group, x, y,mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


class BorderTiles(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, loadedRessources['tiles']['grassPlant'][0], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


class FloorTiles(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, loadedRessources['dungeon']['tiles']['floor'][randint(0, len(loadedRessources['dungeon']['tiles']['floor']) - 1)], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


class WallTiles(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, loadedRessources['dungeon']['walls']['up'][randint(0, len(loadedRessources['dungeon']['walls']['up']) - 1)], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


class WallTilesUp(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark, id):
        Tile.__init__(self, spriteBank['dungeon']['walls']['up'][id], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


class WallTilesdown(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark, id):
        Tile.__init__(self, spriteBank['dungeon']['walls']['down'][id], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

class WallTilesLeft(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark, id):
        Tile.__init__(self, spriteBank['dungeon']['walls']['left'][id], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

class WallTilesRight(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark, id):
        Tile.__init__(self, spriteBank['dungeon']['walls']['right'][id], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

class WallTilesRight(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark, id):

        Tile.__init__(self, spriteBank['dungeon']['walls']['right'][id], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

class WallTilesTopLeftCorner(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, spriteBank['dungeon']['walls']['upLeftCorner'], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

class WallTilesDownLeftCorner(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, spriteBank['dungeon']['walls']['downLeftCorner'], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


class WallTilesDownRightCorner(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, spriteBank['dungeon']['walls']['downRightCorner'], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


class WallTilesUpRightCorner(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, spriteBank['dungeon']['walls']['upRightCorner'], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

class CoinTiles(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, spriteBank['dungeon']['items']['gold'], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

class SqueletonTile(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, spriteBank['dungeon']['mobs']['skeleton']["right"][1], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

class WallTilesDown(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark, id):
        Tile.__init__(self, spriteBank['dungeon']['walls']['down'][id], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

class KnightTaupiqueurTile(Tile):
    def __init__(self, spriteBank: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark, id):
        Tile.__init__(self, spriteBank['entities']['characters']['enemies']['knight1']['right'][id], group, x, y, mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()