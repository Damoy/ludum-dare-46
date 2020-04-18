import pygame
from sprites import GameSprite, GameSpriteGroup, subImage, loadPlayerAnimation

from map import TILE_SIZE
from movement import Direction


class Player(GameSprite):
    def __init__(self, screen: pygame.Surface, image: pygame.image, x, y, group: GameSpriteGroup,
                 spriteBank: dict):
        GameSprite.__init__(self, subImage(image, 0, 1, 14, 15), group)
        self.screen = screen
        self.rect.x = x
        self.rect.y = y
        self.dv = 1
        self.isMoving = False
        self.pxMoveCount = 0
        self.direction = Direction.NONE
        self.animation = loadPlayerAnimation(spriteBank)
        self.animation.setDirection(Direction.DOWN)
        self.userEnded = False

    def update(self):
        self.handleInput()

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.userEnded = True
                return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.userEnded = True
            return

        self.move()

    def move(self):
        if self.isMoving and self.direction is not Direction.NONE:
            self.updateMove()
        else:
            keys = pygame.key.get_pressed()
            oldDirection = self.direction
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.dv
                self.direction = Direction.LEFT
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.dv
                self.direction = Direction.RIGHT
            if keys[pygame.K_DOWN]:
                self.rect.y += self.dv
                self.direction = Direction.DOWN
            if keys[pygame.K_UP]:
                self.rect.y -= self.dv
                self.direction = Direction.UP
            if self.movingKeysActivated(keys):
                if self.direction is not oldDirection:
                    self.animation.setDirection(self.direction)
                    self.image = self.animation.getCurrentFrame()
                self.isMoving = True
                self.pxMoveCount += self.dv

    def updateAnimation(self):
        self.animation.update()
        self.image = self.animation.getCurrentFrame()

    def movingKeysActivated(self, keys):
        return keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] \
            or keys[pygame.K_DOWN] or keys[pygame.K_UP]

    def updateMove(self):
        if self.direction == Direction.DOWN:
            self.rect.y += self.dv
        elif self.direction == Direction.LEFT:
            self.rect.x -= self.dv
        elif self.direction == Direction.RIGHT:
            self.rect.x += self.dv
        elif self.direction == Direction.UP:
            self.rect.y -= self.dv

        self.pxMoveCount += self.dv

        if self.pxMoveCount >= TILE_SIZE:
            self.updateAnimation()
            self.endMove()

    def endMove(self):
        self.isMoving = False
        self.pxMoveCount = 0
