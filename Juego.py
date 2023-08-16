# Example file showing a circle moving on screen
import pygame
import math
import random
import os

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
running = True
OpenMenu = True
Juego = True
dt = 0
pygame.display.set_caption("Masks")

print(os.getcwd())

#JUEGO PERSONAJE
player_pos = pygame.Vector2(screen.get_width() / 2-20, screen.get_height() / 2-20)
Spamton = pygame.image.load('AssetsJuego/Spamton.png')
Spamton = pygame.transform.scale_by(Spamton,0.1)
RightView = pygame.transform.flip(Spamton, True, False)
DownView = pygame.image.load('AssetsJuego/Spamtonabj.png')
DownView = pygame.transform.scale_by(DownView,1)
UpView = pygame.image.load('AssetsJuego/Spamtonarrb.png')
UpView = pygame.transform.scale_by(UpView,1)

if random.randint(0,10) == 4: #Easter Egg
    Music = pygame.mixer.music.load('AssetsJuego/MenuMusic.mp3')
else:
    Music = pygame.mixer.music.load('AssetsJuego/SpamtonMusic.mp3')


Original = Spamton
status = 0
sprin = False
Spamton_Rect = Spamton.get_rect()

#JUEGO BALAS (Animacion)

Bala_pos = pygame.Vector2(0,0)
Bala_pos2 = pygame.Vector2(965,0)
Bala_pos3 = pygame.Vector2(0,460)
Bala_pos4 = pygame.Vector2(965,460)
Bala1 = pygame.image.load("AssetsJuego/Bala 1.png")
Bala2 = pygame.image.load("AssetsJuego/Bala 2.png")
Bala3 = pygame.image.load("AssetsJuego/Bala 3.png")
Bala4 = pygame.image.load("AssetsJuego/Bala 4.png")
Bala5 = pygame.image.load("AssetsJuego/Bala 5.png")
Frames_Balas = [Bala1,Bala2,Bala3,Bala4,Bala5]
Bala_Flipped = pygame.transform.flip(Frames_Balas[0],True,False)
Bala_Flipped = pygame.transform.scale_by(Bala_Flipped,1.5)

for i,thing in enumerate(Frames_Balas):
    thing = pygame.transform.scale_by(thing,1.5)
    Frames_Balas[i] = thing

last_update_bala = pygame.time.get_ticks()
bala_cooldown = 50
frame_bala = 0

#Objects

Objects = []
bulletlist = []

class Object:
    def __init__(self, x, y, width, height, image, mask):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0,0]
        self.mask = mask

        Objects.append(self)

    def draw(self):
        screen.blit(pygame.transform.scale_by(self.image, 1.5), (self.x, self.y))

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def get_center(self):
        return self.x + self.width/2, self.y + self.height/2

#Hitboxes Balas

Mask_Bala = pygame.mask.from_surface(Frames_Balas[0])
Mask_Bala_IMAGE = Mask_Bala.to_surface()
Mask_Bala_IMAGE = pygame.transform.scale_by(Mask_Bala_IMAGE,0.85)
bulletspeed = 10

#HitboxesSpamton
player_pos_mask_IMAGE = pygame.Vector2(screen.get_width() / 2-20, screen.get_height() / 2-20)
player_pos_mask = pygame.Vector2(screen.get_width() / 2-20, screen.get_height() / 2-20)
Mask_Upview = pygame.mask.from_surface(UpView)
Mask_Upview_IMAGE = Mask_Upview.to_surface()
Mask_DownView = pygame.mask.from_surface(DownView)
Mask_DownView_IMAGE = Mask_DownView.to_surface()
Mask_RightView = pygame.mask.from_surface(RightView)
Mask_RightView_IMAGE = Mask_RightView.to_surface()
Mask_Original = pygame.mask.from_surface(Original)
Mask_Original_IMAGE = Mask_Original.to_surface()
Spamton_Mask = Mask_Original
Spamton_Mask_IMAGE = Mask_Original_IMAGE
Status_Mask_IMAGE = 0
Status_Mask = 0
sprin2 = False
sprin3 = False

