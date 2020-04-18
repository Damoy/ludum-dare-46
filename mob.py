import pygame
import sprites
from mark import Mark
from movement import Direction
from gameTime import TickCounter
import config
import random

class Mob(sprites.GameSprite):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image, startImage: pygame.image):
        sprites.GameSprite.__init__(self, startImage, group)
        self.mark = mark
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.dv = 1
        self.spriteBank = spriteBank
        self.directions = {"x": Direction.NONE, "y": Direction.NONE}
        self.animation = self.loadAnimation()
        self.updateDirectionTickCounter = TickCounter(config.FPS >> 1, False)
        self.updateDirectionTickCounter.start()

    def loadAnimation(self):
        return None

    def update(self, roomBounds):
        self.updateDirection()
        self.move()
        self.fixBounds(roomBounds)
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

    def updateDirection(self):
        self.updateDirectionTickCounter.update()
        started = self.updateDirectionTickCounter.hasStarted()
        ended = self.updateDirectionTickCounter.hasReachedEnd()

        if started and ended:
            if random.randint(0, 3) == 0:
                # update direction on X
                randX = random.randint(0, 1)
                self.directions["x"] = Direction.LEFT if randX == 0 else Direction.RIGHT
            else:
                self.directions["x"] = Direction.NONE
            if random.randint(0, 3) == 0:
                # update direction on Y
                randY = random.randint(0, 1)
                self.directions["y"] = Direction.UP if randY == 0 else Direction.DOWN
            else:
                self.directions["y"] = Direction.NONE
            self.updateDirectionTickCounter.restart()

    def move(self):
        xdir = self.directions["x"]
        ydir = self.directions["y"]
        dx = 0
        dy = 0
        if xdir is not Direction.NONE:
            if xdir == Direction.LEFT:
                dx = -self.dv
            if xdir == Direction.RIGHT:
                dx = self.dv
        if ydir is not Direction.NONE:
            if ydir == Direction.UP:
                dy = -self.dv
            if ydir == Direction.DOWN:
                dy = self.dv
        self.x += dx
        self.y += dy

    def fixBounds(self, roomBounds):
        xstart = roomBounds[0]
        xend = roomBounds[1]
        ystart = roomBounds[2]
        yend = roomBounds[3]

        if self.x < xstart:
            self.x = xstart
        if self.x > xend:
            self.x = xend
        if self.y < ystart:
            self.y = ystart
        if self.y > yend:
            self.y = yend


class Gobelin(Mob):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image):
        Mob.__init__(self, x, y, group, spriteBank, mark, textures,
                     spriteBank['entities']['characters']['enemies']['gobelin']['down'])

    def loadAnimation(self):
        gobBank = self.spriteBank['entities']['characters']['enemies']['gobelin']
        anim = sprites.DirectedAnimation(120, True)
        anim.addFrame(sprites.Direction.LEFT, gobBank['left'])
        anim.addFrame(sprites.Direction.RIGHT, gobBank['right'])
        anim.addFrame(sprites.Direction.UP, gobBank['down'])
        anim.addFrame(sprites.Direction.DOWN, gobBank['down'])
        return anim

class Knight1(Mob):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image):
        Mob.__init__(self, x, y, group, spriteBank, mark, textures,
                     spriteBank['entities']['characters']['enemies']['knight1']['right'][0])

    def loadAnimation(self):
        knightBank = self.spriteBank['entities']['characters']['enemies']['knight1']
        anim = sprites.DirectedAnimation(120, True)
        for leftFrame in knightBank['left']:
            anim.addFrame(Direction.LEFT, leftFrame)
        for rightFrame in knightBank['right']:
            anim.addFrame(Direction.RIGHT, rightFrame)
        return anim