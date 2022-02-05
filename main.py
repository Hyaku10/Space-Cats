# IMPORTS
import pygame
import math
import random
#pygame.__init__

# VISUAL ASSETS
background = pygame.image.load('background2.png')
icon = pygame.image.load('007-cat-2.png')
pla_img = pygame.image.load("002-grinning.png")
bullet_img = pygame.transform.scale(pygame.image.load('bullet.png'), (16, 16))
enelvl1_img = pygame.image.load("001-cyclops-1.png")
enelvl2_img = pygame.image.load("001-cyclops-1.png")

# WINDOW
WIN = pygame.display.set_mode((1000, 600))
pygame.display.set_icon(icon)
pygame.display.set_caption ("Space Cats")

# GAME PARAMETERS
clip = []
enelvl1_list = []
fpsclock = pygame.time.Clock()
FPS = 60
plaspd = 7
bulspd = 20
black = (0, 0, 0)
bulmax = 100
enelvl1spd = 3
enelvl2spd = 5
enelvl3spd = 5
enelvl4spd = 5
time_between_enemies1 = 100
time_between_enemies2 = 100
time_between_enemies3 = 100
time_between_enemies4 = 100


# ENEMY LEVEL 1 CLASS
class EneLvl1:
    def __init__(self, x, y, direction, health=10):
        self.x = x
        self.y = y
        self.direction = direction
        self.health = health
        self.img = enelvl1_img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self):
        WIN.blit(self.img, (self.x, self.y))

    def kill(self):
        enelvl1_list.erase(enemy)

    def collision(self, obj):
        return collide(obj, self)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = bullet_img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self):
        WIN.blit(self.img, (self.x, self.y))

    def kill(self):
        clip.remove(self)

    def collision(self, obj):
        return collide(obj, self)


def collide(obj1, obj2):
    xdistance = obj2.x - obj1.x
    ydistance = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask , (xdistance, ydistance)) != None


# DRAW WINDOW
def draw_window():
    WIN.blit(background, (0, 0))


# DRAW PLAYER
def draw_player(player):
    WIN.blit(pla_img, (player.x, player.y))


# HANDLE BULLETS
def handle_bullets(clip, enelvl1_list):
    for bullet in clip:
        bullet.draw()
        bullet.y -= bulspd
        if bullet.y < 1:
            bullet.kill()
        for enemy in enelvl1_list:
            if bullet.collision(enemy):
                enemy.health -= 5
                enelvl1_list.remove(enemy)


# HANDLE ENEMIES
def handle_enemies(enelvl1_list):
    if len(enelvl1_list) > 0:
        for enemy in enelvl1_list:
            enemy.draw()
            if enemy.direction == True:
                enemy.x += enelvl1spd
                if enemy.x > 950:
                    enemy.direction = False
                    enemy.y += 50
            elif enemy.direction == False:
                enemy.x -= enelvl1spd
                if enemy.x < 50:
                    enemy.direction = True
                    enemy.y += 50
            elif enemy.y > 600:
                enemies.remove(enemy)
            elif enemy.health <= 0:
                enemy.kill()
    return enelvl1_list


# MAIN GAME LOOP
def main():
    run = True
    pla_x, pla_y = 450, 517
    player = pygame.Rect(450, 517, 32, 32)
    clocklvl1 = 0
    clocklvl2 = 0
    clocklvl3 = 0
    clocklvl4 = 0

    while run:
        fpsclock.tick(FPS)
        shot = False

        # WINDOW X BUTTON
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # SHOOTING
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(clip) < bulmax:
                    bullet = Bullet(player.x + 8, player.y)
                    clip.append(bullet)

        # HANDLE PLAYER MOVEMENT
        key_pre = pygame.key.get_pressed()
        if key_pre[pygame.K_RIGHT] and player.x < 1000 - 32:
            pla_x += plaspd
        if key_pre[pygame.K_LEFT] and player.x + plaspd > 0:
            pla_x -= plaspd
        player.x = round(pla_x)

        # ENEMY SPAWN CLOCKS
        clocklvl1 += 1
        if clocklvl1 > time_between_enemies1:
            enemylvl1 = EneLvl1(random.randint(50, 950), -50, random.choice([True, False]))
            enelvl1_list.append(enemylvl1)
            clocklvl1 = 0
        if clocklvl2 > time_between_enemies2:
            enemylvl2 = EneLvl2(random.randint(50, 950), -50, random.choice([True, False]))
            enelvl1_list.append(enemylvl2)
            clocklvl2 = 0
        if clocklvl3 > time_between_enemies3:
            enemylvl3 = EneLvl3(random.randint(50, 950), -50, random.choice([True, False]))
            enelvl3_list.append(enemylvl3)
            clocklvl3 = 0
        if clocklvl4 > time_between_enemies4:
            enemylvl4 = EneLvl4(random.randint(50, 950), -50, random.choice([True, False]))
            enelvl4_list.append(enemylvl4)
            clocklvl4 = 0


        draw_window()
        handle_bullets(clip, enelvl1_list)
        handle_enemies(enelvl1_list)
        draw_player(player)
        pygame.display.update()

'''
    def MENU():
        run = True
        plaX, plaY = 450, 517
        player = pygame.Rect(450, 517, 32, 32)
        clip = []
        while run == True:
            shot = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and len(clip) < bulmax:
                        bullet = pygame.Rect(player.x + 8, player.y, 16, 16)
                        clip.append(bullet)
            key_pre = pygame.key.get_pressed()
            if key_pre[pygame.K_RIGHT] and player.x < 1000 - 32:
                plaX += plaSpeed
            if key_pre[pygame.K_LEFT] and player.x + plaSpeed > 0:
                plaX -= plaSpeed
            player.x = round(plaX)
            draw_window(player)
            handle_bullets(clip, player)
            pygame.display.update()
        pygame.QUIT
        '''
if __name__ == "__main__":
   main()