class BattleManager(object):
    MAX_PLAYER = 2

    # the count of turns, initial 0.
    _turn = 0

    # phase: 
    # 0 draw phase, 
    # 1 standby phase, 
    # 2 main phase,
    # 3 end phase.
    _phase = 0

    # player's number
    _player = 0

    # to help controlling battle coroutine
    battleHandler = None

    # all these phases are coroutines
    # we can put "required type" in "yield return" 
    # use battleHandler.send()
    def _drawPhase(self):
        self._phase = 0
        print("draw phase start.")
        # process all effects in queue
        # draw a card
        self._recvOpt = yield None
        print("draw phase end.")

    def _standbyPhase(self):
        self._phase = 1
        print("standby phase start.")
        # process all effects in queue
        self._recvOpt = yield None
        print("standby phase end.")

    def _mainPhase(self):
        self._phase = 2
        print("main phase start.")
        # process all effects in queue
        # hang-up the battleManager, wait for input

        # number 1 is for test
        self._recvOpt = yield 1

        print("main phase end.")

    def _endPhase(self):
        self._phase = 3
        print("end phase start.")
        # process all effects in queue
        self._recvOpt = yield None
        print("end phase end.")


    # yield from: continuously enum value from one iterator UNTIL it exhausts
    def _battleRoutine(self):
        print("battle start")
        while True:
            print("/////////////////////// player %d, turn %d start." % (self._player, self._turn))
            yield from self._drawPhase()
            yield from self._standbyPhase()
            yield from self._mainPhase()
            yield from self._endPhase()

            print("/////////////////////// turn %d end." % self._turn)
            self._player += 1
            if self._player >= self.MAX_PLAYER:
               self._turn += 1
               self._player = 0

    def init(self):
        self.battleHandler = self._battleRoutine()

    # same as pushForward, returns the type of the required operations
    def start(self):
        next(self.battleHandler) # tell coroutine to start battle
        return self.pushForward(None) # is this dangerous to push forward here?
        
    # send operations and continue the battle procedure
    # returns the type of the required operations
    def pushForward(self, opt):
        requiredType = self.battleHandler.send(opt) 
        opt = None # clear opt buffer
        while requiredType == None:
            requiredType = self.battleHandler.send(opt) 
        return requiredType

instance = BattleManager()