import os
import pygame

from player import Player
from window import Window
from board import Board
from mark import Mark
import sprites
import config
import sound

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
        self.board = Board(self.window, self.textures, self.spriteBank, self.mark)
        self.board.initBoard(10, 10, 10);
        self.allSprites = sprites.GameSpriteGroup()
        self.sounds = sound.Sounds()
        self.player = Player(self.window.get(), self.textures, 100, 90, self.allSprites, self.spriteBank, self.mark, self.sounds)

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
        self.board.update()
        if not self.checkCollide(self.player):
            self.player.handleInput()
        else:
            self.player.y += -self.player.dy
            self.player.x += -self.player.dx

        self.cleanMobs()

        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        mobsDico = self.getScreenMobs()
        # print("mobs: ", mobsDico)

        self.player.update(mobsDico)
        self.updateMark()

        keys = pygame.key.get_pressed()
        events = pygame.event.get()

        if self.player.userEnded:
            self.isRunning = False

    def getScreenMobs(self):
        mobs = {}
        for line in self.board.boardGrid:
            for col in line:
                if config.CANVASWIDTH + config.CANVASWIDTH / 1.5 > col.xStart - self.mark.x > - config.CANVASWIDTH / 1.5 and \
                        config.CANVASHEIGHT + config.CANVASHEIGHT / 1.5 > col.yStart - self.mark.y > - config.CANVASHEIGHT / 1.5:
                    mobs[col] = {"mobsGen": col.enemiesGenerated} # "mobsDestroy": col.enemiesToDestroy
        return mobs

    def cleanMobs(self):
        for line in self.board.boardGrid:
            for col in line:
                if config.CANVASWIDTH + config.CANVASWIDTH / 1.5 > col.xStart - self.mark.x > - config.CANVASWIDTH / 1.5 and \
                        config.CANVASHEIGHT + config.CANVASHEIGHT / 1.5 > col.yStart - self.mark.y > - config.CANVASHEIGHT / 1.5:

                    for mob in col.enemiesToDestroy:
                        if mob in col.enemiesGenerated:
                            self.sounds.playHitSound()
                            col.enemiesGenerated.remove(mob)
                            col.enemies.remove(mob) # should be in list
                    col.enemiesToDestroy.clear()

    def checkCollide(self, player):
        for line in self.board.boardGrid:
            for col in line:
                if config.CANVASWIDTH + config.CANVASWIDTH / 1.5 > col.xStart - self.mark.x > - config.CANVASWIDTH / 1.5 and \
                        config.CANVASHEIGHT + config.CANVASHEIGHT / 1.5 > col.yStart - self.mark.y > - config.CANVASHEIGHT / 1.5:

                    for mob in col.enemiesGenerated:
                        if pygame.sprite.collide_rect(mob, player):
                            player.collideMob(mob)

                    for wall in col.generatedWall:
                        for mob in col.enemiesGenerated:
                            if pygame.sprite.collide_rect(mob, wall):
                                mob.collideWall()

                        if pygame.sprite.collide_rect(player, wall):
                            return True

                    for wall in col.generatedWall:
                        if pygame.sprite.collide_rect(player, wall):
                            return True
        return False


    def updateMark(self):

        if self.player.x - self.mark.getX() > self.player.screen.get_width() * 0.70 and not self.player.x > len(self.board.boardGrid[0]) * len(self.board.boardGrid) * config.TILESIZE - config.CANVASWIDTH :
            offset = self.player.x - self.mark.getX() - self.player.screen.get_width() * 0.70
            self.mark.x += offset

        elif self.player.x - self.mark.getX() < self.player.screen.get_width() * 0.30 and not self.player.x < config.CANVASWIDTH :
            offset = self.player.x - self.mark.getX() - self.player.screen.get_width() * 0.30
            self.mark.x += offset

        if self.player.y - self.mark.getY() < self.player.screen.get_height() * 0.30 and not self.player.y < config.CANVASHEIGHT:
            offset = self.player.y - self.mark.getY() - self.player.screen.get_height() * 0.30
            self.player.mark.y += offset

        elif self.player.y - self.mark.getY() > self.player.screen.get_height() * 0.7 and not self.player.y > len(self.board.boardGrid[0]) * len(self.board.boardGrid) * config.TILESIZE - config.CANVASHEIGHT:
            offset = self.player.y - self.mark.getY() - self.player.screen.get_height() * 0.70
            self.mark.y += offset

    def render(self):
        self.screen.fill((255, 255, 255))
        self.board.render()
        self.player.render()
        # self.allSprites.draw(self.screen)
        self.window.render()

    def compute_penetration(self, block, old_rect, new_rect):
        """Calcul la distance de pénétration du `new_rect` dans le `block` donné.

        `block`, `old_rect` et `new_rect` sont des pygame.Rect.
        Retourne les distances `dx_correction` et `dy_correction`.
        """
        dx_correction = dy_correction = 0.0
        if old_rect.bottom <= block.top < new_rect.bottom:
            dy_correction = block.top - new_rect.bottom
        elif old_rect.top >= block.bottom > new_rect.top:
            dy_correction = block.bottom - new_rect.top
        if old_rect.right <= block.left < new_rect.right:
            dx_correction = block.left - new_rect.right
        elif old_rect.left >= block.right > new_rect.left:
            dx_correction = block.right - new_rect.left
        return dx_correction, dy_correction

def main():
    game = Game()
    game.gameLoop()


main()
