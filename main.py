# IMPORTS
import pygame
import random
import subroutine
import out_of_game_menus
import math
from threading import Thread
pygame.mixer.init()
pygame.display.init()
# pygame.__init__

# WINDOW
WIDTH = 1000
HEIGHT = 600
pygame.display.set_caption("Space Cats")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
stop_threads = False

# VISUAL ASSETS
background = pygame.image.load('assets/background2.png')
icon = pygame.image.load('assets/007-cat-2.png')
pla_img = pygame.image.load("assets/002-grinning.png")
bullet_img = pygame.transform.scale(pygame.image.load('assets/bullet.png'), (16, 16))
inverted_bullet_img = pygame.transform.rotate(bullet_img, 180)
enelvl1_img = pygame.image.load("assets/001-cyclops-1.png").convert_alpha()
enelvl2_img = pygame.image.load("assets/002-monster.png")
enelvl3_img = pygame.image.load("assets/006-cat-1.png")
enelvl4_img = pygame.image.load("assets/002-cat-1.png")
enelvl4_img = pygame.transform.scale(enelvl4_img, (32*3, 32*3))
enelvl5_img = pygame.transform.scale(enelvl1_img, (32*2,32*2))
#--
background = pygame.Surface.convert(background)
pla_img = pygame.Surface.convert_alpha(pla_img)
bullet_img = pygame.Surface.convert_alpha(bullet_img)
inverted_bullet_img = pygame.Surface.convert_alpha(inverted_bullet_img)
enelvl1_img = pygame.Surface.convert_alpha(enelvl1_img)
enelvl2_img = pygame.Surface.convert_alpha(enelvl2_img)
enelvl3_img = pygame.Surface.convert_alpha(enelvl3_img)
enelvl4_img = pygame.Surface.convert_alpha(enelvl4_img)
enelvl5_img = pygame.Surface.convert_alpha(enelvl5_img)

pygame.display.set_icon(icon)

# GAME PARAMETERS
pla_x = WIDTH / 2 - 32 / 2
pla_y = 517
fpsclock = pygame.time.Clock()
FPS = 60
plaspd = 7
bulspd = 20
black = (0, 0, 0)
green = (0, 255, 0)
bulmax = 100
time_between_enemies1 = 100
time_between_enemies2 = 200
time_between_enemies3 = 600
time_between_enemies4 = 400
time_between_enemies5 = 500
time_between_enemies6 = 300

# CONTAINERS
ene_clip = []
aimed_ene_clip = []
clip = []
ene_dict = {'l1': [],
            'l2': [],
            'l3': [],
            'l4': [],
            'l5': [],
            'l6': []}

# l1 = level1, etc... here on out
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------


# CLASSES

class Player:
    def __init__(self, x = pla_x, y = pla_y, health=30):
        self.health = health
        self.max_health = health
        self.img = pla_img
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(self.img)
        self.spd = plaspd
        # pygame.Rect(450, 517, 32, 32)

    # DRAW PLAYER
    def draw(self):
        WIN.blit(self.img, (self.x, self.y))

