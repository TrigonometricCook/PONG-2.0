import pygame, csv
from pygame.locals import *

N1 = input('Player Red, Enter your username: ')
N2 = input('Player Blue, Enter your username: ')

pygame.init()

HEIGHT = 620
WIDTH = 1200
p1, p2 = 0, 0

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("BREAKOUT")

counter = 0
test = 0
time = 10

bg_img = pygame.image.load(r'image0000.png')
bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))

Start_x=172
Start_y=200
End_x=172

Bar1_Xcoord=250
Bar1_Ycoord=485
Bar2_Xcoord=250
Bar2_Ycoord=100
Bar1_velocity=4
Bar2_velocity=-4
Bar_speed=3

Ball_Xcoord=300
Ball_Ycoord=300
Ball_Xvelocity=0
Ball_Yvelocity=3.5

Start=False
clock=pygame.time.Clock()
font_name = pygame.font.match_font('gil sans')

def timer():
    global counter, time
    if counter%60 == 0:
        time -= 1
    score(screen,str(time), 25, 700, 543)

def ball():
    BallImg=pygame.image.load(r"eraser.png")
    global Ball_Xvelocity, Ball_Yvelocity, Ball_Xcoord, Ball_Ycoord, Bar1_Xcoord, Bar1_Ycoord, Start, Bar1_velocity, Bar2_velocity
    global p1, p2
    if Start==True:
        Ball_Xcoord+=Ball_Xvelocity
        Ball_Ycoord+=Ball_Yvelocity
        timer()
    else:
        if Ball_Ycoord==114:
            Ball_Xcoord=Bar2_Xcoord+80
        elif Ball_Ycoord==460:
            Ball_Xcoord=Bar1_Xcoord+80
    
    #ball wall collision
    if Ball_Xcoord<= 60 or Ball_Xcoord >=540: 
        Ball_Xvelocity = -Ball_Xvelocity

    #ground
    if Ball_Ycoord >= 530: 
        Ball_Xcoord=Bar2_Xcoord+80
        Ball_Ycoord=114
        Ball_Xvelocity=0
        Ball_Yvelocity=3
        Start=False
        p2 += 1
    #ceiling
    if Ball_Ycoord <= 10: 
        Ball_Xcoord=Bar1_Xcoord+80
        Ball_Ycoord=460
        Ball_Xvelocity=0
        Ball_Yvelocity=3
        Start=False
        p1 += 1
    
    #Collision with Paddle 1
    if 505 >= Ball_Ycoord >= 475 and (Bar1_Xcoord-20) <= Ball_Xcoord <= (Bar1_Xcoord + 220):
        Ball_Xvelocity = Bar1_velocity
        Ball_Yvelocity = -Ball_Yvelocity-0.3    
        if Ball_Xvelocity<0:
            pass
            Ball_Xvelocity -= 0.3
        else:
            Ball_Xvelocity += 0.3
        Bar1_velocity *= 1.001    
        Ball_Ycoord-=5

    #Collision with Paddle 2
    if 80 <=Ball_Ycoord <= 120 and (Bar2_Xcoord-20) <= Ball_Xcoord <= (Bar2_Xcoord + 220): 
        Ball_Xvelocity = Bar2_velocity
        Ball_Yvelocity = -Ball_Yvelocity+0.3
        if Ball_Xvelocity<0:
            Ball_Xvelocity -= 0.3
        else:
            Ball_Xvelocity += 0.3
        Ball_Ycoord+=5
        Bar2_velocity *= 1.001
    screen.blit(BallImg,(Ball_Xcoord,Ball_Ycoord))
    
def bar():
    Bar1Img=pygame.image.load(r"secondd.png")
    Bar2Img=pygame.image.load(r"seconddd.png")
    global Bar1_Xcoord, Bar1_Ycoord, Bar1_velocity, Bar2_velocity,Bar2_Xcoord, Bar2_Ycoord
    Bar1_Xcoord += Bar1_velocity
    Bar2_Xcoord += Bar2_velocity
    if Bar1_Xcoord <= 50 or Bar1_Xcoord >= 400:
        Bar1_velocity = -Bar1_velocity
    if Bar2_Xcoord <= 50 or Bar2_Xcoord >= 400:
        Bar2_velocity = -Bar2_velocity
    screen.blit(Bar1Img,(Bar1_Xcoord,Bar1_Ycoord))
    screen.blit(Bar2Img,(Bar2_Xcoord,Bar2_Ycoord))

def score(surf, text, siStarte, x, y):
    font = pygame.font.Font(font_name, siStarte)
    text_surface = font.render(text, True, "TEAL")
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
def writeScore(N1, p1, N2, p2): 
        with open('MatchHistory.csv', 'a', newline='') as mh:
            writer = csv.writer(mh)
            writer.writerow([N1, str(p1), N2, str(p2)])

  #main namespace  
GameLoop=True
while GameLoop:
    clock.tick(60)
    counter += 1
    #screen.fill((0,40,50))
    screen.blit(bg_img,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==K_ESCAPE:
                GameLoop=False
            if event.key==K_RIGHT:
                Bar1_velocity = Bar_speed
            if event.key==K_LEFT:
                Bar1_velocity = -Bar_speed
            if event.key==K_s:
                Bar2_velocity = Bar_speed
            if event.key==K_a:
                Bar2_velocity = -Bar_speed
            if event.key==K_SPACE:
                Start=True
            elif event.type==QUIT:
                GameLoop=False
        if event.type==pygame.KEYUP:
            if event.key==K_RIGHT:
                Bar1_velocity = 0
            if event.key==K_LEFT:
                Bar1_velocity = 0
            if event.key==K_a:
                Bar2_velocity = 0
            if event.key==K_s:
                Bar2_velocity = 0
        

    if time == 0 and Start == False:
        if test < 1:
            writeScore(N1, p1, N2, p2)
            test += 1
        pygame.time.wait(2000)
        GameLoop = False
        

    #calling the image blit functions
    ball()
    bar()
    score(screen,str(p1), 25, 150, 543)
    score(screen,str(p2), 25, 153, 65)
    #updating the display
    pygame.display.update()
pygame.quit()