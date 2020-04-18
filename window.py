import pygame

class Window:
    def __init__(self, title, width, height, scale=1, flags=0):
        self.title = title
        self.width = width
        self.height = height
        self.scale = scale
        self.widthScaled = self.width // self.scale
        self.heigthScaled = self.height // self.scale
        self.flags = flags
        self.content = None
        self.scaledContent = None
        self.frame = None
        self.create()

    def create(self):
        self.content = pygame.display.set_mode((self.width, self.height), flags=self.flags)
        self.scaledContent = pygame.Surface([self.widthScaled, self.heigthScaled])
        pygame.display.set_caption(self.title)
        return self.scaledContent

    def get(self):
        return self.scaledContent

    def render(self):
        frame = pygame.transform.scale(self.scaledContent, (self.width, self.height))
        self.content.blit(frame, frame.get_rect())
        pygame.display.update();