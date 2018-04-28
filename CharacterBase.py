class CharacterBase(object):
    poolIndex = 0
    owner = 0
    status = {}


    def __init__(self):
        self.status = {
            "HP" : 30,
            "ATK" : 15,
            "DEF" : 8,
            "INT" : 15,
            "RES" : 8,
            "SPD" : 10,
            "MOV" : 4,
            "RNG" : 1
        }