class Enemy:
    def __init__(self, lvl):
        # Pre-Enemy Global Attributes
        self.x = random.randint(50,950)
        self.y = -50
        self.lvl = lvl
        self.isexploding = False

        x = self.x
        y = self.y
        # Level specific
        if lvl == 1:
            self.direction = True
            self.health = 5
            self.img = enelvl1_img
            self.spd = 3
        elif lvl == 2:
            self.health = 5
            self.img = enelvl2_img
            self.spd = 2
        elif lvl == 3:
            self.health = 5
            self.img = enelvl3_img

            # Movement Attributes:

            # Dimensions
            self.actual_x = x
            self.init_x = x
            self.time = 0
            # Velocity & Acc
            self.v = 0
            self.acc = (1/9)
            self.neg_acc = self.acc * -1
            self.temp = 0
            # Target & Halfway
            self.target_location = random.randint(0, WIDTH - 1)
            self.half_way = True
            # Control/State var
            self.isgoing = False
            self.isshooting = False
        elif lvl == 4:
            self.health = 5
            self.img = enelvl4_img
            self.spd = 7
        elif lvl == 5:
            self.health = 30
            self.img = enelvl5_img
            self.spd = 6
            self.direction = False
        elif lvl == 6:
            self.health = 10
            self.img = enelvl4_img
            self.isspawning = True

            # Movement Attributes X:

            # Dimensions
            self.actual_x = x
            self.init_x = x
            self.time = 0
            # Velocity & Acc
            self.v = 0
            self.acc = (1/9)
            self.neg_acc = self.acc * -1
            self.temp = 0
            # Target & Halfway
            self.target_location = random.randint(32*3, WIDTH - 32*3)
            self.half_way = True
            # Control/State var
            self.isgoing_x = False
            self.isshooting = False

            # Movement Attributes Y:

            # Dimensions
            self.actual_y = y
            self.init_y = y
            self.time_y = 0
            # Velocity & Acc
            self.v_y = 0
            self.acc_y = 1/9
            self.neg_acc_y = self.acc_y * -1
            self.temp_y = 0
            # Target & Halfway
            self.target_location_y = random.randint(32*3, 600)
            self.half_way_y = True
            # Control/State var
            self.isgoing_y = False


        # Post Global Attributes
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = self.health

        if self.lvl == 5 or self.lvl == 6:
            self.hp_bar = pygame.Rect(self.x, self.y -8, self.img.get_width(), 6)

    # Methods
    def draw(self):
        if hasattr(self, 'hp_bar'):
            self.hp_bar.x = self.x
            self.hp_bar.y = self.y - 8

            self.hp_bar.w = round(self.img.get_width() * (self.health/self.max_health))
            pygame.draw.rect(WIN, green, self.hp_bar)
        WIN.blit(self.img, (self.x, self.y))


    def kill(self):
        if self.lvl == 1 and self in ene_dict['l1']:
            ene_dict['l1'].remove(self)
        elif self.lvl == 2 and self in ene_dict['l2']:
            ene_dict['l2'].remove(self)
        elif self.lvl == 3 and self in ene_dict['l3']:
            ene_dict['l3'].remove(self)
        elif self.lvl == 4 and self in ene_dict['l4']:
            ene_dict['l4'].remove(self)
        elif self.lvl == 5 and self in ene_dict['l5']:
            ene_dict['l5'].remove(self)
        elif self.lvl == 6 and self in ene_dict['l6']:
            ene_dict['l6'].remove(self)

    def collision(self, obj):
        return collide(obj, self)

    def __str__(self):
        return f'Enemy LVL {self.lvl} with x: {self.x} and y: {self.y}'

    def __repr__(self):
        return f'|e{self.lvl} ({self.x}x, {self.y}y)|'

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = bullet_img
        self.mask = pygame.mask.from_surface(self.img)
        self.b_spd = bulspd

    # Methods
    def draw(self):
        WIN.blit(self.img, (self.x, self.y))

    def kill(self):
        if self in clip:
            clip.remove(self)

    def collision(self, obj):
        return collide(obj, self)

class Enemy_bullet(Bullet):
    # Attributes: reversed bullet img, b_spd -- (inherited) x, y, mask,
    def __init__(self, x, y, src):
        super().__init__(x, y)

        self.img = inverted_bullet_img
        self.b_spd = bulspd/3
        self.src = src

    # Methods
    # collision (inherited)
    def kill(self):
        if self in subroutine.ene_clip:
            subroutine.ene_clip.remove(self)
    def move_down(self):
        self.y += self.b_spd

    def __str__(self):
        return f'Enemy Bullet with x: {self.x} and y: {self.y}'

    def __repr__(self):
        return f'|e_b - ({self.x}x, {self.y}y)|'

class Aimed_Enemy_bullet(Enemy_bullet):
    def __init__(self, x, y, src, player):
        super().__init__(x, y, src)
        self.actual_x = x
        self.actual_y = y
        self.b_spd = bulspd/2

        # Calculations
        dy = src.y - player.y + 16
        dx = src.x - player.x + 16
        slope = dx / dy
        rad_angle = math.atan(abs(slope))
        calc_angle = (rad_angle*180)/math.pi
        self.slope = slope
        if slope < 0:
            calc_angle = 360 - calc_angle
            rad_angle = 2*math.pi - rad_angle

        self.img = pygame.transform.rotate(inverted_bullet_img, calc_angle).convert_alpha()

        # rate of x and y change according to length of hypotenous traveled
        self.rx = self.b_spd * math.sin(rad_angle)
        self.ry = self.b_spd * math.cos(rad_angle)

        # calc slope
        # calc img angle
        # define img

    # movement method
    def move_aimed(self):
        self.actual_x += self.rx
        self.actual_y += self.ry
        self.x = round(self.actual_x)
        self.y = round(self.actual_y)

    def kill(self):
        if self in subroutine.aimed_ene_clip:
            subroutine.aimed_ene_clip.remove(self)



# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------

# UTILITY FX
def draw_window(bg):
    WIN.blit(bg, (0, 0))

def collide(obj1, obj2):
    xdistance = obj2.x - obj1.x
    ydistance = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask , (xdistance, ydistance)) != None


# HANDLERS

# Handle Bullets
def handle_bullets(clip, ene_dict, player, ene_clip, aimed_ene_clip):
    ene_full_list = subroutine.ene_dict_to_ene_list(ene_dict)

    # PLAYER BULLETS
    new_clip = [b for b in clip]
    for bullet in new_clip:
        # Move and draw
        bullet.y -= bulspd
        bullet.draw()

        # Kill if flies off screen (upwards)
        if bullet.y < 1:
            bullet.kill()

        # Enemy-Bullet Collision
        for enemy in ene_full_list:
            if bullet.collision(enemy) and enemy.health > 0:
                enemy.health -= 5
                bullet.kill()

    # ENEMY BULLETS
    if len(ene_clip) != 0:
        for e_b in ene_clip:

            # Move and draw
            e_b.move_down()
            # Kill if flies off screen (downwards)
            if e_b.y > HEIGHT:
                e_b.kill()
            # Kill if shooter died
            if e_b.src not in ene_dict['l3']:
                e_b.kill()

            # Player-EneBullet Collision
            if e_b.collision(player):
                subroutine.player_got_hit(player)
                e_b.kill()

            # Bullet-EneBullet Collision
            for b in clip:
                if e_b.collision(b):
                    print('BULLET COLLISION!')
                    e_b.kill()
                    b.kill()
                    subroutine.exp_sfx.play()
        [WIN.blit(e_b.img, (e_b.x, e_b.y)) for e_b in ene_clip]

    if len(aimed_ene_clip) != 0:
        for aimed_b in aimed_ene_clip:
            aimed_b.move_aimed()

            if aimed_b.y > HEIGHT:
                aimed_b.kill()

            # Kill if shooter died
            if aimed_b.src not in ene_dict['l6']:
                aimed_b.kill()

            # Player-EneBullet Collision
            if aimed_b.collision(player):
                subroutine.player_got_hit(player)
                aimed_b.kill()

            # Bullet-EneBullet Collision
            for b in clip:
                if aimed_b.collision(b):
                    print('AIMED BULLET COLLISION!')
                    aimed_b.kill()
                    b.kill()
                    subroutine.exp_sfx.play()
        [WIN.blit(aimed_b.img, (aimed_b.x, aimed_b.y)) for aimed_b in aimed_ene_clip]
# Handle Enemies
def handle_enemies(ene_dict, player):
    ene = subroutine.ene_dict_to_ene_list(ene_dict)

    for enemy in ene:

        # Explosion
        if enemy.health <= 0:
            if enemy.isexploding == False:
                enemy.isexploding = True
                exp_thread = Thread(target=subroutine.explosion, args=(enemy, subroutine.explosion_gif_list,))
                exp_thread.start()

        # Enemy Movement and actions
        if enemy.health > 0 and enemy.lvl == 1:
            subroutine.lvl1_handle(enemy)
        elif enemy.health > 0 and enemy.lvl == 2:
            subroutine.lvl2_handle(player, enemy)
        elif enemy.health > 0 and enemy.lvl == 3:
            subroutine.lvl3_handle(enemy)
        elif enemy.health > 0 and enemy.lvl == 5:
            subroutine.lvl5_handle(enemy, player)
        elif enemy.health > 0 and enemy.lvl == 6:
            subroutine.lvl6_handle(player, enemy)

            # enemy.img = subroutine.health_img_transfer(enemy)

        # Player enemy collision
        if collide(enemy, player) and enemy.health > 0:
            subroutine.player_got_hit(player)
            enemy.kill()

        # Update visuals of enemy
        enemy.draw()


# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------


# MAIN
def main():
# Loop variable declaration

    # Player and Loop's run
    global stop_threads
    run = True
    player = Player()
    pla_x = player.x

    # Spawn Clocks
    clocklvl1 = 0
    clocklvl2 = 0
    clocklvl3 = 50
    clocklvl4 = 0
    clocklvl5 = 0
    clocklvl6 = 0

    # Starting Menu
    out_of_game_menus.start_menu()

    # Start Game  (Fade out/in black, etc...)
    pygame.mixer.music.fadeout(3)
    pygame.mixer.music.load('assets/bgm.mp3')
    pygame.mixer.music.play(-1)
        # MISSING:
            # FADE TO BLACK FX

# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# LOOP

    while run:
        fpsclock.tick(FPS)
        ene_clip = subroutine.ene_clip
        aimed_ene_clip = subroutine.aimed_ene_clip

        # WINDOW X BUTTON
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                stop_threads = True

            # SHOOTING
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(clip) < bulmax:
                    bullet = Bullet(player.x + 8, player.y)
                    clip.append(bullet)

                # ESCAPE
                elif event.key == pygame.K_ESCAPE:
                    print("escape")
                    # MISSING ESCAPE MENU

        # HANDLE PLAYER MOVEMENT
        key_pre = pygame.key.get_pressed()
        if key_pre[pygame.K_RIGHT] and player.x < WIDTH - 32:
            pla_x += plaspd
        if key_pre[pygame.K_LEFT] and player.x + plaspd > 0:
            pla_x -= plaspd
        player.x = round(pla_x)

        # ----------------------------------------------

        # ENEMY SPAWN
        clocklvl1 += 1
        clocklvl2 += 1
        clocklvl3 += 1
        #clocklvl4 += 1
        clocklvl5 += 1
        clocklvl6 += 1

        if clocklvl1 > time_between_enemies1:
            ene_dict['l1'].append(Enemy(1))
            clocklvl1 = 0
        if clocklvl2 > time_between_enemies2:
            ene_dict['l2'].append(Enemy(2))
            clocklvl2 = 0
        if clocklvl3 > time_between_enemies3:
            ene_dict['l3'].append(Enemy(3))
            clocklvl3 = 0
        # if clocklvl4 > time_between_enemies4:
        #     ene_dict['l4'].append(Enemy(4))
        #     clocklvl4 = 0

        if clocklvl5 > time_between_enemies5:
            ene_dict['l5'].append(Enemy(5))
            clocklvl5 = 0

        if clocklvl6 > time_between_enemies6:
            ene_dict['l6'].append(Enemy(6))
            clocklvl6 = 0
        # ----------------------------------------------

        # UPDATES: (Movement, Visuals, Game-state)

        # Draw background
        draw_window(background)

        # Handle bullets -> Handle enemies
        handle_bullets(clip, ene_dict, player, ene_clip, aimed_ene_clip)
        handle_enemies(ene_dict, player)

        # Draw player and update display
        player.draw()
        pygame.display.update()
        # if len(ene_dict['l6']) > 0:
        #     print(ene_dict['l6'])
        #     for i in ene_dict['l6']:
        #         print(i)
        #         print(f'ix {i.init_x} iy {i.init_y} | ax {i.actual_x} ay {i.actual_y}')
        #         print(f'gx {i.isgoing_x} | gy {i.isgoing_y} | shoot {i.isshooting} | spawn {i.isspawning}')
        #         print(f'tx {i.target_location} ty {i.target_location_y}')
        #         print('\n\n')
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------

# MISSING GAME OVER SCREEN and other post game fxs here


# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
   main()

'''
REPORT
    Known Bugs - Level:
        1. Those mfs start becoming fast... don't know why ¯\_(ツ)_/¯            -       |Important|
        
            - !!!STATUS OPEN!!!
            
            - I think it has to do with overloading the program causing it to bypass fps check and run it as 
              fast as possible, though I really don't know whats causing this.
            
        2. Explosions track formerly alive enemy despite the fact that they shouldn't  -  |Minute|
        
            - Fixed with unoptimal solution of adding if statement at beginning of each subroutine handling
              enemy movement and actions. Though, I would like to fix the if statement in handle_enemies().
              
        3. l3 enemies teleport like 20% of the time                                 -     |Medium|
            
            -STATUS OPEN
            
            - I have the capacity to fix it, but let's focus on other things first. I'll fix it eventually, since 
              aesthetically its not nice, nor is it nice for my ego, but it really doesn't affect that much gameplay.
              
            - UPDATE STATUS CLOSED!
            
            - Error report: The problem was the parameters for the acc fx were still using my bug testing values
              of spawning in the middle of the screen, so whenever an l3 enemy would move for the first time
              it'd teleport to the middle of the screen
              
              -FIX:
                -self.actual_x = x
                -self.init_x = x




'''