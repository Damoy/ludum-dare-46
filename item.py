import pygame
import sprites
import text
from mark import Mark
import config
import gameTime

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
        self.listForDestruction = []


    def update(self):
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

    def render(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def activate(self):
        self.activated = True

    def getBox(self):
        return pygame.rect.Rect(self.x, self.y, config.TILESIZE, config.TILESIZE)

class Scroll(Item):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image,
                 texts: text.Texts, scrollTexts,
                 delaySeconds, screenX, screenY, color, player):
        Item.__init__(self, x, y, group, spriteBank, mark, textures,
                      spriteBank['entities']['scroll'], texts)
        self.scrollTexts = scrollTexts
        self.listForDestruction = None
        self.delaySeconds = delaySeconds
        self.destroyTimeTickCounter = gameTime.TickCounter(self.delaySeconds, False)
        self.screenX = screenX
        self.screenY = screenY
        self.color = color
        self.player = player

    def activate(self):
        super().activate()
        self.destroyTimeTickCounter.start()
        self.player.setRenderingTextMod(True)
        self.player.game.setRenderingText(True)


    def update(self):
        super().update()
        self.destroyTimeTickCounter.update()
        if self.destroyTimeTickCounter.hasStarted() and self.destroyTimeTickCounter.hasReachedEnd():
            self.activated = False
            self.listForDestruction.append(self)
            self.player.setRenderingTextMod(False)
            self.player.game.setRenderingText(False)

    def render(self, window):
        super().render(window)
        if self.activated:
            x = self.screenX
            y = self.screenY
            for scrollText in self.scrollTexts:
                self.texts.render(scrollText, x, y, self.color)
                y += 16

class Chest(Item):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image, texts: text.Texts = None):
        Item.__init__(self, x, y, group, spriteBank, mark, textures,
                      spriteBank['dungeon']['items']['chest'], texts)
        super().update()

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))