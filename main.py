import pygame
from random import randint
from time import time as timer
pygame.init()
HEIGHT = 900
WIDTH = 1600
display = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(pygame.image.load("img.png"), (WIDTH, HEIGHT))
missed = 0
killed = 0
health = 3

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, playerimg, x, y, width, height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(playerimg), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        display.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
class Player(GameSprite):
    def move(self):
        press = pygame.key.get_pressed()
        if press[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.x <= -110:
                self.rect.x = WIDTH
        if press[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.x >= WIDTH:
                self.rect.x = -110
    def fire(self):
        bullet = Bullet("amogus.jpg", self.rect.x + 50, self.rect.y, 20, 20, 4)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            self.rect.y = 0
            self.rect.x  = randint(0, int(WIDTH - 40))
            missed += 1

pl = Player("durak_smirk.png", 750, 800, 100, 100, 9)
pg = pygame.sprite.Group()
eg = pygame.sprite.Group()
restartbtn = GameSprite("reset.png", 0, 220, 128, 128, 0)
rgroup = pygame.sprite.Group()
rgroup.add(restartbtn)
bullets = pygame.sprite.Group()
pg.add(pl)
for i in range(7):
    enemy = Enemy("durak_bully.png", randint(0, int(WIDTH - 50)), 0, 100, 100, randint(1,4))
    eg.add(enemy)

pygame.font.init()
mainfont = pygame.font.Font('Lato-Medium.ttf', 72)
notmainfont = pygame.font.Font('Lato-Medium.ttf', 36)
rtext = notmainfont.render("Reloading", True, (255, 249, 166))
restart = mainfont.render("Game over!", True, (255, 249, 166))
clock = pygame.time.Clock()
reloading = False
reload_time = 0
run = True
finished = False
restarting = False
ammo = 12
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not reloading:
                    ammo -= 1
                    pl.fire()

    if not finished:
        display.blit(bg, (0,0))
        healthinfo = notmainfont.render("Health: " + str(health) + "/3", True, (255, 249, 166))
        display.blit(healthinfo, (20, 20))
        score = notmainfont.render("Score: " + str(killed) + "/50", True, (255, 249, 166))
        display.blit(score, (20, 55))
        missedtext = notmainfont.render("Missed: " + str(missed) + "/5", True, (255, 249, 166))
        display.blit(missedtext, (20, 90))
        ammotext = notmainfont.render("Ammo: " + str(ammo) + "/12", True, (255, 249, 166))
        display.blit(ammotext, (20, 125))
        pl.reset()
        pl.move()
        eg.draw(display)
        eg.update()
        if missed >= 5:
            restarting = True
        if health <= 0:
            restarting = True
        if killed >= 25:
            win = mainfont.render("You win, 25 killed!", True, (255, 249, 166))
            display.blit(win, (200, 430))
            finished = True
        bullets.update()
        bullets.draw(display)
        coll = pygame.sprite.groupcollide(pg, eg, False, True)
        if coll:
            health -= 1
        bulletcoll = pygame.sprite.groupcollide(bullets, eg, True, True)
        for col in bulletcoll:
            killed += 1
            enemy = Enemy("durak_bully.png", randint(0, int(WIDTH - 50)), 0, 100, 100, randint(1,5))
            eg.add(enemy)
        if restarting:
            for e in eg:
                e.kill()
            display.blit(restart, (450, 430))
            restartbtn.reset()
            coll = pygame.sprite.groupcollide(bullets, rgroup, True, False)
            if coll:
                restarting = False
                finished = True

        if ammo == 0 and reloading == False:
            reload_time = timer()
            reloading = True
        if reloading == True:
            display.blit(rtext, (20, 160))
        if 3 > abs(reload_time - timer()) > 2:
            ammo = 12
            reloading = False
        
        pygame.display.update()
        clock.tick(120)
    else:
        for e in eg:
            e.kill()
        for e in bullets:
            e.kill()
        pl.rect.x = 750
        for i in range(7):
            enemy = Enemy("durak_bully.png", randint(0, int(WIDTH - 50)), 0, 100, 100, randint(1,4))
            eg.add(enemy)
        finished = False
        killed = 0
        missed = 0
        ammo = 12