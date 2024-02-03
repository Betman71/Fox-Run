import os
import sqlite3
import sys

import pygame
from pygame.locals import *

pygame.init()
blocks = pygame.sprite.Group()

f1 = True
fox_img1 = ['data/fox1l.png', 'data/fox2l.png', 'data/fox3l.png', 'data/fox4l.png']
fox_img2 = ['data/fox1.png', 'data/foxs2.png', 'data/foxs3.png', 'data/foxs4.png']
co = 0

coin = 0
level_num = 1
buttons1 = pygame.sprite.Group()


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = pygame.image.load('data/star1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = pygame.image.load('data/block.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Hero(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image_stand = 'data/foxs2.png'
        self.anim_hero_right = 'data/ghostright1.png'
        self.anim_hero_left = 'data/ghostleft1.png'
        self.image = pygame.image.load(self.image_stand)
        self.rect = self.image.get_rect()
        self.left = True
        self.right = True
        self.down = True
        self.can_dash = True
        self.count = 0
        self.can_down = True

    def intersect_right(self, block) -> bool:
        for bloc in block:
            if self.rect.right >= bloc.rect.left > self.rect.left \
                    and (bloc.rect.bottom >= self.rect.centery - 10 >= bloc.rect.top
                         or bloc.rect.bottom >= self.rect.centery + 10 >= bloc.rect.top):
                return True
        return False

    def intersect_left(self, block):
        for bloc in block:
            if self.rect.left <= bloc.rect.right < self.rect.right \
                    and (bloc.rect.bottom >= self.rect.centery - 10 >= bloc.rect.top
                         or bloc.rect.bottom >= self.rect.centery + 10 >= bloc.rect.top):
                return True
        return False

    def update(self, button):
        global hero
        global blocks
        delta = 2
        if button == 'right' and not self.intersect_right(blocks):
            if self.rect.left + delta > 600:
                pass
            else:
                self.rect.left += delta
            self.animation_right()
        elif button == 'left' and not self.intersect_left(blocks):
            if self.rect.left - delta < 5:
                pass
            else:
                self.rect.left -= delta
            self.animation_left()

    def animation_stand(self):
        self.image = pygame.image.load(self.image_stand)

    def animation_left(self):
        global co
        if co == 4:
            co = 0
        self.image = pygame.image.load(fox_img1[co])
        co += 1

    def animation_right(self):
        global co
        if co == 4:
            co = 0
        self.image = pygame.image.load(fox_img2[co])
        co += 1

    def collision_down(self, sprite):
        if self.rect.colliderect(sprite.rect) and self.rect.y - 1 - 25 <= sprite.rect.y:
            return True
        else:
            return False

    def dash(self, direction):
        global hero
        if self.can_dash:
            if direction == 'right':
                self.rect.left += 150
                self.count = 0
                self.can_dash = False
                self.left = True
            if direction == 'left':
                self.rect.left -= 150
                self.count = 0
                self.can_dash = False
                self.right = True

    def gravity(self):
        global blocks
        for i in blocks:
            if self.collision_down(i):
                self.can_down = False
                break
            else:
                self.can_down = True
                pass
        if self.can_down:
            self.rect.top += 1.4
            self.animation_stand()
        else:
            self.rect.top -= 0
            self.animation_stand()


hero = Hero()
coins = pygame.sprite.Group()


class CreateLevel:
    def __init__(self, level):
        global blocks
        global hero
        global coins
        global buttons1
        global load_xy

        buttons1 = pygame.sprite.Group()
        f = open('data/' + level, mode="r")
        lines = f.readlines()
        lines1 = []
        for i in lines:
            lines1.append(i.rstrip())
        razmer = 25
        x = 0
        y = 0
        for i in lines1:
            for ii in i:
                if ii == '*':
                    x += razmer
                elif ii == '#':
                    c = Block(x, y)
                    blocks.add(c)
                    x += razmer
                elif ii == '@':
                    if load_xy:
                        hero.rect.x = spis[0]
                        hero.rect.y = spis[1]
                    else:
                        hero.rect.x = x
                        hero.rect.y = y
                    x += razmer
                    pass
                elif ii == '0':
                    c = Star(x, y)
                    coins.add(c)
                    x += razmer
            y += 25
            x = 0


can_load = False


def load(direction):
    global hero
    global level_num
    global coin
    global dop_speed
    global dop_time_dash
    global can_load
    global load_xy
    global spis
    if direction == 'load':
        f = open('data/save.txt', mode="r")
        lines = f.readlines()
        line = lines[0].split(', ')
        for j in line:
            spis[line.index(j)] = int(j)
        can_load = True
        load_xy = True


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)


keys = {K_LEFT: False, K_RIGHT: False, K_LSHIFT: False, K_e: False}

load_xy = False

pygame.init()
screen_size = (1300, 800)
screen = pygame.display.set_mode(screen_size)
FPS = 60

clock = pygame.time.Clock()
pygame.display.set_caption("Fox Run")

pygame.mixer.music.load("data/gamemusic.mp3")
pygame.mixer.music.set_volume(0.2)
button_sound = pygame.mixer.Sound("data/buttonsound.mp3")

icon = pygame.image.load('data/icon.png')
pygame.display.set_icon(icon)


def breakbut():
    main()


def leavebutton():
    pygame.quit()
    quit()


def draw_startmenu():
    menu_background = pygame.transform.scale(load_imag('menushka.jpg'), screen_size)
    pygame.mixer.music.play(-1)
    show = True

    start_button = Button(180, 65)
    leave_button = Button(180, 65)

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        start_button.draw(100, 315, "Start", breakbut, 50)
        leave_button.draw(100, 405, "Leave", leavebutton, 50)

        pygame.display.update()
        clock.tick(FPS)


def load_imag(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def start_screen():
    fon = pygame.transform.scale(load_imag('fox.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif (event.type == pygame.KEYDOWN or
                  event.type == pygame.MOUSEBUTTONDOWN) and pygame.mouse.get_pos()[0] > 280:
                draw_startmenu()
        pygame.display.flip()
        clock.tick(FPS)


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color1 = (218, 193, 144)
        self.color2 = (192, 128, 0)

    def draw(self, x, y, text, action=None, font=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.color1, (x, y, self.width, self.height))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(350)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(screen, self.color2, (x, y, self.width, self.height))

        print_text(text, x + 10, y + 10, font_type='data/MonaspaceXenon-Bold.otf', font_size=font)


def run_game():
    start_screen()
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(FPS)


def print_pause(message, x, y, font_color=(0, 0, 0), font_type='data/Font_Pause.ttf', font_size=45):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def print_text(message, x, y, font_color=(0, 0, 0), font_type='data/Font_Pause.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def pause():
    paused = True

    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_pause('Пауза. Нажмите Enter.', 370, 250)

        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(20)

    pygame.mixer.music.unpause()


spis = [hero.rect.x, hero.rect.y, level_num, coin]


def main():
    global coins
    global level_num
    global can_load
    global blocks
    global coin
    global hero
    pygame.display.set_caption("Fox Run")
    size = width, height = 625, 600
    hero = Hero()
    hero_group = pygame.sprite.Group()
    hero_group.add(hero)
    coins = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    con = sqlite3.connect('data/game_db.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT level FROM levels 
                            WHERE id = {level_num}""").fetchall()
    level = CreateLevel(result[0][0])
    all_sprites = pygame.sprite.Group()
    final = False
    running = True
    all_sprites.add(hero)
    clock = pygame.time.Clock()
    flag = False
    can_up = False
    colvo = 0
    coldown = False
    gmo_group = pygame.sprite.Group()
    while running:
        if can_load:
            level_num = spis[2]
            blocks = pygame.sprite.Group()
            coins = pygame.sprite.Group()

            result = cur.execute(f"""SELECT level FROM levels 
                                        WHERE id = {level_num}""").fetchall()
            level = CreateLevel(result[0][0])
            can_load = False
            continue
        f1 = pygame.font.Font(None, 25)
        t = f1.render(f'STARS: {coin}', True,
                      (0, 0, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause()
                if event.key in keys:
                    keys[event.key] = True
                if event.key == K_UP:
                    if not hero.can_down and not coldown:
                        can_up = True
                        colvo = 0
                        coldown = True
            elif event.type == KEYUP:
                if event.key in keys:
                    keys[event.key] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 325 <= pos[0] <= 350 and 0 <= pos[1] <= 25:
                    print(1)
                elif 225 <= pos[0] <= 250 and 0 <= pos[1] <= 25:
                    if flag:
                        flag = False
                    else:
                        flag = True

        if final:
            screen.fill(pygame.color.Color('black'))
            fox = pygame.sprite.Sprite()
            ghost_group = pygame.sprite.Group()
            fox.image = pygame.image.load('data/final.png')
            fox.rect = fox.image.get_rect()
            fox.rect.x = 0
            fox.rect.y = 0
            ghost_group.add(fox)
            ghost_group.draw(screen)
            pygame.display.flip()
            continue

        if flag:
            continue
        if coin == 3:

            level_num += 1
            coin = 0
            if level_num > 3:
                final = True
            else:
                result = cur.execute(f"""SELECT level FROM levels 
                                    WHERE id = {level_num}""").fetchall()
                coins = pygame.sprite.Group()
                blocks = pygame.sprite.Group()
                level = CreateLevel(result[0][0])
        if can_up and colvo < 10:
            colvo += 1
            hero.rect.top -= 5
            if colvo == 10:
                coldown = False
        else:
            hero.gravity()
            can_up = False
        for i in coins:
            if hero.rect.colliderect(i):
                i.kill()
                coin += 1
        if keys[K_LEFT] and keys[K_LSHIFT]:
            hero.dash('left')
        elif keys[K_RIGHT] and keys[K_LSHIFT]:
            hero.dash('right')
        if keys[K_LEFT]:
            hero.update('left')
        elif keys[K_RIGHT]:
            hero.update('right')
        else:
            pass
        if hero.count == 200:
            hero.can_dash = True
        fon = pygame.transform.scale(pygame.image.load('data/map1.png'), size)
        screen.blit(fon, (0, 0))
        blocks.draw(screen)
        all_sprites.draw(screen)
        buttons1.draw(screen)
        coins.draw(screen)
        clock.tick(60)
        screen.blit(t, (10, 50))
        pygame.display.flip()
    pygame.quit()


run_game()
