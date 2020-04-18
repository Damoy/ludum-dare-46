class TickCounter:
    def __init__(self, maxTick, loop):
        self.tick = 0
        self.maxTick = maxTick
        self.started = False
        self.reachedEnd = False
        self.loop = loop

    def start(self):
        self.started = True
        self.reachedEnd = False

    def update(self):
        if not self.started or self.reachedEnd:
            return False
        self.tick += 1
        reachedEnd = self.reachedEnd
        if self.tick >= self.maxTick:
            self.reachedEnd = True
            reachedEnd = self.reachedEnd
            if self.loop:
                self.restart()
        return reachedEnd

    def stop(self):
        self.started = False

    def reset(self):
        self.tick = 0
        self.started = False
        self.reachedEnd = False

    def restart(self):
        self.reset()
        self.start()

    def hasStarted(self):
        return self.started

    def hasReachedEnd(self):
        return self.reachedEnd