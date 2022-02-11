import pygame
import main
from time import sleep
from threading import Thread
from math import ceil
from random import randint
from copy import deepcopy
global ene_clip
global aimed_ene_clip
pygame.display.init()
ene_clip = []
aimed_ene_clip = []
WIN = pygame.display.set_mode((1000, 600))

# SOUND
exp_sfx = pygame.mixer.Sound('assets/Explosion/9-bit.mp3')
oof = pygame.mixer.Sound('assets/angry-cat-rawr.mp3')
exp_sfx.set_volume(.05)
oof.set_volume(.2)

# SCREEN VAR
WIDTH = 1000
HEIGHT = 600

# ASSETS
explosion_gif_list = [pygame.image.load('assets/Explosion/frame_0_delay-0.png'),
                      pygame.image.load('assets/Explosion/frame_1_delay-0.png'),
                      pygame.image.load('assets/Explosion/frame_2_delay-0.png'),
                      pygame.image.load('assets/Explosion/frame_3_delay-0.png'),
                      pygame.image.load('assets/Explosion/frame_4_delay-0.png'),
                      pygame.image.load('assets/Explosion/frame_5_delay-0.png'),
                      pygame.image.load('assets/Explosion/frame_6_delay-0.png')]

explosion_gif_list = [pygame.Surface.convert_alpha(i) for i in explosion_gif_list]

# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
'''
Function's Order:

Utility
Enemy Movement
Enemy Handling
Miscellaneous
'''
# ------------------------------------------------------------------------------------------------------------
# UTILITY FXS


def player_got_hit(player):
    oof.play()
    player.health -= 5
    print(f'hp: {player.health}')
    if player.health <= 0:
        print('GAME OVER')
        print(f'hp: {player.health}')
        #main.run = False

def list_squasher(nested_list):
    squashed = []
    for list_ in nested_list:
        for item in list_:
            squashed.append(item)
    return squashed

def ene_dict_to_ene_list(ene_dict):
    values_ = ene_dict.values()
    full_l = list_squasher(values_)
    return full_l


# ------------------------------------------------------------------------------------------------------------
# ENEMY MOVEMENT
# creates the movement/actions of enemies and defines their movement patters


# L2
def home_in(self, obj):
    if self.lvl == 2:
        # See the range so the homing object does not over shoot the player
        range_x = obj.x - self.spd <= self.x <= obj.x + self.spd
        range_y = obj.y - self.spd <= self.y <= obj.y + self.spd
        range_xy = range_x and range_y

        # Moves closer by speed X axis
        if not range_x:

            # Enemy to the left
            if self.x > obj.x:
                self.x -= self.spd

            # Enemy to the right
            elif self.x < obj.x:
                self.x += self.spd

        # Moves closer by speed Y axis
        if not range_y:

            # Enemy Up
            if self.y > obj.y:
                self.y -= self.spd

            # Enemy Down
            elif self.y < obj.y:
                self.y += self.spd

        # Collide coordinates of player and enemy if the enemy is in x & y range of player
        if range_xy:
            self.x = obj.x
            self.y = obj.y


# L3
def position_update(self):
    self.x = round(self.actual_x)

def randomize_target_location(self):
    if self.lvl == 3:
        # Choose random target 50 units away
        # hw = 0
        # while hw < 50:
        self.target_location = randint(0, WIDTH - 1)
        #    hw = ((self.target_location - self.init_x) / 2) + self.init_x

        # Reset control checks for movement
        self.isshooting = False
        self.isgoing = True

# Threaded Shooting
def shootlvl3(self):

    # Shooting thread fx for l3
    if self.lvl == 3:

        # Activate control parameters
        self.isshooting = True

        # Shoot then rest then shoot for random range
        for i in range(randint(1,5)):
            ene_clip.append(main.Enemy_bullet(self.x+8, self.y+32, self))
            if main.stop_threads == True:
                return None
            # print(f'\n OG: ({self.x}x, {self.y}y)')
            # print(ene_clip)
            sleep(.5)

        # When done shooting go to a new location
        randomize_target_location(self)

        return None

