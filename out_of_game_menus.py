import main
import pygame
from sys import exit
pygame.mixer.init()

class shootable_buttons():
    def __init__(self, name, x, y, img):
        self.name = name
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # functionality
    def button_call_fx(self):
        if self.name == 'play':
            return False
        if self.name == 'exit':
            return exit(0)
        if self.name == 'title':
            return True

    # DRAW
    def draw(self):
        main.WIN.blit(self.img, (self.x, self.y))


# BUTTONS
start_button = shootable_buttons("play", (200 - 128 / 2), (300 - 128 / 2),
                                 pygame.image.load('assets/menu_assets/002-play.png'))
exit_button = shootable_buttons("exit", (800 - 128 / 2), (300 - 128 / 2),
                                pygame.image.load('assets/menu_assets/001-exit.png'))
title = shootable_buttons("title", (500 - 400 / 2), (300 - 540 / 2),
                                pygame.image.load('assets/menu_assets/space_cats_title3.png'))

shootable_buttons_list = [start_button, exit_button, title]

# BACKGROUND AND MUSIC
pygame.mixer.music.set_volume(.2)
bg=pygame.image.load('assets/menu_assets/menu_background_v1.5.png')
pygame.mixer.music.load('assets/menu_assets/menu_bgm.mp3')
pygame.mixer.music.play(-1)

def menu_bullet(clip, b_list):
    for bullet in clip:
        bullet.draw()
        bullet.y -= main.bulspd
        if bullet.y < 1 and bullet in clip:
            clip.remove(bullet)

        for button in b_list:
            if bullet.collision(button) and button.name != 'title':
                clip.remove(bullet)
                game_state = button.button_call_fx()
                return game_state


def start_menu():
    # DECLARATIVE (that tomer gave me)
    run_start_menu = True
    plaX, plaY = main.WIDTH / 2 - 32 / 2, 517
    player = main.Player(main.pla_x, main.pla_y)
    clip = []
    fpsclock = pygame.time.Clock()
    FPS = 60

    # MENU LOOP
    while run_start_menu == True:
        fpsclock.tick(FPS)

        # EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(clip) < main.bulmax:
                    bullet = main.Bullet(player.x + 8, player.y)
                    clip.append(bullet)

        key_pre = pygame.key.get_pressed()
        if key_pre[pygame.K_RIGHT] and player.x < 1000 - 32:
            plaX += main.plaspd
        if key_pre[pygame.K_LEFT] and player.x > 0:
            plaX -= main.plaspd
        player.x = round(plaX)

        # GAME STATE CHECK

        # Draw
        main.draw_window(bg)
        [img.draw() for img in shootable_buttons_list]
        player.draw()

        # Handle bullets and Check if buttons hit
        run_start_menu = menu_bullet(clip, shootable_buttons_list)
        if run_start_menu is None:
            run_start_menu = True

        pygame.display.update()


def escape_menu():
    pass


def game_over():
    pass

