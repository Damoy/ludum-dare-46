import pygame
import sprites
import text
from mark import Mark
import config

class Item(sprites.GameSprite):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image,
                 startImage: pygame.image, texts: text.Texts):
        sprites.GameSprite.__init__(self, startImage, group)
        # self.rect.x = x
        # self.rect.y = y
        self.x = x
        self.y = y
        self.mark = mark
        self.texts = texts
        self.activated = False
        # print(startImage)
        # print(startImage.get_at((0, 0)))

    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

    def render(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def activate(self):
        self.activated = True

class Scroll(Item):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image,
                 texts: text.Texts, scrollText: str):
        Item.__init__(self, x, y, group, spriteBank, mark, textures,
                      spriteBank['entities']['scroll'], texts)
        self.scrollText = scrollText

    def render(self, window):
        super().render(window)
        if self.activated:
            x, y = self.texts.getMiddleCoords(self.scrollText)
            self.texts.render(self.scrollText, x, y, (255, 255, 255))
