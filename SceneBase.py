import pygame
import sys
import GameEntity

class SceneBase(object):
    isRunning = False
    screen = None
    bgColor = (255, 255, 255)

    def init(self):
        # load resources
        pass

    def start(self):
        # prepare initial values
        self.screen = GameEntity.instance.getWindowContext()
        self.isRunning = True

    def update(self, events):
        # this function runs once per frame
        pass

    def draw(self):
        # this function runs once per frame
        # ONLY put draw functions here
        self.screen.fill(self.bgColor)

    def destroy(self):
        # unload resources
        pass

