from core.Entities.Dummy import Dummy
from core.Sessions.Session import Session

from core.Weapons.Claws import Claws
from core.Weapons.Drobovik import Drobovik
from core.Weapons.Obrez import Obrez
from core.Weapons.Fist import Fist
from core.Weapons.Kastet import Kastet
from core.Weapons.Tesak import Tesak
from core.Weapons.Revolver import Revolver
from core.Weapons.Pistol import Pistol

from core.Skills.Biceps import Biceps
from core.Skills.Dvuzhil import Dvuzhil
from core.Skills.Armor import Armor
import random

all_skills = [Dvuzhil, Armor, Biceps]
all_weapons = [Claws, Drobovik, Obrez, Fist, Kastet, Tesak, Revolver, Pistol]


def simulate():
    s = Session()

    PlayerA = Dummy(s, 'Алекс')
    PlayerB = Dummy(s, 'Скелет')

    PlayerA.weapon = random.choice(all_weapons)()
    PlayerB.weapon = random.choice(all_weapons)()

    PlayerA.skills += [random.choice(all_skills)()]
    PlayerB.skills += [random.choice(all_skills)()]

    s.entities = [PlayerA, PlayerB]

    while True:
        if not s.active:
            return list(s.alive_entities)[0]
        s.trigger_skills('pre-move')
        print(f'Turn {s.turn} begins!')
        for player in s.alive_entities:
            while True:
                player.action = random.choice(player.actions)
                player.target = player
                if player.action.id == 'attack':
                    if not player.targets:
                        continue
                    player.target = random.choice(player.targets)
                break
        s.move()
        print()


simulate()
