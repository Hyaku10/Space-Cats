# IMPORTS
import pygame
import random
import subroutine
import math
import out_of_game_menus
from threading import Thread


# pygame.__init__
pygame.mixer.init()
pygame.display.init()
pygame.font.init()

# FONTS
num_font = pygame.font.SysFont("04B_30__", 50)

# VISUAL ASSETS
# BULLETS
fireball_img = pygame.image.load("assets/007-fire-1.png").convert_alpha()
bullet_normal_img = pygame.transform.scale(pygame.image.load('assets/bullet.png'), (16, 16)).convert_alpha()
bullet_fire_img = pygame.transform.rotate(fireball_img, 180).convert_alpha()
bullet_ice_img = pygame.image.load("assets/008-moonstone.png").convert_alpha()
bullet_electric_img = pygame.image.load("assets/010-lighting.png").convert_alpha()
bullet_rainbow_img = pygame.image.load("assets/rainbow pixels.png").convert_alpha()
inverted_bullet_img = pygame.transform.rotate(bullet_normal_img, 180).convert_alpha()
# SCREEN
background = pygame.image.load('assets/background2.png').convert_alpha()
icon = pygame.image.load('assets/007-cat-2.png').convert_alpha()
hp_icon = pygame.image.load("assets/005-paw.png").convert_alpha()
drop_fire_img = fireball_img
drop_ice_img = pygame.image.load("assets/003-snowflake.png").convert_alpha()
drop_electric_img = pygame.image.load("assets/004-lightning.png").convert_alpha()
drop_rainbow_img = pygame.image.load("assets/001-horn.png").convert_alpha()
question_mark_img = pygame.image.load("assets/001-question.png").convert_alpha()
crystal_img = pygame.image.load("assets/002-emerald-1.png").convert_alpha()
# CATS
pla_img = pygame.image.load("assets/002-grinning.png").convert_alpha()
enelvl1_img = pygame.image.load("assets/001-cyclops-1.png").convert_alpha()
enelvl2_img = pygame.image.load("assets/002-monster.png").convert_alpha()
enelvl3_img = pygame.image.load("assets/006-cat-1.png").convert_alpha()
enelvl4_img = pygame.image.load("assets/002-cat-1.png")
enelvl4_img = pygame.transform.scale(enelvl4_img, (96, 96)).convert_alpha()
enelvl5_img = pygame.image.load('assets/ene_lvl_5.png')
enelvl5_img = pygame.transform.scale(enelvl5_img, (96, 96)).convert_alpha()

# WINDOW
WIDTH = 1000
HEIGHT = 600
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Cats")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
stop_threads = False

# --------------------------------------------------------------------------------------------------

# GAME PARAMETERS
GROUND = 548
pla_x = WIDTH / 2 - 32 / 2
pla_y = GROUND - pla_img.get_height()
fpsclock = pygame.time.Clock()
FPS = 60
plaspd = 7
dropspd = 5
bulspd = 20
black = (0, 0, 0)
bulmax = 100
time_between_enemies1 = 100
time_between_enemies2 = 400
time_between_enemies3 = 1000
time_between_enemies4 = 1500
time_between_enemies5 = 2000
arc_bullet_step = 10
arc_bullet_start = 90
arc_bullet_end = 270 + arc_bullet_step


# CONTAINERS
aimed_ene_clip = []
clip = []
drops_list = []
ene_clip = []
arc_bullet_clip = []
ene_dict = {'l1': [],
            'l2': [],
            'l3': [],
            'l4': [],
            'l5': []}

power_ups = {'fire': [],
             'ice': [],
             'electric': [],
             'rainbow': [],
             'arc bullet': []}

# -------------------------------------------------------------------------

# CLASSES
class Drop:
    def __init__(self, x, y, kind=None):
        self.x = x
        self.y = y
        self.kind = kind
        self.img = pla_img

        if self.kind == "crystal":
            self.img = crystal_img

        if self.kind == "fire":
            self.img = crystal_img

        if self.kind == "ice":
            self.img = crystal_img

        if self.kind == "electric":
            self.img = crystal_img

        self.mask = pygame.mask.from_surface(self.img)

    def draw(self):
        WIN.blit(self.img, (self.x, self.y))

    def collision(self, obj):
        return collide(obj, self)

    def pick_up(self, player):
        if self.kind == "crystal":
            player.health += 10
            # Max health enforcer
            if player.health > player.max_health:
                player.health = player.max_health

    def get_height(self):
        return self.img.get_height()
