#imports
import pygame
import random
import time
pygame.init()

#Make canvas
display_width=600
display_height=500
window = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Asteroid Dodger")

# define colours
black = (0,0,0)
white = (255,255,255)
green = (0,200,0)
yellow = (255,215,0)
red = (200,0,0)
bright_green = (0,255,0)
bright_yellow = (255,255,0)
bright_red = (255,0,0)


#clock for speed
clock = pygame.time.Clock()

#list of every sprite. Blocks and player blocks as well
all_sprites_list = pygame.sprite.Group()

#list patrick, bubble and asteroid
Patrick_list= pygame.sprite.Group()
Asteroid_list= pygame.sprite.Group()
Bubble_list=pygame.sprite.Group()


#set gameLoop to equal True
gameLoop=True


#set moveX and moveY
moveX,moveY=0,0


# detect collision function
def detectCollisions(x1,y1,w1,h1,x2,y2,w2,h2):
    if(x2+w2>=x1>=x2 and y2+h2>=y1>=y2):
        return True
    elif(x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2):
        return True
    elif(x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2):
        return True
    elif(x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2):
        return True
    else:
        return False 


# class for Patrick, the player 
class Patrick(pygame.sprite.Sprite): 
    #setting Patrick vaules. Loading and scaling image, starting points, height and width
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image=pygame.image.load('Patrick.png')
        self.rect=self.image.get_rect()
        self.rect.x=400 
        self.rect.y=450
        self.width=50
        self.height=50
    #call end screen function when patrick collides with asteroid
    def render(self,collision):
        if(collision==True):
            end()
            Asteroid.score=0
#represent Patrick as a block and add to sprite list
Patrick=Patrick()
all_sprites_list.add(Patrick)

#asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.width=100
        self.height=100
        self.image=pygame.image.load('Asteroid.jpg')
        self.score=0
        self.rect=self.image.get_rect()
        self.rect.x= random.randrange(0,display_width-self.width)
        self.rect.y=-50
        self.speed = random.randint(6,10)
    #draw function to make asteroid
    def Draw(self):
        if self.rect.y == -50:
            Asteroid_list.add(self)
            all_sprites_list.add(self)
        # --- Create new sprite when one leaves the screen
        if self.rect.y >= 500:
            self.rect.x = random.randrange(0,display_width-self.width)
            self.rect.y = -50
            self.speed = random.randint(6,10)
            self.score+=1
    #bubble collision function
    def bubbleHit(self):
        # see if it hits a block
        Asteroid_hit_list = pygame.sprite.spritecollide(Bubble, Asteroid_list, True)
        # for each block hit, remove the bubble and add to the score
        for block in Asteroid_hit_list:
            all_sprites_list.remove(Bubble)
            Bubble_list.remove(Bubble)
            self.rect.x = random.randrange(0,display_width-self.width)
            self.rect.y = -50 
            self.speed = random.randint(6,10)
            self.score += 1
    #call end screen function when it collides with patrick
    def render(self,collision):
        if(collision==True):
            end()
            self.score=0
    def update(self):
        self.rect.y+=self.speed
Asteroid=Asteroid()
all_sprites_list.add(Asteroid)


