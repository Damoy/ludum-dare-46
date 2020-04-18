import os
import pygame

from player import Player
from window import Window
from map import Map

import config
import sprites

class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1' # to center window
        pygame.init()
        self.window = Window("Game", 912, 672, 3, flags=0) # [304, 224]
        self.screen = self.window.get()
        self.clock = pygame.time.Clock()
        self.isRunning = False
        self.textures = sprites.load(os.path.join('res', 'graphics', 'textures.png'))
        self.spriteBank = sprites.loadSpriteBank(self.textures)
        self.map = Map(self.window, self.textures, self.spriteBank)
        self.allSprites = sprites.GameSpriteGroup()
        self.player = Player(self.window.get(), self.textures, 100, 100, self.allSprites, self.spriteBank)

    def gameLoop(self):
        self.isRunning = True
        while self.isRunning:
            self.clock.tick(config.FPS)
            self.update()
            if not self.isRunning:
                break
            self.render()
        pygame.quit()

    def update(self):
        self.allSprites.update()
        if self.player.userEnded:
            self.isRunning = False

    def render(self):
        self.screen.fill((255, 255, 255))
        self.map.render()
        self.allSprites.draw(self.screen)
        self.window.render()

def main():
    game = Game()
    game.gameLoop()


main()