def acc_method(self):
    # Formulas
    # v = v0 + at
    # x = x0 + vot + 1/2*a * t^2

    # Time check
    self.time += 1
    dist_to_target = self.target_location - self.actual_x
    hw = ((self.target_location - self.init_x) / 2) + self.init_x
   # if self.time == 1:
        # print(
        #     f'\n\nINIT - TARGET {self.target_location} | init x: {self.init_x} \ncurrent x: {self.actual_x}, {self.x} \n'
        #     f'dist to target: {dist_to_target} | hw: {hw} \n'
        #     f'half way: {self.half_way} | directionality: {dist_to_target > 0} | velocity {self.v} \n'
        #     f'time: {self.time}  |  acc: {self.acc} | temp: {self.temp}')

    # Directionality RIGHT
    if dist_to_target > 0:
        # False if dude is not over half way
        self.half_way = (self.actual_x >= hw)

        # IF ACC [RIGHT]
        if self.half_way is False:
            self.actual_x = self.init_x + (.5 * self.acc * (self.time ** 2))
            position_update(self)
            # Check if acc is finished -> reset for deceleration
            if self.actual_x >= hw:
                self.v = self.acc * self.time
                self.time = 0
                self.temp = deepcopy(self.actual_x)

        # IF DECELERATING [RIGHT]
        elif self.half_way is True:

            # Move
            self.actual_x = self.temp + self.v * self.time + (.5 * self.neg_acc * (self.time ** 2))
            position_update(self)
            # print(
            #     f'EQ: {self.actual_x} = {self.temp} + {self.v}*{self.time} + (.5) * {self.neg_acc} * {self.time ** 2}')
            # print(
            #     f'EQ: {self.actual_x} = {self.temp} + {self.v * self.time} + {.5 * self.neg_acc * self.time ** 2}')

            # Check to see if has arrived first -> reset control var
            if ceil(self.actual_x) >= self.target_location:
                #print('\n' * 10)
                self.x = self.target_location
                self.v = 0
                self.time = 0
                if self.lvl==3:
                    self.isgoing = False
                if self.lvl==6:
                    self.isgoing_x = False
                self.actual_x = deepcopy(self.x)
                self.init_x = deepcopy(self.x)


    # DIR LEFT
    elif dist_to_target <= 0:
        # False if dude is not over half way
        self.half_way = (self.actual_x <= hw)

        # IF ACC [LEFT]
        if self.half_way is False:
            self.actual_x = self.init_x + .5 * self.neg_acc * (self.time ** 2)
            position_update(self)
            # Check if acc is finished -> reset for deceleration
            if self.actual_x <= hw:
                self.v = self.neg_acc * self.time
                self.time = 0
                self.temp = deepcopy(self.actual_x)

        # IF DECELERATING [LEFT]
        if self.half_way is True:
            # Move
            self.actual_x = self.temp + self.v * self.time + (.5 * self.acc * (self.time ** 2))
            position_update(self)
            # print(
            #     f'EQ: {self.actual_x} = {self.temp} + {self.v}*{self.time} + (.5) * {self.neg_acc} * {self.time ** 2}')
            # print(
            #     f'EQ: {self.actual_x} = {self.temp} + {self.v * self.time} + {.5 * self.neg_acc * self.time ** 2}')

            # Check to see if has arrived first -> reset control var
            if ceil(self.actual_x) - 1 <= self.target_location:
                #print('\n' * 10)
                self.x = deepcopy(self.target_location)
                self.v = 0
                self.time = 0
                if self.lvl == 3:
                    self.isgoing = False
                if self.lvl == 6:
                    self.isgoing_x = False
                self.actual_x = deepcopy(self.x)
                self.init_x = deepcopy(self.x)

    else:
        if self.lvl == 3:
            self.isgoing = False
        if self.lvl == 6:
            self.isgoing_x = False
        # print('target reach error')

# L6

def randomize_target_lvl6(self):
    #dy = 0
    # dy < 50:
    self.target_location_y = randint(96, 400)
     #   dy = (self.target_location_y - self.init_y) / 2

    #dx = 0
    #while dx < 20:
    self.target_location = randint(32*3, WIDTH - 32*3)
        #dx = (self.target_location - self.init_x)

    # Reset control checks for movement
    self.isshooting = False
    self.isgoing_y = True
    self.isgoing_x = True

def position_update_y(self):
    self.y = round(self.actual_y)
    
