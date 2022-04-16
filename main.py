import pygame
import os
import json

with open('levels.txt') as levels_file:
    levels = json.load(levels_file)

with open('users.txt') as users_file:
    users = json.load(users_file)

with open('settings.txt') as settings_file:
    volume = json.load(settings_file)

WIDTH = 1280
HEIGHT = 720
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Слова из слов")
clock = pygame.time.Clock()

# настройка папки ассетов
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'foto')
bg_img = pygame.image.load(os.path.join(img_folder, 'bg.png')).convert()
accept_img = pygame.image.load(os.path.join(img_folder, 'accept.png')).convert()
erase_img = pygame.image.load(os.path.join(img_folder, 'erase.png')).convert()
logo_img = pygame.image.load(os.path.join(img_folder, 'logo.png')).convert()
back_img = pygame.image.load(os.path.join(img_folder, 'back.png')).convert()
forward_img = pygame.image.load(os.path.join(img_folder, 'forward.png')).convert()

bg_rect = bg_img.get_rect()

user = {
    'name': '',
    'progress': [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
}

level = 0
word = ''
words = []

result = ''
results = []

forward = None

class TextBlock(pygame.sprite.Sprite):
    def __init__(self, text, x, y, width, height, fz):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.height = height
        self.font_size = fz
        self.width = width
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image.fill(WHITE)
        self.border = pygame.rect.Rect(0, 0, self.width, self.height)
        self.border_color = BLACK
        pygame.draw.rect(self.image, self.border_color, self.border, 3)
        f1 = pygame.font.Font(None, self.font_size)
        text1 = f1.render(self.text, True, BLACK)
        self.image.blit(text1, ((self.width - text1.get_width()) / 2, (self.height - text1.get_height()) / 2))


class ResBlock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ''
        self.height = 50
        self.font_size = 40

    def update(self):
        self.width = 20 + len(self.text) * 20
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.top = HEIGHT - (self.height + 20)
        self.image.fill(WHITE)
        self.border = pygame.rect.Rect(0, 0, self.width, self.height)
        self.border_color = BLACK
        pygame.draw.rect(self.image, self.border_color, self.border, 3)
        f1 = pygame.font.Font(None, self.font_size)
        text1 = f1.render(self.text, True, BLACK)
        self.image.blit(text1, ((self.width - text1.get_width()) / 2, (self.height - text1.get_height()) / 2))

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, width, height, font_size):
        self.pressed = False
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.width = width
        self.height = height
        self.font_size = font_size
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        if self.pressed:
            self.image.fill(GRAY)
        else:
            self.image.fill(WHITE)

        self.border = pygame.rect.Rect(0, 0, self.width, self.height)
        self.border_color = BLACK
        pygame.draw.rect(self.image, self.border_color, self.border, 3)
        f1 = pygame.font.Font(None, self.font_size)
        text1 = f1.render(self.text, True, BLACK)
        self.image.blit(text1, ((self.width - text1.get_width()) / 2, (self.height - text1.get_height()) / 2))

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            if not self.pressed:
                global result
                result += self.text
            self.set_pressed(True)
            print(self.text)

    def set_pressed(self, pressed):
        self.pressed = pressed


class ImageButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.border = pygame.rect.Rect(0, 0, self.width, self.height)
        self.border_color = BLACK
        pygame.draw.rect(self.image, self.border_color, self.border, 3)


class AcceptButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 60
        self.image = accept_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH - (self.width + 20), HEIGHT - (self.height + 20))
        self.border = pygame.rect.Rect(0, 0, self.width, self.height)
        self.border_color = BLACK
        pygame.draw.rect(self.image, self.border_color, self.border, 3)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            global result
            global level
            global words
            global forward

            print(result)
            print(words)
            if result in words and len(result) < 40:
                print('added')
                results.append(result)
                words.remove(result)

                if len(results) == 40 or len(words) == 0:
                    forward = ImageButton(1137, 40, 103, 55, forward_img)
                    all_sprites.add(forward)

                for i in range(len(users)):
                    if users[i]['name'] == user['name']:
                        users[i]['progress'][level - 1].append(result)

                with open('users.txt', 'w') as users_file:
                    json.dump(users, users_file)

                result = ''
                for button in buttons:
                    button.set_pressed(False)


class EraseButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 60
        self.image = erase_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH - (self.width + 100), HEIGHT - (self.height + 20))
        self.border = pygame.rect.Rect(0, 0, self.width, self.height)
        self.border_color = BLACK
        pygame.draw.rect(self.image, self.border_color, self.border, 3)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            global result
            result = ''
            for button in buttons:
                button.set_pressed(False)


