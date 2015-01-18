import pygame
from Animation import Animate, AllSprites
import random
import sys
import Tiles

class Screen:
    def __init__(self):
        self.go = True
        self.state = "LIFESCREEN"
        self.left = False
        self.screenw = 1024
        self.screenh = 768
        self.screen = pygame.display.set_mode((self.screenw, self.screenh))
        pygame.font.init()
        self.fontpath = pygame.font.match_font('lucidasans')
        self.font = pygame.font.Font(self.fontpath, 28)

        self.clouds = Clouds()
        self.cloudlist = self.clouds.clouds
        self.cloudsnormal = sorted(self.clouds.cloudimages)
        self.cloudsinverted = sorted(self.clouds.cloudsinverted)

        self.startplayer= Animate(AllSprites['playerMoveNormal.png'], 2, 2, 5, 32, 32)

        self.current_level = 1
        self.lives = 3
        self.l_screen_clock = pygame.time.Clock()
        self.l_screen_time = 0


                                              
    def update(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left = True
                elif event.key == pygame.K_RIGHT:
                    self.left = False

        if self.state == "LIFESCREEN":
            self.startplayer.Aupdate()
            self.l_screen_time += self.l_screen_clock.tick()
            if self.l_screen_time >= 3000:
                self.state = "GAMESCREEN"
                self.l_screen_time = 0

        elif self.state == "GAMESCREEN":
            self.clouds.cloudupdate()
            
        elif self.state == "ENDSCREEN":
            pass

    def draw(self):
        if self.state == "LIFESCREEN":
            background_colour = (0, 0, 0)
            self.screen.fill(background_colour)
            self.startplayer.draw(self.screen, 460, 352)
            text = self.font.render("x " + str(self.lives), True, pygame.Color(255,255,255))
            self.screen.blit(text, (492, 347))
                                              
        elif self.state == "GAMESCREEN":             
            if self.left:
                self.sun = AllSprites["sunInverse.png"]
                self.background = AllSprites["backgroundInverse.png"]
                for i in range(0, len(self.cloudlist)):
                    if "Inverse" not in self.cloudlist[i][3]:
                        self.cloudlist[i][3] = self.cloudsinverted[int(self.cloudlist[i][3][5]) - 1]
                                 
            else:
                self.sun = AllSprites["sunNormal.png"]
                self.background = AllSprites["backgroundNormal.png"]
                for i in range(0, len(self.cloudlist)):
                    if "Normal" not in self.cloudlist[i][3]:
                        self.cloudlist[i][3] = self.cloudsnormal[int(self.cloudlist[i][3][5]) - 1]

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.sun, (0, 0))

            for i in range(0, len(self.cloudlist)):
                self.screen.blit(AllSprites[self.cloudlist[i][3]], (self.cloudlist[i][0], self.cloudlist[i][1]))
           
        elif self.state == "ENDSCREEN":
            pass            
 
        
        pygame.display.update()


class Clouds:
    def __init__(self):
        self.cloudnum = random.randint(5,15)

        self.clouds = []
        self.cloudimages = []
        self.cloudsinverted = []
        
        for sprite, image in AllSprites.items():
            if "cloud" in sprite:
                if "Normal" in sprite:
                    self.cloudimages.append(sprite)
                elif "Inverse" in sprite:
                    self.cloudsinverted.append(sprite)

        for i in range(0, self.cloudnum):
            # Random width
            # Random height
            # Random speed
            # Random normal cloud
            self.clouds.append([random.randrange(100, 900),random.randrange(117, 500), random.randint(1,2), self.cloudimages[random.randint(0,len(self.cloudimages) - 1)]])

    def cloudupdate(self):
        for i in range(len(self.clouds)):
            self.clouds[i][0] -= self.clouds[i][2]
            if self.clouds[i][0] + 100 < 0:
                self.clouds[i][0] = 1020
                self.clouds[i][1] = random.randrange(117, 500)
                self.clouds[i][3] = self.cloudimages[random.randint(0, len(self.cloudimages) - 1)]

