from numpy import False_
import pygame

pygame.init()

win=pygame.display.set_mode((500,480))
pygame.display.set_caption("First pygame program")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

Soundhit=pygame.mixer.Sound('lose.wav')
Soundshoot=pygame.mixer.Sound('laser.wav')
Soundbg=pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

clock=pygame.time.Clock()
score=0

class Player(object):
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.left=False
        self.right=False
        self.walkcount=0
        self.isJump=False
        self.jumpcount=10
        self.standing=True
        self.hitbox=(self.x+17,self.y+2,31,57)

    def draw(self,win):
        if self.walkcount+1>=27:
            self.walkcount=0
        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkcount//3],(self.x,self.y))
                self.walkcount+=1
            elif self.right:
                win.blit(walkRight[self.walkcount//3],(self.x,self.y))
                self.walkcount+=1
        else:
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))

        self.hitbox=(self.x+17,self.y+2,31,57)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def hit(self):
        self.isJump=False
        self.walkcount=10
        self.x=60
        self.y=410
        self.walkcount=0
        font2=pygame.font.SysFont('Ariel',100)
        text=font2.render('-5',1,(0,0,255))
        win.blit(text,(250-(text.get_width()/2),200))
        pygame.display.update()
        i=0
        while i<200:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i=201
                    pygame.quit()



class Bullet(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=8*facing

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
               
class Platform(object):
    def __init__(self,x,y,width,height,color):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        pass

class Enemies(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=3
        self.walkcount=0
        self.end=end
        self.path=[self.x,self.end]
        self.hitbox=(self.x+17,self.y+2,31,57)
        self.health=10
        self.visible=True


    def draw(self,win):
        if self.visible:
            self.move()
            if self.walkcount+1>=33:
                self.walkcount=0
            if self.vel>0:
                win.blit(self.walkRight[self.walkcount//3],(self.x,self.y))
                self.walkcount+=1
            if self.vel<0:
                win.blit(self.walkLeft[self.walkcount//3],(self.x,self.y))
                self.walkcount+=1
            self.hitbox=(self.x+17,self.y+2,31,57)
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(win,(0,128,0),(self.hitbox[0],self.hitbox[1]-20,50-(5*(10-self.health)),10))
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def move(self):
        if self.vel>0:
            if self.x+self.vel<self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkcount=0
        else:
            if self.x-self.vel>self.path[0]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkcount=0

    def hit(self):
        global score
        score+=1
        if self.health>0:
            self.health-=1
        else:
            self.visible=False

def redraw_window():
    win.blit(bg, (0,0)) 
    text= font.render('Score: {}'.format(score),1,(0,0,0))
    win.blit(text,(390,10))
    man.draw(win)
    enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

font=pygame.font.SysFont('Ariel',30,True)
man=Player(300,410,64,64)
enemy=Enemies(100,410,64,64,400)
running=True
bullets=[]
reload=0

while running:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    if enemy.visible==True:
        if man.hitbox[1]<enemy.hitbox[1]+enemy.hitbox[3] and man.hitbox[1]+man.hitbox[3]>enemy.hitbox[1]:
                if man.hitbox[0]+man.hitbox[2]>enemy.hitbox[0] and man.hitbox[0]<enemy.hitbox[0]+enemy.hitbox[2]:
                    man.hit()
                    score-=5

    if reload>0:
        reload+=1
    if reload>3:
        reload=0

    for bullet in bullets:
        if bullet.y-bullet.radius<enemy.hitbox[1]+enemy.hitbox[3] and bullet.y+bullet.radius>enemy.hitbox[1]:
            if bullet.x+bullet.radius>enemy.hitbox[0] and bullet.x-bullet.radius<enemy.hitbox[0]+enemy.hitbox[2]:
                Soundhit.play()
                enemy.hit()
                bullets.pop(bullets.index(bullet))


        if bullet.x<500 and bullet.x>0:
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys=pygame.key.get_pressed()
    if keys[pygame.K_s] and reload==0:
        Soundshoot.play()
        if man.left:
            facing=-1
        else:
            facing=1

        if len(bullets)<5:
            bullets.append(Bullet(round(man.x+man.width//2),round(man.y+man.height//2),6,(0,0,0),facing))
        reload=1

    if keys[pygame.K_RIGHT] and man.x<500-man.width-man.vel:
        man.x+=man.vel
        man.right=True
        man.left=False
        man.standing=False

    elif keys[pygame.K_LEFT] and man.x>man.vel:
        man.x-=man.vel
        man.left=True
        man.right=False
        man.standing=False
    else:
        man.standing=True
        man.walkcount=0

    if not (man.isJump):
        if keys[pygame.K_DOWN] and man.y<500-man.height-man.vel:
            man.y+=man.vel
        if keys[pygame.K_UP] and man.y>man.vel:
            man.y-=man.vel
        if keys[pygame.K_SPACE]:
            man.isJump=True
            man.right=False
            man.left=False
            man.walkcount=0
    else:
        if man.jumpcount>=-10:
            neg=1
            if man.jumpcount<0:
                neg=-1

            man.y-= (man.jumpcount**2)*0.5*neg
            man.jumpcount-=1

        else:
            man.isJump=False
            man.jumpcount=10

    redraw_window()

pygame.quit()
