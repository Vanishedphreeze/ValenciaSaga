import pygame
import sys
import GameEntity

if GameEntity.instance.init():
    GameEntity.instance.run()
GameEntity.instance.destroy()