class Player:
    def __init__(self, x=pla_x, y=pla_y, health=100):
        self.health = health
        self.max_health = health
        self.img = pla_img
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(self.img)
        self.spd = plaspd
        self.bullet_type = "normal"
        # pygame.Rect(450, 517, 32, 32)

    # DRAW PLAYER
    def draw(self):
        WIN.blit(self.img, (self.x, self.y))
class Enemy:
    def __init__(self, lvl, y=-50):
        # Pre-Enemy Global Attributes
        self.x = random.randint(50, 950)
        self.y = y
        self.lvl = lvl
        self.isexploding = False

        # Level specific
        if lvl == 1:
            self.direction = random.choice([True, False])
            self.health = 5
            self.img = enelvl1_img
            self.spd = 1
        elif lvl == 2:
            self.health = 5
            self.img = enelvl2_img
            self.spd = 1
        elif lvl == 3:
            self.health = 5
            self.img = enelvl3_img

            # Movement Attributes:

            # Dimensions
            self.actual_x = self.x
            self.init_x = self.x
            self.time = 0
            # Velocity & Acc
            self.v = 0
            self.acc = (1 / 9) / 4
            self.neg_acc = self.acc * -1
            self.temp = 0
            # Target & Halfway
            self.target_location = random.randint(0, WIDTH - 1)
            self.half_way = True
            # Control/State var
            self.isgoing = False
            self.isshooting = False

        elif lvl == 4:
            self.health = 10
            self.img = enelvl4_img
            self.isspawning = True

            # Movement Attributes X:

            # Dimensions
            self.actual_x = self.x
            self.init_x = self.x
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

        elif lvl == 5:
            self.health = 30
            self.img = enelvl5_img
            self.spd = 3
            self.direction = random.choice([True, False])
            self.y = y-50


        # Post Global Attributes
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = self.health

        if self.lvl == 5 or self.lvl == 4:
            self.hp_bar = pygame.Rect(self.x, self.y - 8, self.img.get_width(), 6)

    # Methods
    def draw(self):
        if hasattr(self, 'hp_bar'):
            self.hp_bar.x = self.x
            self.hp_bar.y = self.y - 8

            self.hp_bar.w = round(self.img.get_width() * (self.health/self.max_health))
            pygame.draw.rect(WIN, (0,255,0), self.hp_bar)
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

    def collision(self, obj):
        return collide(obj, self)

    def __str__(self):
        return f'Enemy LVL {self.lvl} with x: {self.x} and y: {self.y}'

    def __repr__(self):
        return f'|e{self.lvl} ({self.x}x, {self.y}y)|'
class Bullet:
    def __init__(self, x, y, mode=None):
        self.x = x
        self.y = y
        self.mode = mode
        self.b_spd = bulspd
        self.damage = 0
        self.img = bullet_normal_img

        # BULLET MODES
        if mode == "normal":
            self.x += 8
            self.img = bullet_normal_img
            self.damage = 5

        if mode == "fire":
            self.img = bullet_fire_img
            self.damage = 10

        if mode == "ice":
            self.img = bullet_ice_img
            self.damage = 5

        if mode == "electric":
            self.img = bullet_electric_img
            self.damage = 10

        if mode == "rainbow":
            self.img = bullet_rainbow_img
            self.damage = 999

        self.mask = pygame.mask.from_surface(self.img)

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
    def __init__(self, x, y, src, mode=None):
        super().__init__(x, y, mode)

        self.img = fireball_img
        self.mask = pygame.mask.from_surface(self.img)
        self.b_spd = bulspd
        self.src = src
        self.dmg = 5

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

class arc_bullet(Bullet):
    def __init__(self, x, y, mode, angle):
        super().__init__(x, y, mode)
        self.actual_x = x
        self.actual_y = y
        self.angle_degrees = angle
        rad_angle = math.radians(angle)
        self.img = pygame.transform.rotate(self.img, angle+180).convert_alpha()
        self.rx = self.b_spd * math.sin(rad_angle)
        self.ry = self.b_spd * math.cos(rad_angle)

    def move_aimed(self):
        self.actual_x += self.rx
        self.actual_y += self.ry
        self.x = round(self.actual_x)
        self.y = round(self.actual_y)

    def kill_arc(self, i):
        if self in arc_bullet_clip[i]:
            arc_bullet_clip[i].remove(self)

    def __repr__(self):
        return f'angle{self.angle_degrees} act x{self.actual_x} rx{self.rx}'

