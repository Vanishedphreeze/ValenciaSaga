import pygame
import sys
import GameEntity
import BattleManager
from SceneBase import SceneBase

class BattleScene(SceneBase):
    def init(self):
        super().init()

    def start(self):
        super().start()

    def update(self, events):
        # this should be put in somewhere else, depends on kinds of events
        # to fetch the input operations, use InputManager
        super().update(events)
        for event in events :
            if event.type == pygame.QUIT :
                sys.exit()

        # updates
        # BattleManager.battleManager._drawPhase();
        # BattleManager.battleManager._standbyPhase();
        # BattleManager.battleManager._mainPhase();
        # BattleManager.battleManager._endPhase();

    def draw(self):
        super().draw()

    def destroy(self):
        super().destroy()

