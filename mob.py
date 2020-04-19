import pygame
import sprites
from mark import Mark
from movement import Direction
from gameTime import TickCounter
import config
import random

class Mob(sprites.GameSprite):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image, startImage: pygame.image,
                 life, damage):
        sprites.GameSprite.__init__(self, startImage, group)
        self.mark = mark
        self.dx = 0
        self.dy = 0
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.dv = 1
        self.damage = damage
        self.life = life
        self.spriteBank = spriteBank
        self.directions = {"x": Direction.NONE, "y": Direction.NONE}
        self.animation = self.loadAnimation()
        self.updateDirectionTickCounter = TickCounter(config.FPS >> 2, False)
        self.updateDirectionTickCounter.start()
        self.pxMoveCount = 0
        self.alive = True

    def collideWall(self):
        self.x += -self.dx
        self.y += -self.dy
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

    def getBox(self):
        return pygame.rect.Rect(self.x, self.y, config.TILESIZE, config.TILESIZE)

    def render(self, screen):
        # b = self.getBox()
        # box = pygame.rect.Rect(b.x - self.mark.x, b.y - self.mark.y, 16, 16)
        # pygame.draw.rect(screen, (0, 255, 0), box)
        pass

    def loadAnimation(self):
        return None

    def update(self, roomBounds):
        oldDirs = {"x": self.directions["x"], "y": self.directions["y"]}
        self.updateDirection()
        self.move(oldDirs)
        self.fixBounds(roomBounds)
        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()


    def updateDirection(self):
        self.updateDirectionTickCounter.update()
        started = self.updateDirectionTickCounter.hasStarted()
        ended = self.updateDirectionTickCounter.hasReachedEnd()

        if started and ended:
            if random.randint(0, 4) == 0:
                # update direction on X
                randX = random.randint(0, 1)
                self.directions["x"] = Direction.LEFT if randX == 0 else Direction.RIGHT
                self.pxMoveCount = 0
            else:
                self.directions["x"] = Direction.NONE
                self.pxMoveCount = 0
            if random.randint(0, 4) == 0:
                # update direction on Y
                randY = random.randint(0, 1)
                self.directions["y"] = Direction.UP if randY == 0 else Direction.DOWN
                self.pxMoveCount = 0
            else:
                self.directions["y"] = Direction.NONE
                self.pxMoveCount = 0
            self.updateDirectionTickCounter.restart()

    def move(self, oldDirs):
        oldxdir = oldDirs["x"]
        # oldydir = oldDirs["y"]
        xdir = self.directions["x"]
        ydir = self.directions["y"]
        self.dx = 0
        self.dy = 0
        if xdir is not Direction.NONE:
            if xdir == Direction.LEFT:
                self.dx = -self.dv
            if xdir == Direction.RIGHT:
                self.dx = self.dv
        if ydir is not Direction.NONE:
            if ydir == Direction.UP:
                self.dy = -self.dv
            if ydir == Direction.DOWN:
                self.dy = self.dv

        if xdir != oldxdir:
            if self.dx > 0:
                self.animation.setDirection(Direction.RIGHT)
            elif self.dx < 0:
                self.animation.setDirection(Direction.LEFT)
            self.image = self.animation.getCurrentFrame()

        self.pxMoveCount += max(abs(self.dx), abs(self.dy))
        if self.pxMoveCount > config.TILESIZE:
            self.pxMoveCount = 0
            self.animation.update()
            self.image = self.animation.getCurrentFrame()

        self.x += self.dx
        self.y += self.dy

    def fixBounds(self, roomBounds):
        xstart = roomBounds[0]
        xend = roomBounds[1]
        ystart = roomBounds[2]
        yend = roomBounds[3]

        if self.x < xstart:
            self.x = xstart
            self.updateDirection()
        if self.x > xend:
            self.x = xend
            self.updateDirection()
        if self.y < ystart:
            self.y = ystart
            self.updateDirection()
        if self.y > yend:
            self.y = yend
            self.updateDirection()


class Gobelin(Mob):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image):
        Mob.__init__(self, x, y, group, spriteBank, mark, textures,
                     spriteBank['entities']['characters']['enemies']['gobelin']['down'],
                     1, 1)

    def loadAnimation(self):
        gobBank = self.spriteBank['entities']['characters']['enemies']['gobelin']
        anim = sprites.DirectedAnimation(120, True)
        anim.addFrame(sprites.Direction.LEFT, gobBank['left'])
        anim.addFrame(sprites.Direction.RIGHT, gobBank['right'])
        anim.addFrame(sprites.Direction.UP, gobBank['down'])
        anim.addFrame(sprites.Direction.DOWN, gobBank['down'])
        anim.setDirection(random.choice([Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]))
        return anim

class Knight1(Mob):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image):
        Mob.__init__(self, x, y, group, spriteBank, mark, textures,
                     spriteBank['entities']['characters']['enemies']['knight1']['right'][0],
                     2, 1)

    def loadAnimation(self):
        knightBank = self.spriteBank['entities']['characters']['enemies']['knight1']
        anim = sprites.DirectedAnimation(120, True)
        for leftFrame in knightBank['left']:
            anim.addFrame(Direction.LEFT, leftFrame)
        for rightFrame in knightBank['right']:
            anim.addFrame(Direction.RIGHT, rightFrame)
        anim.setDirection(random.choice([Direction.LEFT, Direction.RIGHT]))
        return anim

class Skeleton(Mob):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: Mark, textures: pygame.image):
        Mob.__init__(self, x, y, group, spriteBank, mark, textures,
                     spriteBank['dungeon']['mobs']['skeleton']['right'][0],
                     2, 1)

    def loadAnimation(self):
        skeletonBank = self.spriteBank['dungeon']['mobs']['skeleton']
        anim = sprites.DirectedAnimation(120, True)
        for leftFrame in skeletonBank['left']:
            anim.addFrame(Direction.LEFT, leftFrame)
        for rightFrame in skeletonBank['right']:
            anim.addFrame(Direction.RIGHT, rightFrame)
        anim.setDirection(random.choice([Direction.LEFT, Direction.RIGHT]))
        return anim