#    _HOW TO PLAY_
'''
Press space to shoot the gun
Game will play until you quit by closing the window or till you have lost
Shoot at the squares which match the color of the indicator (located at the lower right corner of the window)
Letting any squares of the indicator's color escape or shooting the wrong square will result in losing
Creator of this game:Aritra Ghosal
Square speed: 10 pixel/frame
Bullet speed: 90 pixel/frame
Frames per second: 20
'''
#    _PROGRAM_
#Environment
import pygame
import random
#Color library
color_names=["Lime","Aqua","DarkOrange","DeepSkyBlue","OrangeRed","Wheat"]
rgb_code={
    "Lime":(0,255,0),
    "Aqua":(0,255,255),
    "DarkOrange":(255,140,0),
    "DeepSkyBlue":(0,191,255),
    "OrangeRed":(255,69,0),
    "Wheat":(245,222,179),
}
#------------

while True:
    running=True
    kills=0
    width=500
    height=600
    fps=20
    rarity=50
    change_time_period_average=(800)
    civy_kill=False
    bad_escape=False
    user_kill=False
    code_address="D:\\Satan\\Text\\Programs\\Python\\Games\\Shoot the squares\\"
    #Initialization
    pygame.init()
    pygame.mixer.init()
    screen=pygame.display.set_mode((width,height))
    pygame.display.set_caption('Shoot the squares')
    clock=pygame.time.Clock()
    all_sprites=pygame.sprite.Group()
    bullets=pygame.sprite.Group()
    floaters=pygame.sprite.Group()
    def display_text(text,font,size,color,x,y):
        font_name=pygame.font.match_font(font,bold=15)
        font=pygame.font.Font(font_name,size)
        text_surface=font.render(text,True,color)
        text_rect=text_surface.get_rect()
        text_rect.topright=(x,y)
        screen.blit(text_surface,text_rect)
    # Loading shooting sound
    shoot=pygame.mixer.Sound(code_address+"gun_shot.wav")
    fail=pygame.mixer.Sound(code_address+"FAIL SOUND EFFECT.wav")
    class Gun(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.image.load(code_address+"256guns.png").convert()
            self.image.set_colorkey((255,255,255))
            self.velocity=0
            self.rect=self.image.get_rect()
            self.rect.x,self.rect.y=(width-(2*self.rect.width),3*self.rect.height)
        def shoot(self):
            self.velocity=90
        def rebound(self):
            self.velocity=-self.velocity
        def update(self):
            self.rect.x+=self.velocity
            keystate=pygame.key.get_pressed()
            if keystate[pygame.K_SPACE]:
                self.shoot()
            if self.rect.x>(width):
                self.rebound()
            if self.rect.x<(width-(2*self.rect.width)):
                self.velocity=0
                self.rect.x=(width-(2*self.rect.width))
    class Bullet(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            shoot.play()
            self.image=pygame.image.load(code_address+"bullet.png").convert()
            self.image.set_colorkey((255,255,255))
            self.velocity=90
            self.rect=self.image.get_rect()
            self.rect.x,self.rect.y=(width-(2*player.rect.width),3*player.rect.height)
        def update(self):
            self.rect.x-=self.velocity
    class Floater(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.Surface((50,50))
            self.color=rgb_code[random.choice(color_names)]
            self.image.fill(self.color)
            self.rect=self.image.get_rect()
            self.velocity=10
            self.rect.x,self.rect.y=(0,height+3*self.rect.width)
        def update(self):
            self.rect.y-=self.velocity
            if self.rect.y<-100:
                self.velocity=0
    class Indicator(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.Surface((50,50))
            self.color=rgb_code[random.choice(color_names)]
            self.image.fill(self.color)
            self.rect=self.image.get_rect()
            self.rect.y,self.rect.x=(height-self.rect.height,width-self.rect.width)
        def update(self):
            pass
        def change_color(self):
            self.color=rgb_code[random.choice(color_names)]
            self.image.fill(self.color)
    player=Gun()
    signal=Indicator()
    all_sprites.add(player)
    all_sprites.add(signal)
    #Game Loop
    while running:
        #Time management
        clock.tick(fps)
        #Event processing
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                user_kill=True
                pygame.quit()
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            b=Bullet()
            all_sprites.add(b)
            bullets.add(b)
        shots=pygame.sprite.groupcollide(floaters,bullets,True,True)
        if shots:
            for a in shots.keys():
                kills+=1
                if a.color!=signal.color:
                    civy_kill=True
                    running=False
        #Make floaters
        determiner=random.randint(0,rarity*rarity)
        if divmod(determiner,rarity)[1]==0:
            new_floater=Floater()
            floaters.add(new_floater)
            all_sprites.add(new_floater)
        for f in floaters:
            if f.rect.y<-100:
                if f.color==signal.color:
                    bad_escape=True
                    running=False
                floaters.remove(f)
                all_sprites.remove(f)
        #Change signal
        determiner2=random.randint(0,change_time_period_average*change_time_period_average)
        if divmod(determiner2,change_time_period_average)[1]==0:
            signal.change_color()
        #Update
        all_sprites.update()
        for j in bullets:
            if j.rect.x<-500:
                bullets.remove(j)
                all_sprites.remove(j)
        #Draw
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        display_text("Shot : "+str(kills),"Algerian",16,(204,0,0),width,0)
        #Render
        pygame.display.flip()
    messages=pygame.sprite.Group()
    #Picture creation
    if not user_kill:
        class Picture(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                if civy_kill:
                    self.image=pygame.image.load(code_address+"CIVYDEAD.png").convert()
                elif bad_escape:
                    self.image=pygame.image.load(code_address+"CRIMINAL.png").convert()
                self.rect=self.image.get_rect()
                self.rect.x,self.rect.y=(0,0)
        message=Picture()
        messages.add(message)
    #You Lost Loop
    done=False
    if not done and not user_kill:
        fail.play()
    while not done and not user_kill:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            keystate=pygame.key.get_pressed()
            if keystate[pygame.K_SPACE]:
                done=True
        messages.draw(screen)
        if civy_kill:
            score=kills-1
        elif bad_escape:
            score=kills
        display_text("Your score is "+str(score),"Bloodthirsty",30,(60,179,113),400,500)
        pygame.display.flip()
