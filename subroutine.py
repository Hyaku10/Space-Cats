import pygame
from time import sleep

pygame.mixer.init()
exp_sfx = pygame.mixer.Sound('assets/Explosion/9-bit.mp3')
exp_sfx.set_volume(.05)


def explosion(enemy):
    gif_list = [pygame.image.load('assets/Explosion/frame_0_delay-0.png'),
                pygame.image.load('assets/Explosion/frame_1_delay-0.png'),
                pygame.image.load('assets/Explosion/frame_2_delay-0.png'),
                pygame.image.load('assets/Explosion/frame_3_delay-0.png'),
                pygame.image.load('assets/Explosion/frame_4_delay-0.png'),
                pygame.image.load('assets/Explosion/frame_5_delay-0.png'),
                pygame.image.load('assets/Explosion/frame_6_delay-0.png')]


    exp_sfx.play()

    for image in gif_list:
        enemy.img = image
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


