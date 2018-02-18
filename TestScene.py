import pygame
import sys
import GameEntity
from SceneBase import SceneBase

class TestScene(SceneBase):
    speed = [-2, 1]
    player = None
    player_pos = None

    def init(self):
        super().init()
        self.player = pygame.image.load("crop.jpg")

    def start(self):
        super().start()
        self.player_pos = self.player.get_rect()

    def update(self, events):
        super().update(events)
        for event in events :
            if event.type == pygame.QUIT :
                sys.exit()

        self.player_pos = self.player_pos.move(self.speed)

        if self.player_pos.left < 0 or self.player_pos.right > GameEntity.GameEntity.WINDOWSIZE[0] :
            self.player = pygame.transform.flip(self.player, True, False)
            self.speed[0] = -self.speed[0]

        if self.player_pos.top < 0 or self.player_pos.bottom > GameEntity.GameEntity.WINDOWSIZE[1] :
            self.speed[1] = -self.speed[1]

    def draw(self):
        super().draw()
        self.screen.blit(self.player, (self.player_pos.left, self.player_pos.top))

    def destroy(self):
        super().destroy()
