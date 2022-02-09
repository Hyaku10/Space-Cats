import pygame
print('Path to module:',pygame.__file__)

# ENEMY LEVEL 1 CLASS
class Enemy:
    def __init__(self, x, y, lvl):
        self.x = x
        self.y = y
        self.lvl = lvl

        if lvl==1:
        #    self.direction = direction
            self.health = 5
        #    self.img = enemylvl1img
        #    self.mask = pygame.mask.from_surface(self.img)
            self.spd = 3

        if lvl==2:
            pass