#MENU
frame_0 = pygame.image.load("AssetsJuego/Sprite_1.png")
frame_1 = pygame.image.load("AssetsJuego/Sprite_2.png")
frame_2 = pygame.image.load("AssetsJuego/Sprite_3.png")
frame_3 = pygame.image.load("AssetsJuego/Sprite_4.png")
frame_0 = pygame.transform.scale_by(frame_0,8)
frame_1 = pygame.transform.scale_by(frame_1,8)
frame_2 = pygame.transform.scale_by(frame_2,8)
frame_3 = pygame.transform.scale_by(frame_3,8)
PPS = pygame.image.load("AssetsJuego/PleasePressSpace.jpg")
PPSV = pygame.image.load("AssetsJuego/PleasePressSpaceV.png")

Points_Font = pygame.font.Font("AssetsJuego/8bitoperator_jve.ttf",36)
Instrucciones = pygame.image.load("AssetsJuego/Instrucciones.png")
InstruText = Points_Font.render("Instrucciones (R)", True, (255, 255, 255))
InstruTextrect = InstruText.get_rect()
InstruTextrect.center = (850, 100)

PPSS = [PPS,PPSV]
Frames = [frame_0,frame_1,frame_0,frame_1,frame_2,frame_3,frame_2,frame_3]
last_update = pygame.time.get_ticks()
last_updatePPS = pygame.time.get_ticks()
animation_cooldown = 100
PPS_cooldown = 600
frame = 0
fondo = (6, 6, 8)

#Ending

Ending_Neutro = pygame.image.load("AssetsJuego/Game Over Neutro.png")
Ending_Neutro = pygame.transform.scale_by(Ending_Neutro,0.7)
Ending_TryAgain = pygame.image.load("AssetsJuego/Game Over TryAgain.png")
Ending_TryAgain = pygame.transform.scale_by(Ending_TryAgain,0.7)
Ending_Run = pygame.image.load("AssetsJuego/Game Over Run.png")
Ending_Run = pygame.transform.scale_by(Ending_Run,0.7)

OpenOver = True

#Health Bars

Bar100 = pygame.image.load("AssetsJuego/HealthBarFULL.png")
Bar90 = pygame.image.load("AssetsJuego/HealthBar90.png")
Bar80 = pygame.image.load("AssetsJuego/HealthBar80.png")
Bar70 = pygame.image.load("AssetsJuego/HealthBar70.png")
Bar60 = pygame.image.load("AssetsJuego/HealthBar60.png")
Bar50 = pygame.image.load("AssetsJuego/HealthBar50.png")
Bar40 = pygame.image.load("AssetsJuego/HealthBar40.png")
Bar30 = pygame.image.load("AssetsJuego/HealthBar30.png")
Bar20 = pygame.image.load("AssetsJuego/HealthBar20.png")
Bar10 = pygame.image.load("AssetsJuego/HealthBar10.png")
Bar1 = pygame.image.load("AssetsJuego/HealthBar1.png")
Bar0 = pygame.image.load("AssetsJuego/HealthBarMuerto.png")
HealthBars = [Bar100,Bar90,Bar80,Bar70,Bar60,Bar50,Bar40,Bar30,Bar20,Bar10,Bar1,Bar0]
HEALTH_INDICATOR = Bar100

for i,thing in enumerate(HealthBars):
    thing = pygame.transform.scale_by(thing,0.7)
    HealthBars[i] = thing

#FUNCIONES
def PressedKeys(keys,statis,sprin,player_posf):

    if not sprin:

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            statis = 0
            player_posf.x -= 200 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            statis = 1
            player_posf.x += 200 * dt
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            statis = 3
            player_posf.y -= 200 * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            statis = 2
            player_posf.y += 200 * dt
    
    elif sprin:

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            statis = 0
            player_posf.x -= 300 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            statis = 1
            player_posf.x += 300 * dt
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            statis = 3
            player_posf.y -= 300 * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            statis = 2
            player_posf.y += 300 * dt

    return statis
def Chng_status(statusis,urender,rrender,lrender,drender):

    if statusis == 0:
        renderuniversal = lrender

    elif statusis == 1:
        renderuniversal = rrender

    elif statusis == 2:
        renderuniversal = drender
    
    elif statusis == 3:
        renderuniversal = urender

    return renderuniversal
def SPRINTING(correr,cansancio):

    if keys[pygame.K_LSHIFT]:

        if cansancio <= 200:
            correr = True
            cansancio += 1

        if cansancio > 200 and cansancio <= 250:
            correr = False
            cansancio += 50

    else:
        correr = False

        if cansancio > 0:
            cansancio -= 1

    return correr, cansancio
