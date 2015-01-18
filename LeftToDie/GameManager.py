from ScreenManager import Screen
import ScreenManager

class GameManager:

    go = False
    state = ""
    screen = Screen()

    def __init__(self, state):
        self.go = True
        self.state = state

    def run(self):
        self.update()

    def update(self):
        self.screen.update()
        self.screen.draw()

##    def draw(self):
##        
##        if self.state == "LIFESCREEN":
##            print("I Do not")
##        elif self.state == "GAMESCREEN":
##            print("Well you suck")
##        elif self.state == "ENDSCREEN":
##            print("At least I'm not Dead")

    def endGame(self):
        self.go = False

    def changeState(self, newState):
        self.state = newState
