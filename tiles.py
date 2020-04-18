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
        # print("x:", x, ";y:", y)


class GrassTile(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        Tile.__init__(self, loadedRessources['grass'], group, x, y,mark)
        # print("x:", x, ";y:", y)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


class FlowerGrassTile(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y, mark: mark.Mark):
        flowerSet = randint(0, len(loadedRessources['grassFlower'])-1)
        Tile.__init__(self, loadedRessources['grassFlower'][flowerSet][randint(0, len(loadedRessources['grassFlower'][flowerSet]) - 1)], group, x, y, mark)
        # print("x:", x, ";y:", y)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

class TreeTiles(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y,mark:mark.Mark):
        Tile.__init__(self, loadedRessources['fullTree'], group, x, y,mark)

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

