# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import os

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

bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
bg_rect = bg_img.get_rect()

result = ''
words = ['ОПТИКА', 'ПОТ', 'КОТ', 'КАТ', 'ТОК', 'ПАТОКА', 'ПТАШКА', 'ШАПИТО',
         'ИКОТА', 'КАКАО', 'КАПОТ', 'КАТОК', 'КИШКА', 'КОШКА', 'ОПИАТ', 'ТАПКА',
         'ИШАК', 'КИПА', 'ПАКТ', 'ПИКА', 'ШПАК', 'ТОП', 'ШОК', 'ПАТ',
         'ОПТ', 'ШИК']
results = []

class TextBlock(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.height = 40
        self.font_size = 24
        self.width = 10 + len(self.text) * 15
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

    def setText(self, text):
        self.text = text

    def getText(self):
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
            self.setPressed(True)

    def setPressed(self, pressed):
        self.pressed = pressed

class AcceptButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 60
        self.image = accept_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH - (self.width + 20), HEIGHT - (self.height + 20))


    def update(self):
        self.border = pygame.rect.Rect(0, 0, self.width, self.height)
        self.border_color = BLACK
        pygame.draw.rect(self.image, self.border_color, self.border, 3)

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            global result
            if result in words:
                results.append(result)
                words.remove(result)
                result = ''
                for button in buttons:
                    button.setPressed(False)

class EraseButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 60
        self.image = erase_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH - (self.width + 100), HEIGHT - (self.height + 20))


    def update(self):
        self.border = pygame.rect.Rect(0, 0, self.width, self.height)
        self.border_color = BLACK
        pygame.draw.rect(self.image, self.border_color, self.border, 3)

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            global result
            result = ''
            for button in buttons:
                button.setPressed(False)


def form_results():
    x = 50
    y = 150
    for i in range(len(results)):
        tb = TextBlock(results[i], x, y)
        all_sprites.add(tb)
        y += 55
        if (i + 1) % 5 == 0:
            y = 150
            x += 150

all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()

word = 'капитошка'
word = word.upper()
letter_width = 80
letter_spacing = 20
letter_font_size = 52

x = (WIDTH - len(word) * letter_width - (len(word)-1) * letter_spacing)/2
for letter in word:
    button = Button(x, 504, letter, letter_width, letter_width, letter_font_size)
    all_sprites.add(button)
    buttons.add(button)
    x += letter_width + letter_spacing

erase_btn = EraseButton()
accept_btn = AcceptButton()
resblock = ResBlock()
all_sprites.add(erase_btn)
all_sprites.add(accept_btn)
all_sprites.add(resblock)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    print(result)


    # Обновление
    resblock.setText(result)
    all_sprites.update()
    form_results()

    # Рендеринг
    screen.blit(bg_img, bg_rect)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()