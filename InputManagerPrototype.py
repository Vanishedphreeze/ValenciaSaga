import GameObject
from SceneBase import SceneBase

class TestScene(SceneBase):
    '''
    speed = [-2, 1]
    originalplayer = None
    player = None
    player_pos = None
    ratio = 1
    '''
    image = None
    player = GameObject.GameObject()

    # operations
    isPressed = False
    isClick = False
    mousepos = None
    dpos = None

    isDragging = False


    def init(self):
        super().init()
        '''
        # self.player = pygame.image.load("crop.jpg")
        self.originalplayer = pygame.image.load("crop.jpg")
        self.player = self.originalplayer
        '''
        self.image = pygame.image.load("crop.jpg")
        self.player.init(self.image, (0, 0), (50, 50))

        self.mousepos = [0, 0]


    def start(self):
        super().start()
        '''
        self.player_pos = self.player.get_rect()
        '''
        self.player.start()

    def update(self, events):
        super().update(events)
        self.isClick = False
        # for testing event
        cnt = 0

        for event in events :
            print(event)
            if event.type == pygame.QUIT :
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN :
                self.isPressed = True
                self.isClick = True
            elif event.type == pygame.MOUSEBUTTONUP :
                self.isPressed = False

            if event.type == pygame.MOUSEMOTION :
                self.mousepos = event.pos
                cnt += 1

        if cnt >= 2:
            print("cnt larger than 2")
        # print(self.mousepos)
        # if self.isClick and not self.isDragging and //inRange//:
        if self.isClick:
            self.dpos = [self.mousepos[0] - self.player.position[0], self.mousepos[1] - self.player.position[1]]

        if self.isPressed:
            self.player.position[0] = self.mousepos[0] - self.dpos[0]
            self.player.position[1] = self.mousepos[1] - self.dpos[1]

        # inputManger seems very necessary now



        '''
        self.ratio += 0.01

        self.player_pos = self.player_pos.move(self.speed)
        self.player = pygame.transform.smoothscale(self.originalplayer, (int(self.player_pos.width * self.ratio), int(self.player_pos.height * self.ratio)) )

        if self.player_pos.left < 0 or self.player_pos.right > GameEntity.GameEntity.WINDOWSIZE[0] :
            self.player = pygame.transform.flip(self.player, True, False)
            self.speed[0] = -self.speed[0]

        if self.player_pos.top < 0 or self.player_pos.bottom > GameEntity.GameEntity.WINDOWSIZE[1] :
            self.speed[1] = -self.speed[1]
        '''

        self.player.update()

    def draw(self):
        super().draw()
        '''
        self.screen.blit(self.player, (self.player_pos.left, self.player_pos.top))
        '''
        self.player.draw(self.screen)

    def destroy(self):
        super().destroy()
        self.player.destroy()
