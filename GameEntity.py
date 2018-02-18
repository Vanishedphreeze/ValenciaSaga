import pygame
import sys
from SceneBase import SceneBase
from TestScene import TestScene

class GameEntity(object):
    FPS = 60
    WINDOWSIZE = (800, 600)

    _curScene = TestScene()

    _windowContext = None
    _clock = None
    isRunning = False


    def init(self):
        # init pygame and window context
        pygame.init()
        self._windowContext = pygame.display.set_mode(self.WINDOWSIZE)
        self._clock = pygame.time.Clock()

        # load scene， this should be in SceneManager
        if isinstance(self._curScene, SceneBase) :
            self._curScene.init()
            return True
        else:
            # raise RuntimeError('SceneType mismatch.')
            print('SceneType mismatch')
            return False

    def run(self):
        self._curScene.start()

        while self._curScene.isRunning :
            self._curScene.update(pygame.event.get())
            self._curScene.draw()
            pygame.display.flip()
            self._clock.tick(self.FPS)

        # if the scene should be destroyed...
        self._curScene.destroy()

    def destroy(self):
        self._curScene.destroy()

    def getWindowContext(self):
        return self._windowContext

gameEntity = GameEntity()