def new_tb(text, x, y, width, height, fz):
    tb = TextBlock(text, x, y, width, height, fz)
    all_sprites.add(tb)


def form_results():
    global results
    x = 50
    y = 150
    for i in range(len(results)):
        new_tb(results[i], x, y, 145, 40, 24)
        y += 55
        if (i + 1) % 5 == 0:
            y = 150
            x += 150


def print_text(surface, x, y, text, fz):
    font = pygame.font.Font(None, fz)
    text_img = font.render(text, True, BLACK)
    text_rect = text_img.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_img, text_rect)


def show_set_word():
    global word

    screen.blit(bg_img, bg_rect)

    set_word_sprites = pygame.sprite.Group()

    print_text(screen, 330, 280, 'ВВЕДИТЕ ИСХОДНОЕ СЛОВО:', 56)

    form = TextBlock(word, 360, 330, 560, 50, 36)
    accept = ImageButton(950, 325, 60, 60, accept_img)
    back = ImageButton(40, 40, 103, 55, back_img)

    set_word_sprites.add(back)
    set_word_sprites.add(form)
    set_word_sprites.add(accept)

    set_word_sprites.draw(screen)

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_pos = pygame.mouse.get_pos()
                    if accept.rect.collidepoint(mouse_pos):
                        waiting = False

                    if back.rect.collidepoint(mouse_pos):
                        waiting = False

            if event.type == pygame.KEYDOWN:
                print(word)
                if event.key == pygame.K_BACKSPACE:
                    word = word[:-1]
                elif len(word) < 13:
                    word += event.unicode

                form = TextBlock(word, 360, 330, 560, 50, 36)
                set_word_sprites.add(form)
                set_word_sprites.draw(screen)

                pygame.display.flip()


