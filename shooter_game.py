from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x,size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_y=size_y
        self.size_x=size_x
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= spd
        elif keys[K_RIGHT] and self.rect.x <width - 80:
            self.rect.x += spd
            '''
        elif keys[K_DOWN] and self.rect.y < height -80:
            self.rect.y += self.speed
        elif keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
            '''

    def fire(self):
        bullet=Bullet("bullet.png",self.rect.centerx,self.rect.top,15,19,10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global missed
        if self.rect.y>=height:
            self.rect.y=0
            self.rect.x=randint(80,width-80)
            missed+=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y<-25:
            self.kill()


width=700
height=500
running=True
finish=False
FPS=60
score=0
missed=0
background=transform.scale(image.load("galaxy.jpg"),(width,height))
static_background=transform.scale(image.load("static.jpg"),(width,height))
clock=time.Clock()
spd=10
max_missed=3
goal=10
difficulty=5
ufos_present=0
start=True
settings=0
pause=False
game=False
static_frames=30
current_static=0
is_static=False

screen=display.set_mode((width,height))
display.set_caption("Shooter")

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound=mixer.Sound("fire.ogg")

font.init()
font=font.SysFont('Times New Roman',40) #replace None with "cour.ttf" for better experience.

success_text=font.render("YOU WIN",True,(0,255,0))
loss_text=font.render("YOU LOSE",True,(255,0,0))
start_text=font.render("Start Game",True,(255,255,255))
pause_top_text=font.render("Paused",True,(255,0,255))
settings_text=font.render("Settings",True,(255,0,255))
settings_back_text=font.render("Back",True,(255,0,0))
settings_speed_text=font.render("Ship speed",True,(255,255,255))
settings_goal_text=font.render("Winning score",True,(255,255,255))
settings_lose_text=font.render("Losing score",True,(255,255,255))
settings_next_text=font.render("Next",True,(0,255,0))
settings_difficulty_text=font.render("Difficulty",True,(255,255,255))

ship=Player("rocket.png",width/2,height-100,65,65,spd)
ufos=sprite.Group()
for i in range (1,6):
    ufo=Enemy("ufo.png",randint(80,width-80),-40,80,50,randint(1,3))
    ufos.add(ufo)
    ufos_present+=1
bullets=sprite.Group()


while running:
    if not finish or start or game:
        rand=randint(0,180)
        if rand!=1 and is_static==False:
            screen.blit(background,(0,0))
        elif rand==1 or is_static==True:
            screen.blit(static_background,(0,0))
            is_static=True

    if ufos_present!=difficulty:
        ufo=Enemy("ufo.png",randint(80,width-80),-40,80,50,randint(1,3))
        ufos.add(ufo)
        ufos_present+=1

    for e in event.get():
        if e.type == QUIT:
            running=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                fire_sound.play()
                ship.fire()
            elif e.key==K_p:
                print(str(mouse.get_pos()))
            elif e.key==K_s:
                print(str(ship.rect.x)+","+str(ship.rect.y))
            elif e.key==K_TAB:
                if pause==False:
                    pause=True
                    game=False
                    mixer.music.pause()
                elif pause==True:
                    pause=False
                    game=True
                    mixer.music.play()


    if not finish and game==True:
        ship.reset()
        ufos.draw(screen)
        bullets.draw(screen)

        text_counter=font.render("Score: "+str(score),True,(255,255,255))
        text_missed=font.render("Missed: "+str(missed),True,(255,255,255))
        screen.blit(text_counter,(0,0))
        screen.blit(text_missed,(450,0))

        collides=sprite.groupcollide(ufos,bullets,True,True)
        for c in collides:
            score+=1
            ufo=Enemy("ufo.png",randint(80,width-80),-40,80,50,randint((difficulty-4),(difficulty-2)))
            ufos.add(ufo)

        if score >= goal:
            finish=True
            screen.blit(success_text,(281, 233))
            mixer.music.pause()

        if sprite.spritecollide(ship,ufos,False) or missed>=max_missed:
            finish=True
            screen.blit(loss_text,(281, 233))
            mixer.music.pause()

        ship.update()
        ufos.update()
        bullets.update()

    elif start==True:
        screen.blit(start_text,(30, 165))
        screen.blit(settings_text,(30, 293))
        if mouse.get_pressed()[0]==1 and 30<=mouse.get_pos()[0]<=269 and 174<=mouse.get_pos()[1]<=199:
            start=False
            game=True
        elif mouse.get_pressed()[0]==1 and 30<=mouse.get_pos()[0]<=320 and 305<=mouse.get_pos()[1]<=330:
            start=False
            settings=1

    elif pause==True:
        screen.blit(pause_top_text,(272, 117))

    elif settings==1:
        screen.blit(settings_text,(300,20))
        screen.blit(settings_back_text,(300,400))
        screen.blit(settings_speed_text,(300,199))
        screen.blit(settings_goal_text,(300,260))
        screen.blit(settings_lose_text,(300,330))
        screen.blit(settings_next_text,(452, 400))
        screen.blit(settings_difficulty_text,(300,140))
        if mouse.get_pressed()[0]==1 and 300<=mouse.get_pos()[0]<=400 and 410<=mouse.get_pos()[1]<=440:
            settings=0
            start=True
        elif mouse.get_pressed()[0]==1 and 300<=mouse.get_pos()[0]<=550 and 208<=mouse.get_pos()[1]<=239:
            spd=int(input("Input new ship movement speed-->"))
        elif mouse.get_pressed()[0]==1 and 300<=mouse.get_pos()[0]<=617 and 269<=mouse.get_pos()[1]<=296:
            goal=int(input("Input score required to win-->"))
        elif mouse.get_pressed()[0]==1 and 300<=mouse.get_pos()[0]<=600 and 337<=mouse.get_pos()[1]<=367:
            max_missed=int(input("Input amount missed required to lose-->"))
        elif mouse.get_pressed()[0]==1 and 300<=mouse.get_pos()[0]<=540 and 151<=mouse.get_pos()[1]<=180:
            difficulty=int(input("Input new difficulty (default 5)-->"))
        elif mouse.get_pressed()[0]==1 and 448<=mouse.get_pos()[0]<=551 and 411<=mouse.get_pos()[1]<=435:
            print("This is no working")

    else:
        '''
        finish=False
        score=0
        missed=0

        for b in bullets:
            b.kill()
        for m in ufos:
            m.kill()
        time.delay(5000)
        mixer.music.unpause()
        for i in range(5):
            ufo=Enemy("ufo.png",randint(80,width-80),-40,80,50,randint(1,3))
            ufos.add(ufo)
            '''
        pass

    if is_static==True:
        current_static+=1
        if current_static==static_frames:
            is_static=False
            current_static=0

    display.update()
    clock.tick(FPS)


#Eew2W
