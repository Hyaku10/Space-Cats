import pygame
import main
from time import sleep
from threading import Thread
from math import ceil
from random import randint
from copy import deepcopy
global ene_clip
ene_clip = []
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
        hw = 0
        while hw < 50:
            self.target_location = randint(0, WIDTH - 1)
            hw = ((self.target_location - self.init_x) / 2) + self.init_x

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

    if self.lvl == 3:
        # Time check
        self.time += 1
        dist_to_target = self.target_location - self.actual_x
        hw = ((self.target_location - self.init_x) / 2) + self.init_x
       # if self.time == 1:
            # print(
            #     f'\n\nINIT - TARGET {self.target_location} | init x: {self.init_x} \ncurrent x: {self.actual_x}, {self.hb.x} \n'
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
                    self.isgoing = False
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
                    self.isgoing = False
                    self.actual_x = deepcopy(self.x)
                    self.init_x = deepcopy(self.x)

        else:
            self.isgoing = False
            # print('target reach error')


# ------------------------------------------------------------------------------------------------------------
# ENEMY HANDLING (applies above movement given list of enemies)


# Movement & Handling combined for l1
def lvl1_handle(lvl1list):
    for enemy in lvl1list:
        if enemy.health>0:
            if enemy.direction is True:
                enemy.x += enemy.spd
                if enemy.x > 950:
                    enemy.direction = False
                    enemy.y += 50
            elif enemy.direction is False:
                enemy.x -= enemy.spd
                if enemy.x < 50:
                    enemy.direction = True
                    enemy.y += 50


def lvl2_handle(player, lvl2list):
    for enemy in lvl2list:
        if enemy.health > 0:
            home_in(enemy, player)

# Meta-control handling and Spawn for l3
def lvl3_handle(l3):
    for l3_enemy in l3:
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