def show_profile():
    global user
    username = ''

    screen.blit(bg_img, bg_rect)

    logo_img.set_colorkey((255, 0, 0))
    screen.blit(logo_img, (145, 60))

    profile_sprites = pygame.sprite.Group()

    print_text(screen, 330, 280, 'ВВЕДИТЕ ИМЯ ПОЛЬЗОВАТЕЛЯ:', 56)

    form = TextBlock(username, 360, 330, 560, 50, 36)
    accept = ImageButton(950, 325, 60, 60, accept_img)

    profile_sprites.add(form)
    profile_sprites.add(accept)

    profile_sprites.draw(screen)

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_pos = pygame.mouse.get_pos()
                    if accept.rect.collidepoint(mouse_pos) and len(username) > 0:
                        with open('users.txt') as users_file:
                            users = json.load(users_file)

                        found = False
                        for i in range(len(users)):
                            if users[i]['name'] == username:
                                found = True
                                user = {
                                    'name': users[i]['name'],
                                    'progress': users[i]['progress']

                                }

                        if not found:
                            user = {
                                'name': username,
                                'progress': [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

                            }
                            users.append(user)
                            with open('users.txt', 'w') as users_file:
                                json.dump(users, users_file)

                        waiting = False

            if event.type == pygame.KEYDOWN:
                print(username)
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 32:
                    username += event.unicode

                form = TextBlock(username, 360, 330, 560, 50, 36)
                profile_sprites.add(form)
                profile_sprites.draw(screen)

                pygame.display.flip()


def show_game():
    global word
    global level
    global words
    global results

    global forward

    resblock = ResBlock()
    erase_btn = EraseButton()
    accept_btn = AcceptButton()
    all_sprites.add(resblock)
    all_sprites.add(erase_btn)
    all_sprites.add(accept_btn)

    back = ImageButton(40, 40, 103, 55, back_img)
    all_sprites.add(back)

    if len(results) == 40 or len(words) == 0:
        forward = ImageButton(1137, 40, 103, 55, forward_img)
        all_sprites.add(forward)

    word = word.upper()
    letter_width = 80
    letter_spacing = 20
    letter_font_size = 52

    x = (WIDTH - len(word) * letter_width - (len(word) - 1) * letter_spacing) / 2
    for letter in word:
        button = Button(x, 504, letter, letter_width, letter_width, letter_font_size)
        all_sprites.add(button)
        buttons.add(button)
        x += letter_width + letter_spacing

    waiting = True
    while waiting:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_pos = pygame.mouse.get_pos()
                    if back.rect.collidepoint(mouse_pos):
                        waiting = False

                    if forward != None and forward.rect.collidepoint(mouse_pos):
                        forward = None

                        level += 1
                        word = levels[level - 1]['word']
                        words = levels[level - 1]['words']

                        results = user['progress'][level - 1]

                        print(results)

                        for i in range(len(results)):
                            if results[i] in words:
                                words.remove(results[i])

                        all_sprites.empty()
                        buttons.empty()

                        all_sprites.add(resblock)
                        all_sprites.add(erase_btn)
                        all_sprites.add(accept_btn)
                        all_sprites.add(back)

                        if len(results) == 40 or len(words) == 0:
                            forward = ImageButton(1137, 40, 103, 55, forward_img)
                            all_sprites.add(forward)

                        word = word.upper()
                        letter_width = 80
                        letter_spacing = 20
                        letter_font_size = 52

                        x = (WIDTH - len(word) * letter_width - (len(word) - 1) * letter_spacing) / 2
                        for letter in word:
                            button = Button(x, 504, letter, letter_width, letter_width, letter_font_size)
                            all_sprites.add(button)
                            buttons.add(button)
                            x += letter_width + letter_spacing


        # Обновление
        resblock.set_text(result)
        all_sprites.update()
        form_results()

        # Рендеринг
        screen.blit(bg_img, bg_rect)
        all_sprites.draw(screen)
        print_text(screen, 490, 50, 'УРОВЕНЬ ' + str(level), 72)
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

    all_sprites.empty()
    buttons.empty()


def show_levels():
    global words
    global word
    global level
    global results

    screen.blit(bg_img, bg_rect)

    blocks = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    back = ImageButton(40, 40, 103, 55, back_img)
    buttons.add(back)

    x = 295
    y = 165

    last_level = 1
    for i in range(1, len(user['progress'])):
        if user['progress'][i] == []:
            last_level = i
            break

    for i in range(last_level):
        tb = TextBlock(str(i + 1), x, y, 90, 90, 56)
        blocks.add(tb)
        x += 150

        if (i + 1) % 5 == 0:
            x = 295
            y += 150

    buttons.draw(screen)
    blocks.draw(screen)

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_pos = pygame.mouse.get_pos()
                    for block in blocks:
                        if block.rect.collidepoint(mouse_pos):
                            level = int(block.text)
                            word = levels[level - 1]['word']
                            words = levels[level - 1]['words']

                            results = user['progress'][level - 1]

                            print(results)

                            for i in range(len(results)):
                                if results[i] in words:
                                    words.remove(results[i])

                            show_game()

                            blocks.empty()

                            last_level = 1
                            for i in range(1, len(user['progress'])):
                                if user['progress'][i] == []:
                                    last_level = i
                                    break

                            x = 295
                            y = 165

                            for i in range(last_level):
                                tb = TextBlock(str(i + 1), x, y, 90, 90, 56)
                                blocks.add(tb)
                                x += 150

                                if (i + 1) % 5 == 0:
                                    x = 295
                                    y += 150

                            screen.blit(bg_img, bg_rect)
                            buttons.draw(screen)
                            blocks.draw(screen)

                            pygame.display.flip()

                    if back.rect.collidepoint(mouse_pos):
                        waiting = False


def show_play():
    options = ['ПРОДОЛЖИТЬ', 'ЗАДАТЬ СЛОВО']
    blocks = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    screen.blit(bg_img, bg_rect)

    for i in range(len(options)):
        tb = TextBlock(options[i], 455, 240 + (i * 150), 370, 90, 56)
        blocks.add(tb)

    back = ImageButton(40, 40, 103, 55, back_img)
    buttons.add(back)

    buttons.draw(screen)
    blocks.draw(screen)

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_pos = pygame.mouse.get_pos()
                    for block in blocks:
                        if block.rect.collidepoint(mouse_pos):
                            match block.text:
                                case 'ПРОДОЛЖИТЬ':
                                    show_levels()

                                    screen.blit(bg_img, bg_rect)
                                    buttons.draw(screen)
                                    blocks.draw(screen)
                                    pygame.display.flip()

                                case 'ЗАДАТЬ СЛОВО':
                                    show_set_word()

                                    screen.blit(bg_img, bg_rect)
                                    buttons.draw(screen)
                                    blocks.draw(screen)
                                    pygame.display.flip()

                    if back.rect.collidepoint(mouse_pos):
                        waiting = False


def show_rules():
    surf = pygame.surface.Surface((640, 360))
    surf.fill((229, 229, 229))
    rules = [
        'Механика игры состоит в составлении максимального количества',
        'слов из представленного игроку исходного слова.',
        '',
        'После составления всех возможных слов появится возможность',
        'перехода на следующий уровень.',
        '',
        'Слова, получаемые в результате, должны удовлетворять следующим',
        'требованиям:',
        '  -имя существительное;',
        '  -именительный падеж;',
        '  -минимальная длина - три буквы.'
    ]

    for i in range(len(rules)):
        print_text(surf, 30, 70 + (i * 20), rules[i], 24)

    screen.blit(surf, (320, 180))
    pygame.draw.rect(screen, BLACK, pygame.rect.Rect(320, 180, 640, 360), 3)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    waiting = False


def draw_slider():
    pygame.draw.line(screen, BLACK, (570, 270), (840, 270), 6)
    pygame.draw.line(screen, BLACK, (570, 285), (570, 255), 6)
    pygame.draw.line(screen, BLACK, (840, 285), (840, 255), 6)

    pygame.draw.line(screen, BLACK, (560, 235), (580, 235), 6)

    pygame.draw.line(screen, BLACK, (830, 235), (850, 235), 6)
    pygame.draw.line(screen, BLACK, (840, 225), (840, 245), 6)


def show_settings():
    global volume
    start = 570
    end = 840

    screen.blit(bg_img, bg_rect)
    buttons = pygame.sprite.Group()
    back = ImageButton(40, 40, 103, 55, back_img)
    buttons.add(back)

    buttons.draw(screen)

    print_text(screen, 400, 250, 'ЗВУК', 64)
    draw_slider()

    circle = pygame.surface.Surface((30, 30))
    circle.fill(WHITE)
    circle.set_colorkey(WHITE)
    circle_rect = circle.get_rect()
    pygame.draw.circle(circle, BLACK, circle_rect.center, 15)
    circle_rect.center = (start + (end - start) * volume, 270)

    screen.blit(circle, circle_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_pos = pygame.mouse.get_pos()
                    if back.rect.collidepoint(mouse_pos):
                        waiting = False

        print(volume)
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_pos[0] in range(555, 855) and mouse_pos[1] in range(255, 285) and mouse_buttons[0]:
            circle_rect.center = (mouse_pos[0], 270)

            if circle_rect.centerx < start:
                circle_rect.centerx = start

            if circle_rect.centerx > end:
                circle_rect.centerx = end

            screen.blit(bg_img, bg_rect)
            buttons.draw(screen)
            print_text(screen, 400, 250, 'ЗВУК', 64)
            draw_slider()
            screen.blit(circle, circle_rect)

            volume = (circle_rect.centerx - start) / (end - start)

            with open('settings.txt', 'w') as settings_file:
                json.dump(volume, settings_file)

            pygame.display.flip()


def show_menu():
    global user
    options = ['ИГРАТЬ', 'ПРАВИЛА', 'НАСТРОЙКИ', 'ВЫХОД']

    blocks = pygame.sprite.Group()

    screen.blit(bg_img, bg_rect)

    print_text(screen, 1010, 40, 'ИГРОК:', 36)

    for i in range(len(options)):
        tb = TextBlock(options[i], 455, 90 + (i * 150), 370, 90, 64)
        blocks.add(tb)

    user_block = TextBlock(user['name'], 1110, 35, 120, 30, 36)
    blocks.add(user_block)

    blocks.draw(screen)

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_pos = pygame.mouse.get_pos()
                    for block in blocks:
                        if block.rect.collidepoint(mouse_pos):
                            match block.text:
                                case 'ИГРАТЬ':
                                    show_play()
                                    screen.blit(bg_img, bg_rect)
                                    print_text(screen, 1010, 40, 'ИГРОК:', 36)
                                    blocks.draw(screen)

                                    pygame.display.flip()

                                case 'ПРАВИЛА':
                                    show_rules()
                                    screen.blit(bg_img, bg_rect)
                                    print_text(screen, 1010, 40, 'ИГРОК:', 36)
                                    blocks.draw(screen)

                                    pygame.display.flip()
                                case 'НАСТРОЙКИ':
                                    show_settings()
                                    screen.blit(bg_img, bg_rect)
                                    print_text(screen, 1010, 40, 'ИГРОК:', 36)
                                    blocks.draw(screen)

                                    pygame.display.flip()
                                case 'ВЫХОД':
                                    pygame.quit()

                            if block.text == user['name']:
                                show_profile()
                                screen.blit(bg_img, bg_rect)
                                print_text(screen, 1010, 40, 'ИГРОК:', 36)

                                blocks.remove(user_block)
                                user_block = TextBlock(user['name'], 1110, 35, 120, 30, 36)
                                blocks.add(user_block)

                                blocks.draw(screen)

                                pygame.display.flip()


all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()

show_profile()
show_menu()

pygame.quit()