def MENU(running_xd,Open,last_updatef,last_updatef2,framef,Juegof):

    numerosis = 0
    Instrubool = False
    while Open:

        keysmenu = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keysmenu[pygame.K_ESCAPE]:
                Open = False
                running_xd = False
                Juegof = False

        #ANIMACIÓN :D
        screen.fill(fondo)

        current_time = pygame.time.get_ticks()
        current_time2 = pygame.time.get_ticks()
        if current_time - last_updatef >= animation_cooldown:
            framef += 1
            last_updatef = current_time
            if framef >= len(Frames):
                framef = 0
        
        screen.blit(Frames[framef],(screen.get_width()/2-105, screen.get_height()/2-200))

        if current_time2 - last_updatef2 >= PPS_cooldown:
            numerosis += 1
            last_updatef2 = current_time2
            if numerosis >= 2:
                numerosis = 0

        screen.blit(PPSS[numerosis],(screen.get_width()/2-470, screen.get_height()/2+8.9))

        screen.blit(InstruText,InstruTextrect)

        if keysmenu[pygame.K_r] or Instrubool:
            Instrubool = True
            screen.blit(Instrucciones,(0,0))

            if keysmenu[pygame.K_SPACE]:
                Instrubool = False

        if keysmenu[pygame.K_SPACE] and Instrubool == False:
            running_xd = True
            Open = False
        
        pygame.display.flip()

    return running_xd,Juegof
def ScreenLimit(PosicionX,PosicionY):

    PosicionXR = PosicionX
    PosicionYR = PosicionY

    if PosicionX <= -3:
        PosicionXR = -2  
    if PosicionX >= 951:
        PosicionXR = 950
    if PosicionY >= 430:
        PosicionYR = 429
    if PosicionY <= -1:
        PosicionYR = 0

    return PosicionXR,PosicionYR
def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect
def HBar(HEALTH_INDICATOR):

    if Health >= 100:
        HEALTH_INDICATOR = HealthBars[0]
    
    elif Health >= 90:
        HEALTH_INDICATOR = HealthBars[1]

    elif Health >= 80:
        HEALTH_INDICATOR = HealthBars[2]

    elif Health >= 70:
        HEALTH_INDICATOR = HealthBars[3]

    elif Health >= 60:
        HEALTH_INDICATOR = HealthBars[4]

    elif Health >= 50:
        HEALTH_INDICATOR = HealthBars[5]

    elif Health >= 40:
        HEALTH_INDICATOR = HealthBars[6]

    elif Health >= 30:
        HEALTH_INDICATOR = HealthBars[7]

    elif Health >= 20:
        HEALTH_INDICATOR = HealthBars[8]

    elif Health >= 10:
        HEALTH_INDICATOR = HealthBars[9]

    elif Health >= 1:
        HEALTH_INDICATOR = HealthBars[10]

    elif Health <= 0:
        HEALTH_INDICATOR = HealthBars[11]

    return HEALTH_INDICATOR
def GAMEOVER(runningxd2,OpenOverf,Juegof2):

    Seleccion = 0
    pygame.mixer.music.load('AssetsJuego/GameOver.mp3')
    pygame.mixer.music.play(-1)
    while OpenOverf:
    
        keysgameover = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keysgameover[pygame.K_ESCAPE]:
                OpenOverf = False
                runningxd2 = False
                Juegof2 = False

        if Seleccion == 0:
            screen.blit(Ending_Neutro,(52,0))
        
        if Seleccion == -1:
            screen.blit(Ending_TryAgain,(52,0))
            if keysgameover[pygame.K_SPACE]:
                runningxd2 = True
                Juegof2 = True
                break
        
        if Seleccion == 1:
            screen.blit(Ending_Run,(52,0))
            if keysgameover[pygame.K_SPACE]:
                runningxd2 = False
                Juegof2 = False
                break
        
        screen.blit(Points_Text,(250,300))

        if keysgameover[pygame.K_a] or keysgameover[pygame.K_LEFT]:
            Seleccion = -1
        
        if keysgameover[pygame.K_d] or keysgameover[pygame.K_RIGHT]:
            Seleccion = 1
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    return runningxd2, Juegof2
def Shoot(flip:bool,bulletposxd:float|None=0,bulletposyd:float|None=0,amplifier:int|None=10,anglezz:float|None=0):

    RealBullet = Object(bulletposxd,bulletposyd,19,17,pygame.image.load("AssetsJuego/Bala 1.png"),"mask")

    RealBullet.velocity = [player_pos.x - bulletposxd,player_pos.y - bulletposyd]

    magnitude = (RealBullet.velocity[0] ** 2 + RealBullet.velocity[1] ** 2) ** 0.5

    RealBullet.velocity = [RealBullet.velocity[0] / magnitude*amplifier, RealBullet.velocity[1] / magnitude*amplifier]

    if flip:
        RealBullet.image = pygame.transform.flip(RealBullet.image,True,False)

    RealBullet.image = rot_center(RealBullet.image,anglezz,RealBullet.x,RealBullet.y)[0]
    RealBullet.mask = pygame.mask.from_surface(RealBullet.image)

    bulletlist.append(RealBullet)