# Bubble Class
class Bubble(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load("bubble.jpg")
        self.rect = self.image.get_rect()
        self.numbBubble = 5
    def bubbleGone(self):
        # Remove the bubble if it flies off the screen
        if self.rect.y < -50:
            Bubble_list.remove(Bubble)
            all_sprites_list.remove(Bubble)
    #remove bubble and asteroid if they collide
    def render(self,collision):
        if(collision==True):
            Bubble_list.remove(Bubble)
            all_sprites_list.remove(Bubble)
            Asteroid.rect.x = random.randrange(0,display_width-self.width)
            Asteroid.rect.y = -50 
            Asteroid.speed = random.randint(6,10)
            Asteroid.score += 1
    def update(self):
        self.rect.y -= 10

# This represents a bubble
Bubble = Bubble()

#class for background image
class Background(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height): 
        self.x=0 
        self.y=0 
        self.width = display_width 
        self.height = display_height
        self.image = pygame.image.load("Background.png")
    #set render to make image background
    def render(self):
        window.blit(self.image, (self.x, self.y))
        def render(self):
            window.blit(self.image, (self.x, self.y))
Background = Background (0,0,600,500)

#score 
def Asteroid_dodge(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: "+str(count), True, white)
    window.blit(text, (0,0))

#how many bubbles remain
def Bubble_num(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Bubbles: "+str(count), True, white)
    window.blit(text, (510,0))
    
#change speed of asteroid as score goes up
def asteroidSpeed(self):
    if Asteroid.score>=0 and Asteroid.score<=9:
        Asteroid.speed = 8
    if Asteroid.score>=10 and Asteroid.score<=14:
        Asteroid.speed = 9
    if Asteroid.score>=20 and Asteroid.score<=19:
        Asteroid.speed = 10
    if Asteroid.score>=25 and Asteroid.score<=29:
        Asteroid.speed = 11
    if Asteroid.score>=30:
        Asteroid.speed = 12

# Function for button clicking
def button(msg,x,y,width,height,iC,aC,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # detect if "button" was pressed
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(window, aC, (x,y,width,height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, iC, (x,y,width,height))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText, black)
    textRect.center = ( (x+(width/2)),(y+(height/2)) )
    window.blit(textSurf, textRect)

#quit game function
def quitGame():
    pygame.quit()
    quit()

#text function
def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

#game start to start the game
def gameStart():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        Background.render()
        largeText = pygame.font.Font("freesansbold.ttf",70)
        TextSurf, TextRect = text_objects("Asteroid Dodger", largeText, black,)
        TextRect.center = ((display_width/2),(display_height/2))
        window.blit(TextSurf, TextRect)

        button("PLAY",75,410,135,20,green,bright_green,gameLoop)
        button("QUIT",415,410,135,20,red,bright_red,quitGame)

        pygame.display.update()
        clock.tick(15)


#end screen function     
def end():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # diaplay "Game Over"
        largeText = pygame.font.Font("freesansbold.ttf",70)
        TextSurf, TextRect = text_objects("Game Over", largeText, white)
        TextRect.center = ((display_width/2),(display_height/2)-100)
        window.blit(TextSurf, TextRect)
        # Define font
        font = pygame.font.SysFont(None, 50)
        # number of Asteroids dodged
        text1 = font.render("Asteroids Dodged: "+str(Asteroid.score), True, white)
        window.blit(text1, (0,0))
        # buttons
        button("PLAY",75,410,135,20,green,bright_green,gameLoop)
        button("QUIT",415,410,135,20,red,bright_red,quitGame)

        pygame.display.update()
        clock.tick(15)


#MAIN LOOP
def gameLoop():
    #reset values
    Asteroid.rect.x = random.randrange(0,display_width-Asteroid.width)
    Asteroid.rect.y = -50
    Asteroid.score=0
    Bubble.numbBubble=5
    running=True
    
    #make moveX equal something
    moveX=0
    global pause
    while running:
        #movement keys
        for event in pygame.event.get():
            if (event.type==pygame.QUIT): 
                    gameLoop=False
            if (event.type==pygame.KEYDOWN): 
                if (event.key==pygame.K_LEFT): 
                    moveX = -4
                if (event.key==pygame.K_RIGHT): 
                    moveX = 4
                if (event.key==pygame.K_UP): 
                    moveY = -4
                if (event.key==pygame.K_DOWN):
                    moveY = 4
                if event.key == pygame.K_SPACE:
                    if 0 < Bubble.numbBubble:
                        # Set the Bubble so it is where the Patrick is
                        Bubble.rect.x = Patrick.rect.x + 25
                        Bubble.rect.y = Patrick.rect.y + 25
                        # Add the Bubble to the lists
                        all_sprites_list.add(Bubble)
                        Bubble_list.add(Bubble)
                        Bubble.numbBubble -= 1
            if (event.type==pygame.KEYUP): 
                if (event.key==pygame.K_LEFT): 
                    moveX=0
                if (event.key==pygame.K_RIGHT): 
                    moveX=0
                if (event.key==pygame.K_UP): 
                    moveY=0
                if (event.key==pygame.K_DOWN): 
                    moveY=9

        #makes canvas black
        Background.render()

        #bullet collision
        Asteroid.bubbleHit()
        Bubble.bubbleGone()
        
        #call speed function
        asteroidSpeed(Asteroid.score)
        
        #draw in asteroid
        Asteroid.Draw()
        
        # Pat moves      
        Patrick.rect.x+=moveX

        #update sprites
        all_sprites_list.update()

        # restricting Patrick's movements so he can only move left and right and stay on the screen
        if Patrick.rect.x>=750:
            Patrick.rect.x=750
        if Patrick.rect.x<=0:
            Patrick.rect.x=0
        if Patrick.rect.y>=350:
            Patrick.rect.y=350
        if Patrick.rect.y<=400:
            Patrick.rect.y=400

        #set collisions  to the detectCollisions function for bubble and patrick with asteroid
        collisions=detectCollisions(Patrick.rect.x,Patrick.rect.y,Patrick.rect.width,Patrick.rect.height,Asteroid.rect.x,Asteroid.rect.y,Asteroid.rect.width,Asteroid.rect.height)
        

        #use collision detection
        Patrick.render(collisions)
        Asteroid.render(False)

        #call score function
        Asteroid_dodge(Asteroid.score)
        Bubble_num(Bubble.numbBubble)

     
        #speed
        all_sprites_list.draw(window)
        pygame.display.update()
        clock.tick(85)
#call gameStart to start the loop and title screen
gameStart()

