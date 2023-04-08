#Создай собственный Шутер!

from pygame import *
from random import *


mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
beam = mixer.Sound('stone.ogg')


bg = "galaxy.jpg"
hero = "rocket.png"

win = display.set_mode((700, 500))
display.set_caption('dumb ufos')
background = transform.scale(image.load(bg), (700, 500))



font.init()
font2 = font.SysFont("Arial", 36)


class GameSprite(sprite.Sprite):
    def __init__(self, pimage, x, y, speed, SiX, SiY):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pimage), (SiX, SiY))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed



    def fire(self):
        bullet = Bullet("bullet.png", player.rect.x+27, player.rect.y, -10, 15, 20)
        bullets.add(bullet)        
        
        if wins > 3:
        
            bullet = Bullet("bullet.png", player.rect.x+27, player.rect.y, -2, 15, 20)
            bullets.add(bullet)

            if wins > 8:


                bullet = Bullet("bullet.png", player.rect.x-5, player.rect.y + 50, -5, 15, 20)
                bullets.add(bullet)

                bullet = Bullet("bullet.png", player.rect.x+60, player.rect.y + 50, -5, 15, 20)
                bullets.add(bullet)




score = 0 #сбито кораблей
lost = 0

class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > 500:
           self.rect.x = randint(80, 620)
           self.rect.y = 0
           lost = lost + 1


class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class asteroid(GameSprite):
    def update(self):
        if self.rect.x > 800 or self.rect.x < -100:
            self.speed *= -1
        self.rect.x += self.speed



wins = 1

win_match = 10

monsters = sprite.Group()
for i in range(1,2):
    monster = Enemy("ufo.png", randint(0, 420), 0, randint(1, 4), 70, 70)
    monsters.add(monster)


asters = sprite.Group()
for i in range(1,4):
    aster = asteroid("asteroid.png", randint(0, 420), 20 + i*80, randint(-2, 2), 100, 100)
    asters.add(aster)



bullets = sprite.Group()
    
run = True
course = False

player = GameSprite(hero, 450, 400, 6, 70, 70)
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()







    if not course:
        win.blit(background, (0, 0))

        text = font2.render("Счет: " + str(score) + "/" + str(win_match), 1, (255, 255, 255))
        win.blit(text, (10, 20))


        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        win.blit(text_lose, (10, 50))

        rounds = font2.render("Раунд:  " + str(wins), 1, (255, 255, 255))
        win.blit(rounds, (10, 80))
        

        player.update()
        monsters.update()
        bullets.update()
        asters.update()


        player.reset()  
        monsters.draw(win)
        bullets.draw(win)
        asters.draw(win)

        colds = sprite.groupcollide(monsters, bullets, True, True)
        for c in colds:
            score += 1
            monster = Enemy("ufo.png", randint(0, 420), 0, randint(1, 2), 70, 70)
            monsters.add(monster)

        f = font2.render("u dumb", 1, (255, 50, 50))

        if sprite.spritecollide(player, monsters, True):
            run = False
            win.blit(f, (200, 200))

        if sprite.groupcollide(asters, bullets, False, True):
            beam.play()

        if score >= win_match:
            for monster in monsters:
                monster.kill()
            win_match = win_match + 5 + lost
            lost = 0 
            wins += 1
            score = 0
            for i in range(0, wins):
                monster = Enemy("ufo.png", randint(0, 420), 0, randint(1, 1), 70, 70)
                monsters.add(monster)


        display.update()
    
        clock.tick(70)
        