from time import sleep
from pygame import *
from random import *
mixer.init()
font.init()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, rect_x, rect_y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.rect.width = width
        self.rect.height = height

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_d]:
            self.rect.x += self.speed

        if self.rect.x > 1250:
            self.rect.x = 10

        if keys[K_a]:
            self.rect.x -= self.speed

        if self.rect.x < 0:
            self.rect.x = 1200

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 750:
            self.rect.y = randint(-120, 0)
            self.rect.x = randint(-20, 950)

    def zombi(self):

        self.rect.x += self.speed
        if self.rect.x > 1350:
            self.rect.x = randint(- 150, 0)

        if self.rect.x > (main_hero.rect.x - self.rect.x + 50 ):
            self.speed = 8
        else:
            self.speed = 3


class Gift(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 200:
            self.speed = 7

        if self.rect.y > 400:
            self.speed = 10

        if self.rect.y > 710:
            self.speed = 0

        else:
            self.speed = 2


# установка значений переменных
HeightWindow = 800 # высота окна по Y
WidhtWindow = 1300 # ширина окна по X

HeightHero = 100
WidhtHero = 90

HeightZombi = 100
WidhtZombi = 90

SaveArea = 100
SizeMeteor = 100

# окно
win = display.set_mode((WidhtWindow, HeightWindow))
display.set_caption('Новогодния игра')
fon = transform.scale(image.load('bg_lvl4.png'), (WidhtWindow, HeightWindow))
win.blit(fon, (0, 0))

# игрок
main_hero = Player('main_hero.png', (WidhtWindow // 2), (HeightWindow - HeightHero), 10, WidhtHero, HeightHero)

#зомби
zombi = Enemy('zombi (2).png', 0, (HeightWindow - HeightZombi), 3, HeightZombi, WidhtZombi)


# враги
meteors = sprite.Group()
for i in range(12):
    meteor = Enemy('mon_for_ng.png', randint(0, WidhtWindow-SaveArea), randint(-120, 0), 5, SizeMeteor, SizeMeteor)
    meteors.add(meteor)

#подарок
gifts = sprite.Group()
for a in range(5):
    gift = Gift('gift_ng1.png', randint(10, WidhtWindow-SaveArea), randint(-120, 0), 4, 100, 100)
    gifts.add(gift)


# игра
fps = 60
clock = time.Clock()
game = True

#переменные прыжка
ground = HeightWindow
jump_force = 20  # сила прыжка
move = jump_force + 1

# счет подарков
collected_gifts = 0

# установка переменных счета раундов
font_round = font.Font(None, 36)
round_1 = 1

# установка переменных для счета подарков
font_total = font.Font(None, 36)

#музыка
mixer.music.load('round_1.ogg')
mixer.music.play()

mixer.music.queue('musicforgamefon.ogg')
mixer.music.play()

while game:

    #заливка главного окна фоном
    win.blit(fon, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            game = False

        #прыжок
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and ground == main_hero.rect.bottom:
                move = -jump_force

    if move <= jump_force:
        if (main_hero.rect.bottom + move) < ground:
            main_hero.rect.bottom += move
            if move < jump_force:
                move += 1

        else:
            main_hero.rect.bottom = ground
            move = jump_force + 1


    #создания переменных счета и раунда
    #раунд
    round_text = font_round.render('Раунд ' + str(round_1), True, (255, 105, 31))
    place_round = round_text.get_rect(center=(55, 15))
    win.blit(round_text, place_round)

    #счетчик
    total_text = font_round.render('Собрано подарков ' + str(collected_gifts) + ' / 40', True, (255, 105, 31))
    place_total = round_text.get_rect(center=(50, 40))
    win.blit(total_text, place_total)




    #проверка раундов (если больше 10 то раунд становится труднее)
    if collected_gifts >= 15:
        mixer.music.load('round_3.ogg')
        mixer.music.play(1)
        round_1 = 2
        meteors.update()

        SizeMeteor = 110
        meteors.speed = 5

    if collected_gifts >= 30:
        mixer.music.load('round_3.ogg')
        mixer.music.play()

        round_1 = 3
        meteors.update()

        SizeMeteor = 120
        meteors.speed = 6


    #проверка столкновений
    hits_meteors = sprite.spritecollide(main_hero, meteors, False, sprite.collide_circle)

    hits_zombi = sprite.collide_circle(main_hero, zombi)

    hits_gift = sprite.spritecollide(main_hero, gifts, True)


    if hits_zombi or hits_meteors:
        print('Проигрыш')
        #game = False

    for i in hits_gift:

        collected_gifts += 1
        gift = Gift('gift_ng1.png', randint(10, 1200), randint(-200, 0), 4, 100, 100)
        gifts.add(gift)


    main_hero.update()
    main_hero.reset()

    meteors.update()
    meteors.draw(win)

    zombi.zombi()
    zombi.reset()

    gifts.update()
    gifts.draw(win)



    clock.tick(fps)
    display.update()