def acc_method_y(self):

    # Time check
    self.time_y += 1
    dist_to_target = self.target_location_y - self.actual_y
    hw = ((self.target_location_y - self.init_y)/2) + self.init_y

    # if self.time_y == 1:
    #     print(f'\n\nINIT Y - TARGETY {self.target_location_y} | init y: {self.init_y} \ncurrent y: {self.actual_y}, {self.y} \n'
    # f'dist to target y: {dist_to_target} | hw y: {hw} \n'
    # f'half way_y: {self.half_way_y} | directionality_y: {dist_to_target > 0} | velocity y {self.v_y} \n'
    # f'time y: {self.time_y}  |  acc y: {self.acc_y} | temp y: {self.temp_y} is going y: {self.isgoing_y}\n'
    # f'hashes: {hash(self.actual_y)} {hash(self.temp_y)} {hash(self.y)} {self.target_location_y}')

    # Directionality UP
    if dist_to_target > 0:
        # False if dude is not over half way
        self.half_way_y = (self.actual_y >= hw)

        # IF ACC [UP]
        if self.half_way_y is False:
            self.actual_y = self.init_y + (.5 * self.acc_y * (self.time_y**2))
            position_update_y(self)
            # Check if acc is finished -> reset
            if self.actual_y >= hw:
                self.v_y = self.acc_y * self.time_y
                self.time_y = 0
                self.temp_y = deepcopy(self.actual_y)
                # Check to see if has arrived first
                if ceil(self.actual_y) >= self.target_location_y:
                #    print('\n' * 10)
                    self.y = self.target_location_y
                    self.v_y = 0
                    self.time_y = 0
                    self.isgoing_y = False
                    self.actual_y = deepcopy(self.y)
                    self.init_y = deepcopy(self.y)

        # IF DECELERATING [RIGHT]
        elif self.half_way_y is True:

            # Move
            self.actual_y = self.temp_y + self.v_y*self.time_y + (.5 * self.neg_acc_y * (self.time_y**2))
            position_update_y(self)
            # print(f'EQ: {self.actual_x} = {self.temp} + {self.v}*{self.time} + (.5) * {self.neg_acc} * {self.time**2}')
            # print(f'EQ: {self.actual_y} = {self.temp_y} + {self.v_y*self.time_y} + {.5 * self.neg_acc_y * self.time_y**2}')

            # Check to see if has arrived first
            if ceil(self.actual_y) >= self.target_location_y:
                #print('\n'*10)
                self.y = self.target_location_y
                self.v_y = 0
                self.time_y = 0
                self.isgoing_y = False
                self.actual_y = deepcopy(self.y)
                self.init_y = deepcopy(self.y)

        # print(
        #     f'\nTARGETY {self.target_location_y} | init y: {self.init_y} \ncurrent y: {self.actual_y}, {self.y} \n'
        #     f'dist to target y: {dist_to_target} | hw y: {hw} \n'
        #     f'half way_y: {self.half_way_y} | directionality_y: {dist_to_target > 0} | velocity y {self.v_y} \n'
        #     f'time y: {self.time_y}  |  acc y: {self.acc_y} | temp y: {self.temp_y} is going y: {self.isgoing_y}\n'
        #     f'hashes: {hash(self.actual_y)} {hash(self.temp_y)} {hash(self.y)} {self.target_location_y}')

    # DIR DOWN
    elif dist_to_target <= 0:
        # False if dude is not over half way
        self.half_way_y = (self.actual_y <= hw)

        # IF ACC [DOWN]
        if self.half_way_y is False:
            self.actual_y = self.init_y + .5 * self.neg_acc_y * (self.time_y ** 2)
            position_update_y(self)
            # Check if acc is finished -> reset
            if self.actual_y <= hw:
                self.v_y = self.neg_acc_y * self.time_y
                self.time_y = 0
                self.temp_y = deepcopy(self.actual_y)
                if ceil(self.actual_y) - 1 <= self.target_location_y:
                    #print('\n' * 10)
                    self.y = deepcopy(self.target_location_y)
                    self.v_y = 0
                    self.time_y = 0
                    self.isgoing_y = False
                    self.actual_y = deepcopy(self.y)
                    self.init_y = deepcopy(self.y)

        # IF DECELERATING [DOWN]
        if self.half_way_y is True:
        # Move
            self.actual_y = self.temp_y + self.v_y * self.time_y + (.5 * self.acc_y * (self.time_y**2))
            position_update_y(self)
            # print(
            #     f'EQ: {self.actual_x} = {self.temp} + {self.v}*{self.time} + (.5) * {self.neg_acc} * {self.time ** 2}')
            # print(
            #     f'EQ: {self.actual_y} = {self.temp_y} + {self.v_y * self.time_y} + {.5 * self.acc_y * self.time_y ** 2}')

            # Check to see if has arrived first
            if ceil(self.actual_y) - 1 <= self.target_location_y:
                # print('\n'*10)
                self.y = deepcopy(self.target_location_y)
                self.v_y = 0
                self.time_y = 0
                self.isgoing_y = False
                self.actual_y = deepcopy(self.y)
                self.init_y = deepcopy(self.y)

        # print(f'\nTARGETY {self.target_location_y} | init y: {self.init_y} \ncurrent y: {self.actual_y}, {self.y} \n'
        # f'dist to target y: {dist_to_target} | hw y: {hw} \n'
        # f'half way_y: {self.half_way_y} | directionality_y: {dist_to_target > 0} | velocity y {self.v_y} \n'
        # f'time y: {self.time_y}  |  acc y: {self.acc_y} | temp y: {self.temp_y} is going y: {self.isgoing_y}\n'
        # f'hashes: {hash(self.actual_y)} {hash(self.temp_y)} {hash(self.y)} {self.target_location_y}')

    else:
        self.isgoing_y = False
        #print('target reach error Y')

