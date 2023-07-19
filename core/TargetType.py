from enum import Enum


class TargetType:
    def __init__(self, distance, team, aliveness, own):
        self.distance = distance
        self.team = team
        self.aliveness = aliveness
        self.own = own

    def __str__(self):
        return type(self).__name__


class Distance(Enum):
    ANY = 0
    NEARBY_ONLY = 1
    DISTANT_ONLY = 2


class Team(Enum):
    ANY = 0
    ALLIES_ONLY = 1
    ENEMIES_ONLY = 2


class Aliveness(Enum):
    ANY = 0
    ALIVE_ONLY = 1
    DEAD_ONLY = 2


class Own(Enum):
    SELF_INCLUDED = 0
    SELF_ONLY = 1
    SELF_EXCLUDED = 2


class Allies(TargetType):
    def __init__(self, distance=Distance.ANY, aliveness=Aliveness.ALIVE_ONLY):
        super().__init__(distance=distance, team=Team.ALLIES_ONLY, aliveness=aliveness, own=Own.SELF_INCLUDED)


class Enemies(TargetType):
    def __init__(self, distance=Distance.ANY, aliveness=Aliveness.ALIVE_ONLY):
        super().__init__(distance=distance, team=Team.ENEMIES_ONLY, aliveness=aliveness, own=Own.SELF_EXCLUDED)


class Everyone(TargetType):
    def __init__(self, distance=Distance.ANY, aliveness=Aliveness.ALIVE_ONLY, own=Own.SELF_INCLUDED):
        super().__init__(distance=distance, team=Team.ANY, aliveness=aliveness, own=own)


class OwnOnly(TargetType):
    def __init__(self):
        super().__init__(distance=Distance.ANY, team=Team.ANY, aliveness=Aliveness.ALIVE_ONLY, own=Own.SELF_ONLY)
