import pygame
import sys
import GameEntity

if GameEntity.gameEntity.init():
    GameEntity.gameEntity.run()
GameEntity.gameEntity.destroy()
