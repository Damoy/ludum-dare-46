import os
import pygame

class Sounds:
    def __init__(self):
        pygame.mixer.init()
        sounds = self.loadSounds()
        hitSound = None
        hitSound2 = None

    def loadSounds(self):
        self.hitSound = pygame.mixer.Sound(os.path.join('res', 'sounds', 'hit.wav'))
        self.hitSound2 = pygame.mixer.Sound(os.path.join('res', 'sounds', 'hit2.wav'))
        return [self.hitSound, self.hitSound2]

    def playHitSound(self):
        self.hitSound.play()

    def playHitSound2(self):
        self.hitSound2.play()