# ------------------------------------------------------------------------------------------

# UTILITY FX
def draw_window(bg):
    WIN.blit(bg, (0, 0))
def collide(obj1, obj2):
    xdistance = obj2.x - obj1.x
    ydistance = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (xdistance, ydistance)) is not None
def display_HP(HP):
    WIN.blit(hp_icon, (10, HEIGHT - 42))
    pygame.draw.rect(WIN, (255, 0, 0), (50, HEIGHT - 42, 200, 32), 0)
    pygame.draw.rect(WIN, (0, 255, 0), (50, HEIGHT - 42, HP*2, 32), 0)
def display_power_ups(power_ups, player, selected_bullet):
    #SELECT
    pygame.draw.rect(WIN, (255, 0, 0), (300, HEIGHT - 42 - 5, 60, 42), 0)
    pygame.draw.rect(WIN, (0, 0, 255), (360, HEIGHT - 42 - 5, 60, 42), 0)
    pygame.draw.rect(WIN, (255, 255, 0), (420, HEIGHT - 42 - 5, 60, 42), 0)
    pygame.draw.rect(WIN, (0, 0, 0), (480+60, HEIGHT - 42 - 5, 60, 42), 0)
    if player.bullet_type == "rainbow" or len(power_ups["rainbow"]) > 0:
        pygame.draw.rect(WIN, (204, 204, 0), (480, HEIGHT - 42 - 5, 60, 42), 0)
    else:
        pygame.draw.rect(WIN, (100, 100, 100), (480, HEIGHT - 42 - 5, 60, 42), 0)
    if selected_bullet == 0:
        pygame.draw.rect(WIN, (0, 128, 0), (300 - 2, HEIGHT - 42 - 5 -2, 64, 46), 0)
    if selected_bullet == 1:
        pygame.draw.rect(WIN, (0, 128, 0), (360 - 2, HEIGHT - 42 - 5 - 2, 64, 46), 0)
    if selected_bullet == 2:
        pygame.draw.rect(WIN, (0, 128, 0), (420 - 2, HEIGHT - 42 - 5 -2, 64, 46), 0)
    if selected_bullet == 3:
        pygame.draw.rect(WIN, (0, 128, 0), (480 - 2, HEIGHT - 42 - 5 - 2, 64, 46), 0)
    if selected_bullet == 4:
        pygame.draw.rect(WIN, (0, 128, 0), (480+60 - 2, HEIGHT - 42 - 5 - 2, 64, 46), 0)
    #FIRE
    pygame.draw.rect(WIN, (255, 200, 200), (305, HEIGHT - 42 , 50, 32), 0)
    WIN.blit(fireball_img, (305, HEIGHT - 42))
    fire_label = num_font.render(str(len(power_ups["fire"])), True, (0, 0, 0))
    WIN.blit(fire_label, (305 + 30, HEIGHT - 42))
    #ICE
    pygame.draw.rect(WIN, (200, 200, 255), (365, HEIGHT - 42, 50, 32), 0)
    WIN.blit(drop_ice_img, (365, HEIGHT - 42))
    ice_label = num_font.render(str(len(power_ups["ice"])), True, (0, 0, 0))
    WIN.blit(ice_label, (365 + 30, HEIGHT - 42))
    #ELECTRIC
    pygame.draw.rect(WIN, (255, 255, 200), (425, HEIGHT - 42, 50, 32), 0)
    WIN.blit(drop_electric_img, (425, HEIGHT - 42))
    electric_label = num_font.render(str(len(power_ups["electric"])), True, (0, 0, 0))
    WIN.blit(electric_label, (425 + 30, HEIGHT - 42))
    #RAINBOW
    if player.bullet_type == "rainbow" or len(power_ups["rainbow"]) > 0:
        pygame.draw.rect(WIN, (218, 165, 32), (485, HEIGHT - 42, 50, 32), 0)
        WIN.blit(drop_rainbow_img, (485, HEIGHT - 42))
        rainbow_label = num_font.render(str(len(power_ups["rainbow"])), True, (0, 0, 0))
        WIN.blit(rainbow_label, (485 + 30, HEIGHT - 42))
    else:
        pygame.draw.rect(WIN, (200, 200, 200), (485, HEIGHT - 42, 50, 32), 0)
        WIN.blit(question_mark_img, (485, HEIGHT - 42))
        rainbow_label = num_font.render(str(len(power_ups["rainbow"])), True, (0, 0, 0))
        WIN.blit(rainbow_label, (485 + 30, HEIGHT - 42))

    pygame.draw.rect(WIN, (150, 150, 150), (485+60, HEIGHT - 42, 50, 32), 0)
    WIN.blit(bullet_normal_img, (485+60, HEIGHT - 42))
    arc_b_label = num_font.render(str(len(power_ups["arc bullet"])), True, (0, 0, 0))
    WIN.blit(arc_b_label, (485 + 90, HEIGHT - 42))