pygame.mixer.music.play(-1)
running, Juego = MENU(running,OpenMenu,last_update,last_updatePPS,frame,Juego)

Tiredness = 0
Tiredness2 = 0
Tiredness3 = 0

RunSymbol = pygame.image.load("AssetsJuego/Speed.png")
RunSymbol = pygame.transform.scale_by(RunSymbol,0.25)

colortr = pygame.Surface((1000,750))  # the size of your rect
colortr.set_alpha(75)                # alpha level
colortr.fill((255,0,0))           # this fills the entire surface

fondo_juego = pygame.image.load("AssetsJuego/FondoEspacio.jpg")
fondo_juego = pygame.transform.scale_by(fondo_juego,0.17)

while Juego:

    #Musica Juego
    pygame.mixer.music.stop()
    pygame.mixer.music.load('AssetsJuego/SpamtonMusic2.mp3')
    pygame.mixer.music.play(-1)

    #Vida
    Health = 100

    #Puntos y Delay
    Points = 0
    RangeDelay = 400

    while running:
        
        keys = pygame.key.get_pressed()
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                running = False
                Juego = False
                OpenOver = False

        screen.blit(fondo_juego,((0,0)))

        Points_Text = Points_Font.render("Score: "+str(Points), True, (255, 255, 255))
        textrect = Points_Text.get_rect()
        textrect.center = (700, 480)
        screen.blit(Points_Text,textrect)

        #Hitboxes (Damage)
        for b in bulletlist:
            if Spamton_Mask.overlap(b.mask,((b.x,b.y)-(player_pos_mask))):
                screen.blit(colortr,(0,0))
                Health -= 1*(dt*20)
        
        if Spamton_Mask.overlap(Mask_Bala,((Bala_pos)-(player_pos_mask))):
            screen.blit(colortr,(0,0))
            Health -= 1*(dt*20)

        for obj in Objects:
            obj.update()

        # fill the screen with a color to wipe away anything from last frame
        #screen.fill("black")
        
        #AnimationBala
        """current_time_bala = pygame.time.get_ticks()
        if current_time_bala - last_update_bala >= bala_cooldown:
            frame_bala += 1
            last_update_bala = current_time_bala
            if frame_bala >= len(Frames_Balas):
                frame_bala = 0
        
        screen.blit(Frames_Balas[frame_bala],(0,0))"""

        #Bullet Rotation

        angle1 = math.degrees(math.atan(player_pos.y/player_pos.x)*(-1))
        if angle1 > 81:
            angle1 = angle1*-1
        
        angle2 = math.degrees(math.atan(player_pos.y/(screen.get_width() - player_pos.x)))

        angle3 = math.degrees(math.atan((screen.get_height() - player_pos.y)/player_pos.x))
        if angle3 < 0:
            angle3 = angle3*-1
        
        angle4 = math.degrees(math.atan((screen.get_height() - player_pos.y)/(screen.get_width() - player_pos.x)))*(-1)

        BulletRotadaBliteable = rot_center(Frames_Balas[0],angle1,Bala_pos.x,Bala_pos.y)
        BulletRotadaBliteable2 = rot_center(Bala_Flipped,angle2,Bala_pos2.x,Bala_pos2.y)
        BulletRotadaBliteable3 = rot_center(Frames_Balas[0],angle3,Bala_pos3.x,Bala_pos3.y)
        BulletRotadaBliteable4 = rot_center(Bala_Flipped,angle4,Bala_pos4.x,Bala_pos4.y)

        #Balas

        screen.blit(BulletRotadaBliteable[0],Bala_pos)
        screen.blit(BulletRotadaBliteable2[0],Bala_pos2)
        screen.blit(BulletRotadaBliteable3[0],Bala_pos3)
        screen.blit(BulletRotadaBliteable4[0],Bala_pos4)

        #Shoot!

        if random.randint(1,RangeDelay) == 2:
            Shoot(False,0,0,bulletspeed,angle1)
            
        elif random.randint(1,RangeDelay) == 5:
            Shoot(True,965,0,bulletspeed,angle2)
            
        elif random.randint(1,RangeDelay) == 8:
            Shoot(False,0,460,bulletspeed,angle3)
            
        elif random.randint(1,RangeDelay) == 3:
            Shoot(True,965,460,bulletspeed,angle4)
                    

        #Health Bar

        HEALTH_INDICATOR = HBar(HEALTH_INDICATOR)
        screen.blit(HEALTH_INDICATOR,(400,456))

        """Rectangulo_rocho = pygame.draw.rect(screen,"red",((414,456),(178,64)),1)
        Rectangulo_spam = pygame.draw.rect(screen,"red",((player_pos.x,player_pos.y),(Spamton_Rect[2],Spamton_Rect[3])),1)"""

        #Movement
        Spamton = Chng_status(status,UpView,RightView,Original,DownView)
        Spamton_Mask_IMAGE = Chng_status(Status_Mask_IMAGE,Mask_Upview_IMAGE,Mask_RightView_IMAGE,Mask_Original_IMAGE,Mask_DownView_IMAGE)
        Spamton_Mask = Chng_status(Status_Mask,Mask_Upview,Mask_RightView,Mask_Original,Mask_DownView)

        screen.blit(Spamton,player_pos)
        #screen.blit(Mask_Bala_IMAGE,Bala_pos)
        #screen.blit(Spamton_Mask_IMAGE,player_pos_mask_IMAGE)

        sprin, Tiredness = SPRINTING(sprin,Tiredness)
        sprin2, Tiredness2 = SPRINTING(sprin2,Tiredness2)
        sprin3, Tiredness3 = SPRINTING(sprin3,Tiredness3)

        #Sprint_Bar

        ratio = (200-Tiredness)/200
        pygame.draw.rect(screen, "yellow", (150,467,179*ratio, 25))
        screen.blit(RunSymbol,(132,456))

        status = PressedKeys(keys,status,sprin,player_pos)
        Status_Mask_IMAGE = PressedKeys(keys,Status_Mask,sprin2,player_pos_mask_IMAGE)
        Status_Mask = PressedKeys(keys,Status_Mask,sprin3,player_pos_mask)

        #Limites de la pantalla

        player_pos.x,player_pos.y = ScreenLimit(player_pos.x,player_pos.y)
        player_pos_mask.x,player_pos_mask.y = ScreenLimit(player_pos_mask.x,player_pos_mask.y)
        player_pos_mask_IMAGE.x,player_pos_mask_IMAGE.y = ScreenLimit(player_pos_mask_IMAGE.x,player_pos_mask_IMAGE.y)

        if Health <= 0:

            screen.fill("Black")
            running = False

        for b in bulletlist:
            if -10 <= b.x <= 1000 and -10 <= b.y <= 500:
                continue
            bulletlist.remove(b)
            Objects.remove(b)
            Points += 2

        if Points == 14:
            RangeDelay -= 50
            Points += 2
        
        if Points == 28:
            RangeDelay -= 100
            Points += 2
        
        if Points == 58:
            RangeDelay -= 25
            bulletspeed += 1
            Points += 2
        
        if Points == 98:
            RangeDelay -= 50
            Points += 2
        
        if Points == 148:
            RangeDelay -= 100
            Points += 2
        
        if Points == 348:
            RangeDelay -= 25
            Points += 2
        
        if Points == 598:
            RangeDelay -= 25
            Points += 2

        if Points == 1498:
            bulletspeed += 3
            Points += 2
        
        """print(Points,"a")
        print(RangeDelay,"b")"""

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.mixer.music.stop()

    #Posiciones
    player_pos.x = screen.get_width() / 2-20
    player_pos.y = screen.get_height() / 2-20
    player_pos_mask.x = screen.get_width() / 2-20
    player_pos_mask.y = screen.get_height() / 2-20
    
    running, Juego = GAMEOVER(running,OpenOver,Juego)
    if running:
        bulletlist.clear()
        Objects.clear()

pygame.quit()