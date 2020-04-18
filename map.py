import pygame
from window import Window
import sprites
import random

TILE_SIZE = 16


class Map:
    def __init__(self, window: Window, textures: pygame.image, spriteBank: dict):
        self.window = window
        self.textures = textures
        self.rows = window.heigthScaled // TILE_SIZE
        self.cols = window.widthScaled // TILE_SIZE
        self.maxHeight = self.rows * TILE_SIZE
        self.maxWidth = self.cols * TILE_SIZE
        self.tilesBank = spriteBank['tiles']
        self.tilesGroup = sprites.GameSpriteGroup()
        self.tiles = self.initTiles()

    def initTiles(self):
        tiles = []
        grassFlowerTiles = self.tilesBank['grassFlower']
        for row in range(self.rows):
            y = max(TILE_SIZE // 2, min(self.maxHeight - TILE_SIZE, row * TILE_SIZE))
            tileRow = []
            for col in range(self.cols):
                x = max(TILE_SIZE // 2, min(self.maxWidth - TILE_SIZE, col * TILE_SIZE))
                texture = self.getRandomTile(grassFlowerTiles)
                tile = Tile(texture, self.tilesGroup, x, y)
                tileRow.append(tile)
            tiles.append(tileRow)
        return tiles

    def getRandomTile(self, arrs):
        n = len(arrs)
        row = random.randint(0, n - 1)
        m = random.randint(0, len(arrs[row]) - 1)
        return arrs[row][m]

    def update(self):
        pass

    def render(self):
        self.window.get().fill(self.tilesBank['grass'].get_at((0, 0)))
        self.tilesGroup.draw(self.window.get())

class Tile(sprites.GameSprite):
    def __init__(self, image: pygame.image, group: sprites.GameSpriteGroup, x, y):
        sprites.GameSprite.__init__(self, image, group, x, y)
        # print("x:", x, ";y:", y)