def drop(dropper):
    drop = random.randint(1, 10)
    if drop == 7:
        #drop2 = random.randint(1, 4)
        drop2 = 1
        if drop2 == 1:
            drops_list.append(Drop(dropper.x, dropper.y, "crystal"))
        if drop2 == 2:
            drops_list.append(Drop(dropper.x, dropper.y, "fire"))
        if drop2 == 3:
            drops_list.append(Drop(dropper.x, dropper.y, "ice"))
        if drop2 == 4:
            drops_list.append(Drop(dropper.x, dropper.y, "electric"))
def arc_bullet_add(player):
    l_=[]
    for angle in range(arc_bullet_start, arc_bullet_end, arc_bullet_step):
        temp = arc_bullet(player.x, player.y, player.bullet_type, angle)
        temp.move_aimed()
        #temp.move_aimed()
        l_.append(temp)
    return l_

# HANDLERS
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

    if len(arc_bullet_clip) != 0:
        #squash_arc_b = subroutine.list_squasher(arc_bullet_clip)
        for i, v in enumerate(arc_bullet_clip):
            for arc_b in v:
                # move
                arc_b.move_aimed()
                arc_b.draw()

                # out of screen
                if arc_b.y < 1:
                    arc_b.kill_arc(i)
                elif not 0 < arc_b.x < WIDTH:
                    arc_b.kill_arc(i)

                # Enemy-Bullet Collision
                for enemy in ene_full_list:
                    if arc_b.collision(enemy) and enemy.health > 0:
                        enemy.health -= 5
                        arc_b.kill_arc(i)



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

        '''Bullet-EneBullet Collision
            for b in clip:
                if e_b.collision(b):
                    print('BULLET COLLISION!')
                    e_b.kill()
                    b.kill()
                    subroutine.exp_sfx.play()'''
        [WIN.blit(e_b.img, (e_b.x, e_b.y)) for e_b in ene_clip]

    if len(aimed_ene_clip) != 0:
        for aimed_b in aimed_ene_clip:
            aimed_b.move_aimed()

            if aimed_b.y > HEIGHT:
                aimed_b.kill()

            # Kill if shooter died
            if aimed_b.src not in ene_dict['l4']:
                aimed_b.kill()

            # Player-EneBullet Collision
            if aimed_b.collision(player):
                subroutine.player_got_hit(player)
                aimed_b.kill()

            # Bullet-EneBullet Collision
        #     for b in clip:
        #         if aimed_b.collision(b):
        #             print('AIMED BULLET COLLISION!')
        #             aimed_b.kill()
        #             b.kill()
        #             subroutine.exp_sfx.play()
        [WIN.blit(aimed_b.img, (aimed_b.x, aimed_b.y)) for aimed_b in aimed_ene_clip]
