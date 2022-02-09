# SINGLE DIMENSIONAL ACCELERATOR AND DECELERATOR

import pygame
from random import randint
from copy import deepcopy
from math import ceil
fps = 30
w = 1280
h = 720
clock = pygame.time.Clock()
screen = pygame.display.set_mode((w, h))
screen.fill((0,0,0))


class my_dude:
    def __init__(self, acc=10/9):
        # Creating object and position
        self.actual_x = w/2
        self.init_x = w/2
        self.hb = pygame.Rect(w/2, 250, 64, 64)
        self.time = 0

        # Velocity & Acc
        self.v = 0
        self.acc = acc
        self.neg_acc = -1*acc
        self.temp = 0

        # Target & Halfway
        self.target_location = randint(0, w-1)
        self.half_way = True

        # Control var
        self.isgoing = True

    # Utility Methods
    def position_update(self):
        self.hb.x = round(self.actual_x)
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255, 255, 255), self.hb, 20, 20)
        pygame.display.update()

    def randomize_target(self):
        self.target_location = randint(0, w-1)
        self.half_way = False

    def wait(self):
        self.time += 1
        if self.time == 1:
            print('Transit succesful')
        if self.time > 120:
            self.time = 0
            self.isgoing = True
            print('Initiating once more')
            pygame.event.wait()
            self.randomize_target()

    # Formulas
        # v = v0 + at
        # x = x0 + vot + 1/2*a * t^2


    def acc_method(self):

        # Time check
        self.time += 1
        dist_to_target = self.target_location - self.actual_x
        hw = ((self.target_location - self.init_x)/2) + self.init_x
        if self.time == 1:
            print(
                f'\n\nINIT - TARGET {self.target_location} | init x: {self.init_x} \ncurrent x: {self.actual_x}, {self.hb.x} \n'
                f'dist to target: {dist_to_target} | hw: {hw} \n'
                f'half way: {self.half_way} | directionality: {dist_to_target > 0} | velocity {self.v} \n' 
                f'time: {self.time}  |  acc: {self.acc} | temp: {self.temp}')

        # Directionality RIGHT
        if dist_to_target > 0:
            # False if dude is not over half way
            self.half_way = (self.actual_x >= hw)

            # IF ACC [RIGHT]
            if self.half_way is False:
                self.actual_x = self.init_x + (.5 * self.acc * (self.time**2))
                # Check if acc is finished -> reset
                if self.actual_x >= hw:
                    self.v = self.acc * self.time
                    self.time = 0
                    self.temp = deepcopy(self.actual_x)

            # IF DECELERATING [RIGHT]
            elif self.half_way is True:

                # Move
                self.actual_x = self.temp + self.v*self.time + (.5 * self.neg_acc * (self.time**2))
                print(f'EQ: {self.actual_x} = {self.temp} + {self.v}*{self.time} + (.5) * {self.neg_acc} * {self.time**2}')
                print(f'EQ: {self.actual_x} = {self.temp} + {self.v*self.time} + {.5 * self.neg_acc * self.time**2}')

                # Check to see if has arrived first
                if ceil(self.actual_x) >= self.target_location:
                    print('\n'*10)
                    self.hb.x = self.target_location
                    self.v = 0
                    self.time = 0
                    self.isgoing = False
                    self.actual_x = deepcopy(self.hb.x)
                    self.init_x = deepcopy(self.hb.x)


        # DIR LEFT
        elif dist_to_target <= 0:
            # False if dude is not over half way
            self.half_way = (self.actual_x <= hw)

            # IF ACC [LEFT]
            if self.half_way is False:
                self.actual_x = self.init_x + .5 * self.neg_acc * (self.time ** 2)
                # Check if acc is finished -> reset
                if self.actual_x <= hw:
                    self.v = self.neg_acc * self.time
                    self.time = 0
                    self.temp = deepcopy(self.actual_x)

            # IF DECELERATING [LEFT]
            if self.half_way is True:
            # Move
                self.actual_x = self.temp + self.v*self.time + (.5 * self.acc * (self.time**2))
                print(
                    f'EQ: {self.actual_x} = {self.temp} + {self.v}*{self.time} + (.5) * {self.neg_acc} * {self.time ** 2}')
                print(
                    f'EQ: {self.actual_x} = {self.temp} + {self.v * self.time} + {.5 * self.neg_acc * self.time ** 2}')

                # Check to see if has arrived first
                if ceil(self.actual_x) - 1 <= self.target_location:
                    print('\n'*10)
                    self.hb.x = deepcopy(self.target_location)
                    self.v = 0
                    self.time = 0
                    self.isgoing = False
                    self.actual_x = deepcopy(self.hb.x)
                    self.init_x = deepcopy(self.hb.x)



        else:
            self.isgoing = False
            print('target reach error')

        print(f'\nTARGET {self.target_location} | init x: {self.init_x} \ncurrent x: {self.actual_x}, {self.hb.x} \n'
        f'dist to target: {dist_to_target} | hw: {hw} \n'
        f'half way: {self.half_way} | directionality: {dist_to_target > 0} | velocity {self.v} \n'
        f'time: {self.time}  |  acc: {self.acc} | temp: {self.temp} is going: {self.isgoing}\n'
        f'hashes: {hash(self.actual_x)} {hash(self.temp)} {hash(self.hb.x)} {self.target_location}')





