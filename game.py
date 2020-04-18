import os
import pygame

from player import Player
from window import Window
from board import Board
from mark import Mark
import sprites
import config


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1' # to center window
        pygame.init()
        self.window = Window("Game", config.HEIGHT, config.WIDTH, 3, flags=0) # [300, 226]
        self.screen = self.window.get()
        self.clock = pygame.time.Clock()
        self.isRunning = False
        self.textures = sprites.load(os.path.join('res', 'graphics', 'textures.png'))
        self.spriteBank = sprites.loadSpriteBank(self.textures)
        self.mark = Mark(0, 0)
        self.map = Board(self.window, self.textures, self.spriteBank, self.mark)
        self.map.initBoard(10, 10, 10);
        self.allSprites = sprites.GameSpriteGroup()
        self.player = Player(self.window.get(), self.textures, 150, 150, self.allSprites, self.spriteBank, self.mark)

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
        self.updateMark()
        if self.player.userEnded:
            self.isRunning = False

    def updateMark(self):
        if self.player.x - self.mark.getX() > self.player.screen.get_width() * 0.70:
            offset = self.player.x - self.mark.getX() - self.player.screen.get_width() * 0.70
            self.mark.x += offset

        elif self.player.x - self.mark.getX() < self.player.screen.get_width() * 0.2:
            offset = self.player.x - self.mark.getX() - self.player.screen.get_width() * 0.20
            self.mark.x += offset

        if self.player.y - self.mark.getY() < self.player.screen.get_height() * 0.1:
            offset = self.player.y - self.mark.getY() - self.player.screen.get_height() * 0.10
            self.player.mark.y += offset

        elif self.player.y - self.mark.getY() > self.player.screen.get_height() * 0.8:
            offset = self.player.y - self.mark.getY() - self.player.screen.get_height() * 0.80
            self.mark.y += offset

    def render(self):
        self.screen.fill((255, 255, 255))
        self.map.render()
        self.allSprites.draw(self.screen)
        self.window.render()


def main():
    game = Game()
    game.gameLoop()


main()