def handle_enemies(ene_dict, player):
    ene = subroutine.ene_dict_to_ene_list(ene_dict)

    for enemy in ene:
        if enemy.health <= 0:
            # Explosion
            if enemy.isexploding == False:
                enemy.isexploding = True
                drop(enemy)
                exp_thread = Thread(target=subroutine.explosion, args=(enemy, subroutine.explosion_gif_list,))
                exp_thread.start()

        # Enemy Movement and actions
        if enemy.health > 0 and enemy.lvl == 1:
            subroutine.lvl1_handle(enemy)
        elif enemy.health > 0 and enemy.lvl == 2:
            subroutine.lvl2_handle(player, enemy)
        elif enemy.health > 0 and enemy.lvl == 3:
            subroutine.lvl3_handle(enemy)
        elif enemy.health > 0 and enemy.lvl == 4:
            subroutine.lvl4_handle(player, enemy)
        elif enemy.health > 0 and enemy.lvl == 5:
            subroutine.lvl5_handle(enemy, player)

            # enemy.img = subroutine.health_img_transfer(enemy)

        # Player enemy collision
        if collide(enemy, player) and enemy.health > 0:
            subroutine.player_got_hit(player)
            enemy.kill()

        # Update visuals of enemy
        enemy.draw()
def handle_drops(drops_list, player):
    for drop in drops_list:
        if drop.y < GROUND - drop.get_height() - 5:
            drop.y += dropspd
        drop.draw()
        if drop.collision(player):
            drop.pick_up(player)
            drops_list.remove(drop)

# ----------------------------------------------------------------------------------------

# MAIN
def main():
    # Loop variable declaration

    # Player and Loop's run
    global arc_bullet_clip
    global stop_threads
    run = True
    player = Player()
    pla_x = player.x
    selected_bullet = 0

    # Spawn Clocks
    clocklvl1 = 0
    clocklvl2 = 0
    clocklvl3 = 0
    clocklvl4 = 0
    clocklvl5 = 0

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
                    bullet = Bullet(player.x, player.y, player.bullet_type)
                    clip.append(bullet)

                # ESCAPE
                elif event.key == pygame.K_ESCAPE:
                    print("escape")
                    print(player.bullet_type)
                    # MISSING ESCAPE MENU

                # CHEAT CODES
                elif event.key == pygame.K_r:
                    player.bullet_type = "rainbow"
                elif event.key == pygame.K_i:
                    player.bullet_type = 'ice'
                elif event.key == pygame.K_u:
                    arc_bullet_clip.append(arc_bullet_add(player))

                # SELECTING BULLET TYPE
                if event.key == pygame.K_DOWN:
                    selected_bullet += 1
                    if selected_bullet > 4:
                        selected_bullet = 0


        # HANDLE PLAYER MOVEMENT
        key_pre = pygame.key.get_pressed()
        if key_pre[pygame.K_RIGHT] and player.x < WIDTH - 32:
            pla_x += plaspd
        if key_pre[pygame.K_LEFT] and player.x + plaspd > 0:
            pla_x -= plaspd
        player.x = round(pla_x)

        #secret weapon drop(WIP)
        if key_pre[pygame.K_SPACE] and player.bullet_type == "rainbow":
            bullet = Bullet(player.x, player.y, "rainbow")
            clip.append(bullet)

        # ----------------------------------------------

        # ENEMY SPAWN
        clocklvl1 += 1
        clocklvl2 += 1
        clocklvl3 += 1
        clocklvl4 += 1
        clocklvl5 += 1

        if clocklvl1 > time_between_enemies1:
            ene_dict['l1'].append(Enemy(1))
            clocklvl1 = 0
        if clocklvl2 > time_between_enemies2:
            ene_dict['l2'].append(Enemy(2))
            clocklvl2 = 0
        if clocklvl3 > time_between_enemies3:
            ene_dict['l3'].append(Enemy(3))
            clocklvl3 = 0
        if clocklvl4 > time_between_enemies4:
            ene_dict['l4'].append(Enemy(4))
            clocklvl4 = 0
        if clocklvl5 > time_between_enemies5:
            ene_dict['l5'].append(Enemy(5))
            clocklvl5 = 0


        # ----------------------------------------------

        # UPDATES: (Movement, Visuals, Game-state)

        # Draw background
        draw_window(background)

        # Handle bullets -> Handle enemies
        handle_bullets(clip, ene_dict, player, ene_clip, aimed_ene_clip)
        handle_enemies(ene_dict, player)
        handle_drops(drops_list, player)

        # Draw player and update display
        player.draw()
        display_HP(player.health)
        display_power_ups(power_ups, player, selected_bullet)
        pygame.display.update()
        


if __name__ == "__main__":
    main()

'''
REPORT
    Known Bugs - Level:
    1. Bullets disappear after source killed in mid air - On purpose
        Need to implement it at a thread level not here but havent gotten to that yet bc complicated

'''