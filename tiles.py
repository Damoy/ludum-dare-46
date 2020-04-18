import sprites
import pygame
import mark


class Tile(sprites.GameSprite):
    def __init__(self, image: pygame.image, group: sprites.GameSpriteGroup, x, y,mark:mark.Mark):
        sprites.GameSprite.__init__(self, image, group, x, y)
        self.mark = mark
        self.x = x;
        self.y = y;

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.x - self.mark.getY()
        # print("x:", x, ";y:", y)


class GrassTile(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y, mark:mark.Mark):
        Tile.__init__(self, loadedRessources['grass'], group, x, y,mark)
        # print("x:", x, ";y:", y)

class TreeTiles(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y,mark:mark.Mark):
        Tile.__init__(self, loadedRessources['fullTree'], group, x, y,mark)

