import pygame
import sprites

from board import TILE_SIZE
from movement import Direction
import config
import gameTime
import mark

class Player(sprites.GameSprite):
    def __init__(self, screen: pygame.Surface, image: pygame.image, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: mark):
        sprites.GameSprite.__init__(self, sprites.subImage(image, 0, 1, 14, 15), group)
        self.screen = screen
        self.mark = mark
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.dv = 1
        self.dvDash = self.dv * 3
        self.pxMoveCount = 0
        self.directions = {"x": Direction.LEFT, "y": Direction.DOWN}
        self.walkAnimation = None
        self.dashAnimation = None
        self.loadAnimations(spriteBank)
        self.animation = self.walkAnimation
        self.animation.setDirection(self.directions["y"])
        self.userEnded = False
        self.isDashing = False
        self.canDash = True
        self.cdDashTickCounter = gameTime.TickCounter(config.FPS >> 1, False)

    def update(self):

        self.handleInput()

        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

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

    def updateCdDashTickCounter(self):
        if self.cdDashTickCounter.hasStarted():
            self.cdDashTickCounter.update()
        if self.cdDashTickCounter.hasStarted() and self.cdDashTickCounter.hasReachedEnd():
            self.canDash = True
            self.cdDashTickCounter.reset()

    def move(self):
        self.updateCdDashTickCounter()

        if self.isDashing:
            self.updateDash()
        else:
            dx = 0
            dy = 0
            dirX = Direction.NONE
            dirY = Direction.NONE

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                dx = -self.dv
                dirX = Direction.LEFT
            if keys[pygame.K_RIGHT]:
                dx = self.dv
                dirX = Direction.RIGHT
            if keys[pygame.K_DOWN]:
                dy = self.dv
                dirY = Direction.DOWN
            if keys[pygame.K_UP]:
                dy = -self.dv
                dirY = Direction.UP

            dirUpdated = self.directions["x"] is not dirX or self.directions["y"] is not dirY
            self.directions["x"] = dirX
            self.directions["y"] = dirY

            if keys[pygame.K_f] and (dx != 0 or dy != 0) and self.canDash:
                self.isDashing = True
                self.canDash = False

            if self.isDashing:
                self.animation = self.dashAnimation
                self.setAnimationDirection()
            else:
                self.animation = self.walkAnimation

            if not self.isDashing and dx != 0 or dy != 0:
                self.pxMoveCount += max(abs(dx), abs(dy))
                self.x += dx
                self.y += dy
                if dirUpdated:
                    self.setAnimationDirection()
                elif self.pxMoveCount >= config.TILESIZE:
                    self.pxMoveCount = 0
                    self.updateAnimation()

    def setAnimationDirection(self):
        if self.directions["y"] is Direction.NONE:
            self.animation.setDirection(self.directions["x"])
        else:
            self.animation.setDirection(self.directions["y"])
        self.image = self.animation.getCurrentFrame()

    def updateAnimation(self):
        self.animation.update()
        self.image = self.animation.getCurrentFrame()

    def movingKeysActivated(self, keys):
        return keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] \
            or keys[pygame.K_DOWN] or keys[pygame.K_UP]

    def loadAnimations(self, spriteBank: dict):
        playerBank = spriteBank['entities']['characters']['player']
        playerWalk = playerBank['walk']

        self.walkAnimation = sprites.DirectedAnimation(60, True)
        for playerUpFrame in playerWalk['up']:
            self.walkAnimation.addFrame(Direction.UP, playerUpFrame)
        for playerDownFrame in playerWalk['down']:
            self.walkAnimation.addFrame(Direction.DOWN, playerDownFrame)
        for playerLeftFrame in playerWalk['left']:
            self.walkAnimation.addFrame(Direction.LEFT, playerLeftFrame)
        for playerRightFrame in playerWalk['right']:
            self.walkAnimation.addFrame(Direction.RIGHT, playerRightFrame)

        playerDash = playerBank['dash']
        self.dashAnimation = sprites.DirectedAnimation(90, True)
        for playerDownFrame in playerDash['down']:
            self.dashAnimation.addFrame(Direction.DOWN, playerDownFrame)
        for playerUpFrame in playerDash['up']:
            self.dashAnimation.addFrame(Direction.UP, playerUpFrame)
        for playerLeftFrame in playerDash['left']:
            self.dashAnimation.addFrame(Direction.LEFT, playerLeftFrame)
        for playerRightFrame in playerDash['right']:
            self.dashAnimation.addFrame(Direction.RIGHT, playerRightFrame)

    def updateDash(self):
        if self.directions["x"] is Direction.NONE and self.directions["y"] is Direction.NONE:
            return
        dx = 0
        dy = 0
        dirX = self.directions["x"]
        dirY = self.directions["y"]

        if dirX == Direction.LEFT:
            dx = -self.dvDash
        if dirX == Direction.RIGHT:
            dx = self.dvDash
        if dirY == Direction.UP:
            dy = -self.dvDash
        if dirY == Direction.DOWN:
            dy = self.dvDash

        self.x += dx
        self.y += dy
        self.pxMoveCount += max(abs(dx), abs(dy))

        # update dash animation
        if self.pxMoveCount >= 16:
            self.updateAnimation()

        # end of dash
        if self.pxMoveCount >= 48:
            self.isDashing = False
            self.cdDashTickCounter.start()
            self.animation = self.walkAnimation
            self.setAnimationDirection()
            self.pxMoveCount = 0


