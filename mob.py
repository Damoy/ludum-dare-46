import pygame
import sprites
import mark

class Mob(sprites.GameSprite):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: mark, textures: pygame.image, startImage: pygame.image):
        sprites.GameSprite.__init__(self, startImage, group)
        self.mark = mark
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.dv = 1
        self.spriteBank = spriteBank
        self.animation = self.loadAnimation()

    def loadAnimation(self):
        return None

    def update(self):
        pass

class Gobelin(Mob):
    def __init__(self, x, y, group: sprites.GameSpriteGroup,
                 spriteBank: dict, mark: mark, textures: pygame.image):
        Mob.__init__(self, x, y, group, spriteBank, mark, textures,
                     spriteBank['entities']['characters']['enemies']['gobelin']['down'])

    def loadAnimation(self):
        gobBank = self.spriteBank['entities']['characters']['enemies']['gobelin']
        print(gobBank)
        anim = sprites.DirectedAnimation(120, True)
        anim.addFrame(sprites.Direction.LEFT, gobBank['left'])
        anim.addFrame(sprites.Direction.RIGHT, gobBank['right'])
        anim.addFrame(sprites.Direction.UP, gobBank['down'])
        anim.addFrame(sprites.Direction.DOWN, gobBank['down'])
        return anim