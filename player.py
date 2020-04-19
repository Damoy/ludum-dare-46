import pygame
import sprites

from board import TILE_SIZE
from movement import Direction
import config
import gameTime
import mark
import math
from pygame.rect import Rect

class Attack:
    def __init__(self, x, y, w, h, color, screen, start, stop, mark: mark.Mark, dmg):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.screen = screen
        self.start = start
        self.stop = stop
        self.shouldRender = False
        self.box = None
        self.mark = mark
        self.dmg = dmg

    def collide(self, rect2: pygame.rect.Rect):
        if self.box is None or rect2 is None:
            return False
        return self.box.colliderect(rect2)

    # collision todo
    def update(self, mobsDico: dict):
        self.box = self.getBox()
        for room in mobsDico:
            mobsGenerated = mobsDico[room]['mobsGen']
            # mobsToDestroy = mobsDico[room]['mobsDestroy']
            for mob in mobsGenerated:
                if self.collide(mob.getBox()):
                    mob.life -= self.dmg
                    if mob.life <= 0:
                        mob.alive = False
                        room.enemiesToDestroy.append(mob)

    def render(self):
        if self.shouldRender:
            pygame.draw.arc(self.screen, self.color,
                [self.x - self.mark.x, self.y - self.mark.y, self.w, self.h], self.start, self.stop)
            # print("[", self.x, ",", self.y, ",", self.w, ",", self.h)
            # pygame.draw.rect(self.screen, (255, 0, 0), pygame.rect.Rect(self.x - self.mark.x, self.y - self.mark.y, self.w, self.h))
            self.shouldRender = False
            # print("treggfd:", "x:", self.x, ";y:", self.y, ";w:", self.w, ";h:", self.h, ";s:", self.start, ";stop:", self.stop)

    def getBox(self):
        box = pygame.rect.Rect(self.x, self.y, 16, 16)
        # print("attack box:", box)
        return box


class Player(sprites.GameSprite):
    def __init__(self, screen: pygame.Surface, image: pygame.image, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: mark, sounds):
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
        self.directions = {"x": Direction.NONE, "y": Direction.DOWN}
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
        self.cdAttackTickCounter = gameTime.TickCounter(5, False)
        self.damage = 1
        self.attackArcCircle = Attack(0, 0, config.TILESIZE, config.TILESIZE,
                                      (255, 255, 255), self.screen, 0, 0, self.mark, self.damage)
        self.attackDirections = {"x": self.directions["x"], "y": self.directions["y"]}
        self.updateHandleAttack()
        self.oldPos = (0, 0)
        self.sounds = sounds

    def getAttackBox(self):
        if not self.isAttacking:
            return None
        return self.attackArcCircle.getBox()

    def render(self):
        # image
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        # life
        w = self.life * config.TILESIZE >> 1
        h = config.TILESIZE >> 1
        pygame.draw.rect(self.screen, (30, 230, 30), pygame.Rect(10, 10, w, h))
        # attack
        if self.attackArcCircle.shouldRender:
            self.attackArcCircle.render()

    def update(self, mobsDico):
        # self.handleInput()
        self.handleAttack(mobsDico)

        self.rect.x = self.x - self.mark.getX()
        self.rect.y = self.y - self.mark.getY()

    def handleAttack(self, mobsDico):
        # attack arc circle
        self.updateCdAttackTickCounter()
        if self.isAttacking:
            # self.sounds.playHitSound2()
            self.updateHandleAttack()
            self.attackArcCircle.update(mobsDico)

    def updateHandleAttack(self):
        start = self.attackArcCircle.start
        stop = self.attackArcCircle.stop
        xdir = self.attackDirections["x"]
        ydir = self.attackDirections["y"]
        x = self.attackArcCircle.x
        y = self.attackArcCircle.y
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
            x = self.x - 16 if xdir == Direction.LEFT else self.x + 12
            y = self.y - 16 if ydir == Direction.UP else self.y + 12
        elif xdir is not Direction.NONE and ydir is Direction.NONE:
            start = 3 * math.pi / 4 if xdir == Direction.LEFT else -math.pi / 4
            stop = -3 * math.pi / 4 if xdir == Direction.LEFT else math.pi / 4
            x = self.x - 16 if xdir == Direction.LEFT else self.x + 12
            y = self.y
        elif xdir is Direction.NONE and ydir is not Direction.NONE:
            start = math.pi / 4 if ydir == Direction.UP else 5 * math.pi / 4
            stop = 3 * math.pi / 4 if ydir == Direction.UP else 7 * math.pi / 4
            x = self.x - 2
            y = self.y - 16 if ydir == Direction.UP else self.y + 12
        self.attackArcCircle.x = x
        self.attackArcCircle.y = y
        self.attackArcCircle.start = start
        self.attackArcCircle.stop = stop
        self.attackArcCircle.shouldRender = True
        self.isAttacking = False
        self.cdAttackTickCounter.restart()
        self.canAttack = False

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
        if not self.isDashing and not self.isAttacking and self.canAttack:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.isAttacking = True
                self.cdAttackTickCounter.stop()


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
                self.attackDirections["x"] = dirX
            if keys[pygame.K_RIGHT]:
                self.dx = self.dv
                dirX = Direction.RIGHT
                self.attackDirections["x"] = dirX
            if keys[pygame.K_DOWN]:
                self.dy = self.dv
                dirY = Direction.DOWN
                self.attackDirections["y"] = dirY
            if keys[pygame.K_UP]:
                self.dy = -self.dv
                dirY = Direction.UP
                self.attackDirections["y"] = dirY

            dirXUpdated = self.directions["x"] is not dirX
            dirYUpdated = self.directions["y"] is not dirY
            dirUpdated = dirXUpdated or dirYUpdated

            if dirXUpdated and not dirYUpdated:
                self.attackDirections["y"] = Direction.NONE
            if not dirXUpdated and dirYUpdated:
                self.attackDirections["x"] = Direction.NONE

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
        if self.pxMoveCount >= config.TILESIZE:
            self.updateAnimation()

        # end of dash
        if self.pxMoveCount >= config.TILESIZE * 3:
            self.isDashing = False
            self.cdDashTickCounter.start()
            self.animation = self.walkAnimation
            self.setAnimationDirection()
            self.pxMoveCount = 0

    def collideMob(self, mob):
        self.life -= mob.damage
        # print("colision")
        self.x -= self.dx
        self.y -= self.dy
