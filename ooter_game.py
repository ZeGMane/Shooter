from pygame import *
from random import randint
import time as timer

win = display.set_mode((700,500))
display.set_caption('Шутер')

class GameSprite(sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed

    def fire(self):   
        bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)

        
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(50, 600)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(50, 600)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


player_image = transform.scale(image.load('rocket.png'), (70,100))
enemy_image = transform.scale(image.load('ufo.png'), (100,70))
bullet_image = transform.scale(image.load('bullet.png'), (15,20))
asteroid_image = transform.scale(image.load('asteroid.png'), (80,80))

player = Player(player_image, 200,400, 10)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    enemy1 = Enemy(enemy_image, randint(10,400), 0, randint(1, 3))
    monsters.add(enemy1)

for i in range(3):
    asteroid1 = Asteroid(asteroid_image, randint(10, 400), 0 , randint(2 ,5))
    asteroids.add(asteroid1)

run = True
finish = False
bg = transform.scale(image.load('galaxy.jpg'), (700,500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

font.init()
font = font.Font(None, 36)


winner = font.render('YOU WIN!', True, (255,150,0))
lose = font.render('YOU LOSE', True,(255,0,0))
reloading = font.render('wait, reload', True, (255,0,50))

podbito = 0
ammo = 0
r = False

clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not r:
                ammo += 1
                player.fire()
                fire.play()
            if ammo >= 5 and not r:
                last_time = timer.time()
                r = True

    if not finish:
        win.blit(bg, (0,0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(win)
        bullets.update()
        bullets.draw(win)
        asteroids.update()
        asteroids.draw(win)

        lost_text = font.render('Пропущено: '+str(lost), True, (255,255,255))
        win.blit(lost_text, (10,10))

        schet = font.render('Счёт: '+str(podbito), True, (255,255,255))
        win.blit(schet, (10, 40))

        podbito_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in podbito_list:
            podbito += 1
            enemy1 = Enemy(enemy_image, randint(10,400), 0, randint(1, 3))
            monsters.add(enemy1)
            if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
                sprite.spritecollide(player, monsters, True)
                sprite.spritecollide(player, asteroids, True)

        
        if podbito >= 10:
            win.blit(winner, (300, 250))
            finish = True

        lost_list = sprite.spritecollide(player, monsters, False)
        lost_list2 = sprite.spritecollide(player, asteroids, False)
        if lost >= 3 or lost_list or lost_list2:
            win.blit(lose, (300, 250))
            finish = True

        sprite.groupcollide(asteroids, bullets, False,True)

        if r:
            new_time = timer.time()
            if new_time - last_time < 3:
                reloading = font.render('wait, reload', True, (255,0,50))
                win.blit(reloading, (250,450))

            else:
                ammo = 0
                r = False
    else:
        finish = False
        podbito = 0
        lost = 0
        ammo = 0

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()   
        
        time.delay(3000)
        for i in range(5):
            enemy1 = Enemy(enemy_image, randint(10,400), 0, randint(1, 3))
            monsters.add(enemy1)

        for i in range(3):
            asteroid1 = Asteroid(asteroid_image, randint(10, 400), 0 , randint(2 ,5))
            asteroids.add(asteroid1)

    clock.tick(60)
    display.update()
    time.delay(50)