from core.Entities.Dummy import Dummy
from core.Sessions.Session import Session
import random

from core.Weapons.Claws import Claws
from core.Weapons.Drobovik import Drobovik
from core.Weapons.Obrez import Obrez
from core.Weapons.Fist import Fist
from core.Weapons.Kastet import Kastet
from core.Weapons.Tesak import Tesak
from core.Weapons.Revolver import Revolver
from core.Weapons.Pistol import Pistol
from core.Weapons.Flamethrower import Flamethrower

from core.Skills.Biceps import Biceps
from core.Skills.Dvuzhil import Dvuzhil
from core.Skills.Armor import Armor

from core.States.Aflame import Aflame


all_states = [Aflame]
all_skills = [Dvuzhil, Armor, Biceps]
all_weapons = [Claws, Drobovik, Obrez, Fist, Kastet, Tesak, Revolver, Pistol, Flamethrower]


def simulate():
    s = Session()

    PlayerA = Dummy(s, 'Алекс')
    PlayerB = Dummy(s, 'Скелет')

    PlayerA.weapon = Flamethrower() #random.choice(all_weapons)()
    PlayerB.weapon = random.choice(all_weapons)()

    PlayerA.skills += [random.choice(all_skills)()] + list(map(lambda s: s(), all_states))
    PlayerB.skills += [random.choice(all_skills)()] + list(map(lambda s: s(), all_states))

    s.entities = [PlayerA, PlayerB]

    while True:
        if not s.active:
            return
        s.trigger('pre-move')
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