#
dude = my_dude()
dude.position_update()
pygame.display.update()
dude.randomize_target()

run = True
while run is True:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if dude.isgoing is True:
        dude.acc_method()
        dude.position_update()
        pygame.display.flip()

    else:
        dude.wait()



class dude_but_yyyy(my_dude):
    def __init__(self, acc = 10/9, acc_y = 7/9):
        super().__init__()
        self.acc = acc

        self.actual_y = h / 2
        self.init_y = h / 2
        self.time_y = 0
        self.hb = pygame.Rect(w/2, h/2, 64, 64)

        # Velocity & Acc
        self.v_y = 0
        self.acc_y = acc_y
        self.neg_acc_y = -1 * acc_y
        self.temp_y = 0

        # Target & Halfway
        self.target_location_y = randint(0, h - 1)
        self.half_way_y = True

        # Control var
        self.isgoing_y = True

    # Utility Methods

    def position_update(self):
        self.hb.x = round(self.actual_x)
        self.hb.y = round(self.actual_y)
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), self.hb, 20, 20)
        pygame.display.update()

    def randomize_target_y(self):
        self.target_location_y = randint(0, h - 1)
        self.half_way_y = False

    def wait(self):
        self.time += 1
        if self.time == 1:
            print('Transit succesful')
        if self.time > 30:
            self.time = 0
            self.time_y = 0
            self.isgoing = True
            self.isgoing_y = True
            print('Initiating once more')
            pygame.event.wait()
            self.randomize_target()
            self.randomize_target_y()


    def acc_method_y(self):

        # Time check
        self.time_y += 1
        dist_to_target = self.target_location_y - self.actual_y
        hw = ((self.target_location_y - self.init_y)/2) + self.init_y

        if self.time_y == 1:
            print(f'\n\nINIT Y - TARGETY {self.target_location_y} | init y: {self.init_y} \ncurrent y: {self.actual_y}, {self.hb.y} \n'
        f'dist to target y: {dist_to_target} | hw y: {hw} \n'
        f'half way_y: {self.half_way_y} | directionality_y: {dist_to_target > 0} | velocity y {self.v_y} \n'
        f'time y: {self.time_y}  |  acc y: {self.acc_y} | temp y: {self.temp_y} is going y: {self.isgoing_y}\n'
        f'hashes: {hash(self.actual_y)} {hash(self.temp_y)} {hash(self.hb.y)} {self.target_location_y}')

        # Directionality UP
        if dist_to_target > 0:
            # False if dude is not over half way
            self.half_way_y = (self.actual_y >= hw)

            # IF ACC [UP]
            if self.half_way_y is False:
                self.actual_y = self.init_y + (.5 * self.acc_y * (self.time_y**2))
                # Check if acc is finished -> reset
                if self.actual_y >= hw:
                    self.v_y = self.acc_y * self.time_y
                    self.time_y = 0
                    self.temp_y = deepcopy(self.actual_y)

            # IF DECELERATING [RIGHT]
            elif self.half_way_y is True:

                # Move
                self.actual_y = self.temp_y + self.v_y*self.time_y + (.5 * self.neg_acc_y * (self.time_y**2))
                # print(f'EQ: {self.actual_x} = {self.temp} + {self.v}*{self.time} + (.5) * {self.neg_acc} * {self.time**2}')
                print(f'EQ: {self.actual_y} = {self.temp_y} + {self.v_y*self.time_y} + {.5 * self.neg_acc_y * self.time_y**2}')

                # Check to see if has arrived first
                if ceil(self.actual_y) >= self.target_location_y:
                    print('\n'*10)
                    self.hb.y = self.target_location_y
                    self.v_y = 0
                    self.time_y = 0
                    self.isgoing_y = False
                    self.actual_y = deepcopy(self.hb.y)
                    self.init_y = deepcopy(self.hb.y)

            print(
                f'\nTARGETY {self.target_location_y} | init y: {self.init_y} \ncurrent y: {self.actual_y}, {self.hb.y} \n'
                f'dist to target y: {dist_to_target} | hw y: {hw} \n'
                f'half way_y: {self.half_way_y} | directionality_y: {dist_to_target > 0} | velocity y {self.v_y} \n'
                f'time y: {self.time_y}  |  acc y: {self.acc_y} | temp y: {self.temp_y} is going y: {self.isgoing_y}\n'
                f'hashes: {hash(self.actual_y)} {hash(self.temp_y)} {hash(self.hb.y)} {self.target_location_y}')

        # DIR DOWN
        elif dist_to_target <= 0:
            # False if dude is not over half way
            self.half_way_y = (self.actual_y <= hw)

            # IF ACC [DOWN]
            if self.half_way_y is False:
                self.actual_y = self.init_y + .5 * self.neg_acc_y * (self.time_y ** 2)
                # Check if acc is finished -> reset
                if self.actual_y <= hw:
                    self.v_y = self.neg_acc_y * self.time_y
                    self.time_y = 0
                    self.temp_y = deepcopy(self.actual_y)

            # IF DECELERATING [DOWN]
            if self.half_way_y is True:
            # Move
                self.actual_y = self.temp_y + self.v_y * self.time_y + (.5 * self.acc_y * (self.time_y**2))
                # print(
                #     f'EQ: {self.actual_x} = {self.temp} + {self.v}*{self.time} + (.5) * {self.neg_acc} * {self.time ** 2}')
                print(
                    f'EQ: {self.actual_y} = {self.temp_y} + {self.v_y * self.time_y} + {.5 * self.acc_y * self.time_y ** 2}')

                # Check to see if has arrived first
                if ceil(self.actual_y) - 1 <= self.target_location_y:
                    print('\n'*10)
                    self.hb.y = deepcopy(self.target_location_y)
                    self.v_y = 0
                    self.time_y = 0
                    self.isgoing_y = False
                    self.actual_y = deepcopy(self.hb.y)
                    self.init_y = deepcopy(self.hb.y)

            print(f'\nTARGETY {self.target_location_y} | init y: {self.init_y} \ncurrent y: {self.actual_y}, {self.hb.y} \n'
            f'dist to target y: {dist_to_target} | hw y: {hw} \n'
            f'half way_y: {self.half_way_y} | directionality_y: {dist_to_target > 0} | velocity y {self.v_y} \n'
            f'time y: {self.time_y}  |  acc y: {self.acc_y} | temp y: {self.temp_y} is going y: {self.isgoing_y}\n'
            f'hashes: {hash(self.actual_y)} {hash(self.temp_y)} {hash(self.hb.y)} {self.target_location_y}')

        else:
            self.isgoing_y = False
            print('target reach error Y')





bruh = dude_but_yyyy()
bruh.position_update()
pygame.display.update()
bruh.randomize_target()

run_xy = True
while run_xy is True:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_xy = False

    if bruh.isgoing is True or bruh.isgoing_y is True:

        if bruh.isgoing is True:
            bruh.acc_method()

        if bruh.isgoing_y is True:
            bruh.acc_method_y()

        bruh.position_update()
        pygame.display.flip()

    else:
        bruh.wait()
