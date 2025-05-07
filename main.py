from pygame import *
from random import randint
from time import time as timer

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

game = True

clock = time.Clock()
FPS = 50

speed = 5

img_bullet = 'bullet.png'
img_enemy = 'ufo.png'
img_aster = 'asteroid.png'

num_fire = 0
rel_time = False

mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
lost = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)

monsters = sprite.Group()
asteroids = sprite.Group()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        keys = key.get_pressed()
        if self.rect.y < 0:
            self.kill()
            
bullets = sprite.Group()

for i in range(1, 4):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

for i in range(1, 3):
    asteroid = Asteroid(img_aster, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
    asteroids.add(asteroid)

font.init()
font1 = font.SysFont('Arial', 40)

font.init()
font = font.SysFont('Arial', 70)

winfin = font.render(
    'YOU WIN!', True, (255, 255, 0)
)
fail = font.render(
    'YOU LOSE!', True, (255, 0, 0)
)
bullet_reload = font1.render(
    'Погодь...перезагрузка 3 сек', True, (255, 255, 255)
)

ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    ship.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    now_time = timer()


    if finish != True:
        window.blit(background,(0,0))
        lose = font1.render(
            'Пропущено:' + str(lost), True, (255, 255, 255)
        )
        win = font1.render(
            'Сбито:'+ str(score), True, (255, 255, 255)
        )
        
        window.blit(win, (10, 20))
        window.blit(lose, (10, 50))
        bullets.update()
        ship.update()
        monsters.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list_monster = sprite.spritecollide(ship, monsters, False)
        sprites_list_aster = sprite.spritecollide(ship, asteroids, False)

        if rel_time:
            cur_time = timer()
            if cur_time - now_time < 2:
                window.blit(bullet_reload , (200, 450))
            else:
                num_fire = 0
                rel_time = False


        for collide in collides:
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)
            score += 1
        
        if score >= 10:
            window.blit(winfin, (200, 200))
            finish = True

        if lost >= 3 or sprites_list_monster or sprites_list_aster:
            window.blit(fail, (200, 200))
            finish = True
            
        display.update()

    clock.tick(FPS)