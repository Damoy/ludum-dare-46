import sprites
import pygame


class Tile(sprites.GameSprite):
    def __init__(self, image: pygame.image, group: sprites.GameSpriteGroup, x, y):
        sprites.GameSprite.__init__(self, image, group, x, y)
        # print("x:", x, ";y:", y)


class GrassTile(Tile):
    def __init__(self, loadedRessources: dict, group: sprites.GameSpriteGroup, x, y):
        #print(loadedRessources)
        Tile.__init__(self, loadedRessources['fullTree'], group, x, y)

        # print("x:", x, ";y:", y)

