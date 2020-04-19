import pygame
import os
import config


class Texts:
    def __init__(self, screen):
        pygame.font.init()
        self.gameFont = None
        self.screen = screen
        self.fonts = self.loadFonts()

    def loadFonts(self):
        self.gameFont = pygame.font.Font(os.path.join('res', 'fonts', 'pixel_art', 'pixelart.ttf'), config.FONT_SIZE)
        return [self.gameFont]

    def render(self, text, x, y, color):
        # def render(self, text, antialias, color, background=None):
        textSurface = self.gameFont.render(text, True, color)
        self.screen.blit(textSurface, (x, y))

    def getTextSize(self, text):
        return self.gameFont.size(text)

    def getMiddleCoords(self, text):
        w, h = self.getTextSize(text)
        x = config.CANVAS_MIDDLE_X
        y = config.CANVAS_MIDDLE_Y
        return x, y