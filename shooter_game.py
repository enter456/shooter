from pygame import *
from random import randint
from time import time as timer

win_width = 700
win_height = 500
img_back = 'galaxy.jpg'
img_enemy = 'ufo.png'
img_hero = 'rocket.png'
bullet = 'bullet.png'
img_asteroid = 'asteroid.png'
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load('galaxy.jpg'),(700, 500))
score = 0
goal = 10
lost = 0
max_lost = 3
life = 3
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost=lost + 1
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0                                  
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (0, 255, 0))  
lose = font1.render('YOU LOSE!', True, (180, 0, 0))      
font2 = font.SysFont('Arial', 36)                           
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')       


class Player(GameSprite):
    def update(self):
        keys_pressed =  key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > -10:
            self.rect.x -= self.speed                                   
        if keys_pressed[K_d] and self.rect.x < 640:
            self.rect.x += self.speed   
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


clock = time.Clock()
player = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Asteroid(img_asteroid,randint(30, win_width - 30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)
bullets = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)
    
  

finish = False
run = True
rel_time = False
num_fire = 0  
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False 
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    player.fire() 
                    fire_sound.play()  
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True   
    if not finish:
        window.blit(background, (0,0))        
        text_lose = font2.render('Пропущено: {}'.format(lost),True,(255,255,255))
        window.blit(text_lose, (10,50))
        text_score = font2.render('Счёт: {}'.format(score),True,(255,255,255))
        window.blit(text_score, (10,20))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)   
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Перезаряжается...', 1, (150, 0 ,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False  
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)  
        
        if score >= goal:
            finish = True
            window.blit(win, (200,200))
        if sprite.spritecollide(player, monsters,True) or sprite.spritecollide(player,asteroids,True):
            asteroid = Asteroid(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)
            life = life - 1
        if life==0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200)) 
        text_life = font2.render('Жизни: {}'.format(life),True,(255,255,255))
        window.blit(text_life, (10,80)) 
            
        display.update()
    clock.tick(40)