# Threaded Shooting
def shootlvl6(self, player):

    # Shooting thread fx for l3
    if self.lvl == 6:

        # Activate control parameters
        self.isshooting = True

        # Shoot then rest then shoot for random range
        for i in range(randint(1,5)):
            aimed_ene_clip.append(main.Aimed_Enemy_bullet(self.x+8, self.y+32, self, player))
            if main.stop_threads == True:
                return None
            # print(f'\n OG: ({self.x}x, {self.y}y)')
            # print(ene_clip)
            sleep(.5)

        # When done shooting go to a new location
        randomize_target_lvl6(self)

        return None
# ------------------------------------------------------------------------------------------------------------
# ENEMY HANDLING (applies above movement given list of enemies)


# Movement & Handling combined for l1
def lvl1_handle(l1_enemy):
    if l1_enemy.health>0:
        if l1_enemy.direction is True:
            l1_enemy.x += l1_enemy.spd
            if l1_enemy.x > 950:
                l1_enemy.direction = False
                l1_enemy.y += 50
        elif l1_enemy.direction is False:
            l1_enemy.x -= l1_enemy.spd
            if l1_enemy.x < 50:
                l1_enemy.direction = True
                l1_enemy.y += 50

def lvl2_handle(player, l2_enemy):
    if l2_enemy.health > 0:
        home_in(l2_enemy, player)

# Meta-control handling and Spawn for l3
def lvl3_handle(l3_enemy):
    # FLOW CONTROL
    # IF ELIF ELIF
    if l3_enemy.health>0:
        # Going
        if l3_enemy.isgoing == True:
            acc_method(l3_enemy)

    # --------
    # l3 SPAWN

    # ---------
        # Spawning
        elif l3_enemy.y < 50:

            # Bring them down slowly
            l3_enemy.y  += 1

            # If at target position (if finished spawning)
            # initiate their movement
            if l3_enemy.y >= 50:
                l3_enemy.y = 50
                #randomize_target_location(l3_enemy)
    # --------

        # Neither going, nor spawning, nor shooting -> Make them shoot
        # (thereby completing l3 flow cycle)
        elif l3_enemy.isshooting == False:
            t = Thread(target=shootlvl3, args=(l3_enemy, ))
            t.start()

def lvl5_handle(l5_enemy, player):
    if l5_enemy.health > 0:
        if l5_enemy.direction is True:
            l5_enemy.x += l5_enemy.spd
            if l5_enemy.x > 950:
                l5_enemy.direction = False
                if l5_enemy.y+100 < player.y:
                    l5_enemy.y += 100
                else:
                    l5_enemy.y = player.y - 32

        elif l5_enemy.direction is False:
            l5_enemy.x -= l5_enemy.spd
            if l5_enemy.x < 50:
                l5_enemy.direction = True
                if l5_enemy.y + 100 < player.y:
                    l5_enemy.y += 100
                else:
                    l5_enemy.y = player.y - 32

def lvl6_handle(player, l6_enemy):
    # FLOW CONTROL
    # IF ELIF ELIF
    if l6_enemy.health > 0:
        # x and y
        moving = (l6_enemy.isgoing_x or l6_enemy.isgoing_y)

        # Going
        if moving:
            if l6_enemy.isgoing_x == True:
                acc_method(l6_enemy)
            if l6_enemy.isgoing_y == True:
                acc_method_y(l6_enemy)
    # --------
    # l3 SPAWN

    # ---------
        # Spawning
        elif l6_enemy.isspawning == True:

            # Bring them down slowly
            l6_enemy.y  += 1

            # If at target position (if finished spawning)
            # initiate their movement
            if l6_enemy.y >= 96:
                l6_enemy.isspawning = False
                l6_enemy.init_y = l6_enemy.y
                l6_enemy.actual_y = l6_enemy.y
    # --------

        # Neither going, nor spawning, nor shooting -> Make them shoot
        # (thereby completing l3 flow cycle)
        elif l6_enemy.isshooting == False:
            t = Thread(target=shootlvl6, args=(l6_enemy, player))
            t.start()

# ------------------------------------------------------------------------------------------------------------

# MISCELLANEOUS

# Exp thread
def explosion(enemy, gif_list):
    exp_sfx.play()
    for image in gif_list:
        enemy.img = image
        if main.stop_threads == True:
            break
        sleep(.1)
    enemy.kill()
    return None

def health_img_transfer(enemy):

    if enemy.health == 20:
        return pygame.image.load('assets/007-cat-2.png')
    elif enemy.health == 15:
        return pygame.image.load('assets/004-cat.png')
    elif enemy.health == 10:
        return pygame.image.load('assets/002-monster.png')
    elif enemy.health == 5:
        return pygame.image.load('assets/001-cyclops-1.png')
    else:
        return pygame.image.load('assets/001-cyclops-1.png')

