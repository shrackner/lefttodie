import pygame
from Animation import Animate, AllSprites
import random

class Screen:
    def __init__(self):
        self.state = "GAMESCREEN"
        self.left = False
        self.screenw = 1024
        self.screenh = 768
        self.screen = pygame.display.set_mode((self.screenw, self.screenh))      
        self.clouds = Clouds()
        self.cloudlist = self.clouds.clouds
        self.cloudsnormal = sorted(self.clouds.cloudimages)
        self.cloudsinverted = sorted(self.clouds.cloudsinverted)
                                              
        #pygame.display.set_caption('Left To Die')
        #animator = Animate(Animation.AllSprites['playerIdleNormal.png'], 2, 2, 5, 32, 32)

    def update(self):

        if self.state == "LIFESCREEN":
            pass
        elif self.state == "GAMESCREEN":
            self.clouds.cloudupdate()
            
        elif self.state == "ENDSCREEN":
            pass

        self.draw()

    def draw(self):
        if self.state == "LIFESCREEN":
            background_colour = (255, 255, 255)
            self.screen.fill(background_colour)
                                              
        elif self.state == "GAMESCREEN":
            if self.left:
                self.background = AllSprites["backgroundInverse.png"]
                for i in range(0, len(self.cloudlist)):
                    if "Inverse" not in self.cloudlist[i][3]:
                        self.cloudlist[i][3] = self.cloudsinverted[int(self.cloudlist[i][3][5]) - 1]
                                 
            else:
                for i in range(0, len(self.cloudlist)):
                    if "Normal" not in self.cloudlist[i][3]:
                        self.cloudlist[i][3] = self.cloudsnormal[int(self.cloudlist[i][3][5]) - 1]
  
                self.background = AllSprites["backgroundNormal.png"]

            self.screen.blit(self.background, (0, 0))

            for i in range(0, len(self.cloudlist)):
                self.screen.blit(AllSprites[self.cloudlist[i][3]], (self.cloudlist[i][0], self.cloudlist[i][1]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit();

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.left = True
                    elif event.key == pygame.K_RIGHT:
                        self.left = False
            
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
            self.clouds.append([random.randrange(100, 900),random.randrange(117, 500), random.randint(1,3), self.cloudimages[random.randint(0,len(self.cloudimages) - 1)]])

    def cloudupdate(self):
        for i in range(len(self.clouds)):
            self.clouds[i][0] -= self.clouds[i][2]
            if self.clouds[i][0] + 100 < 0:
                self.clouds[i][0] = 1020

