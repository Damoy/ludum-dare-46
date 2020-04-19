import pygame
import sprites

from board import TILE_SIZE
from movement import Direction
import config
import gameTime
import mark
import math

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
        self.dx = 0;
        self.dy = 0;
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
        self.life = 10
        self.isAttacking = False
        self.canAttack = True
        self.cdAttackTickCounter = gameTime.TickCounter(config.FPS >> 2, False)
        self.oldPos = (0, 0)

    def render(self):
        w = self.life * config.TILESIZE >> 1
        h = config.TILESIZE >> 1
        pygame.draw.rect(self.screen, (30, 230, 30), pygame.Rect(10, 10, w, h))
        # attack arc circle
        if self.isAttacking:
            start = 0
            stop = 0
            xdir = self.directions["x"]
            ydir = self.directions["y"]
            x = 0
            y = 0
            if xdir is not Direction.NONE and ydir is not Direction.NONE:
                if xdir == Direction.LEFT and ydir == Direction.UP:
                    start = math.pi / 2
                    stop = math.pi
                elif xdir == Direction.LEFT and ydir == Direction.DOWN:
                    start = math.pi
                    stop = 3 * (math.pi / 2)
                elif xdir == Direction.RIGHT and ydir == Direction.UP:
                    start = 0
                    stop = math.pi / 2
                elif xdir == Direction.RIGHT and ydir == Direction.DOWN:
                    start = 3 * (math.pi / 2)
                    stop = 2 * math.pi
                x = self.rect.x - 5 if xdir == Direction.LEFT else self.rect.x + 3
                y = self.rect.y - 5 if ydir == Direction.UP else self.rect.y + 3
            elif xdir is not Direction.NONE and ydir is Direction.NONE:
                start = 3 * math.pi / 4 if xdir == Direction.LEFT else -math.pi / 4
                stop = -3 * math.pi / 4 if xdir == Direction.LEFT else math.pi / 4
                x = self.rect.x - 5 if xdir == Direction.LEFT else self.rect.x + 3
                y = self.rect.y
            elif xdir is Direction.NONE and ydir is not Direction.NONE:
                start = math.pi / 4 if ydir == Direction.UP else 5 * math.pi / 4
                stop = 3 * math.pi / 4 if ydir == Direction.UP else 7 * math.pi / 4
                x = self.rect.x - 1
                y = self.rect.y - 5 if ydir == Direction.UP else self.rect.y + 3
            pygame.draw.arc(self.screen, (255, 255, 255),
                [x, y, config.TILESIZE, config.TILESIZE], start, stop)
            self.isAttacking = False

    def update(self):
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
        self.attack()

    def updateCdDashTickCounter(self):
        if self.cdDashTickCounter.hasStarted():
            self.cdDashTickCounter.update()
        if self.cdDashTickCounter.hasStarted() and self.cdDashTickCounter.hasReachedEnd():
            self.canDash = True
            self.cdDashTickCounter.reset()

    def updateCdAttackTickCounter(self):
        if self.cdAttackTickCounter.hasStarted():
            self.cdAttackTickCounter.update()
        if self.cdAttackTickCounter.hasStarted() and self.cdAttackTickCounter.hasReachedEnd():
            self.canAttack = True
            self.cdAttackTickCounter.reset()

    def attack(self):
        # self.updateCdAttackTickCounter()
        if not self.isDashing and not self.isAttacking: # and self.canAttack:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.isAttacking = True
                # self.canAttack = False
                # self.cdAttackTickCounter.restart()


    def move(self):
        self.oldPos = ( self.x, self.y)
        self.updateCdDashTickCounter()

        if self.isDashing:
            self.updateDash()
        else:
            self.dx = 0
            self.dy = 0
            dirX = Direction.NONE
            dirY = Direction.NONE

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.dx = -self.dv
                dirX = Direction.LEFT
            if keys[pygame.K_RIGHT]:
                self.dx = self.dv
                dirX = Direction.RIGHT
            if keys[pygame.K_DOWN]:
                self.dy = self.dv
                dirY = Direction.DOWN
            if keys[pygame.K_UP]:
                self.dy = -self.dv
                dirY = Direction.UP

            dirUpdated = self.directions["x"] is not dirX or self.directions["y"] is not dirY
            self.directions["x"] = dirX
            self.directions["y"] = dirY

            if keys[pygame.K_f] and (self.dx != 0 or self.dy != 0) and self.canDash:
                self.isDashing = True
                self.canDash = False

            if self.isDashing:
                self.animation = self.dashAnimation
                self.setAnimationDirection()
            else:
                self.animation = self.walkAnimation

            if not self.isDashing and self.dx != 0 or self.dy != 0:
                self.pxMoveCount += max(abs(self.dx), abs(self.dy))
                self.x += self.dx
                self.y += self.dy
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


